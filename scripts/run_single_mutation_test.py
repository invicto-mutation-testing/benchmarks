#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mutmut Benchmark Builder — No-Input CSV, Directory Sweep
Windows 11 (PowerShell 5.1) • Python 3.10 • Single-file script (std lib only)

Changes in this version:
- Mutant counts are read DIRECTLY from `.mutmut-cache` (SQLite), not via `mutmut result-ids`.
- Uses the installed mutmut's MUTANT_STATUSES mapping when available; otherwise a safe fallback.
- Keeps all prior semantics, CSV schema, timeouts, process-tree cleanup, and deterministic ordering.
- Forces PYTHONHASHSEED=0 for every mutmut invocation by default (override with --python-hash-seed).
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import shutil
import signal
import sqlite3
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

DEFAULT_VENV = ".venv-invicto"
DEFAULT_OUTPUT = "mut_benchmark_results.csv"
DEFAULT_TIMEOUT = 300
DEFAULT_JOBS = 1
MAX_JOBS = 8

SCAN_ROOTS = ["completions", "assistant"]

CSV_HEADER = [
    "put",
    "api_mode",
    "temperature",
    "repetition_id",
    "duration_seconds",
    "file_size_bytes",
    "killed_mutations",
    "all_mutations",
    "score",
    "actual_test_path",
    "status",  # 'ok', 'failed', 'timeout', or 'error'
]

FLOAT_RX = re.compile(r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?')
# Accept any non-underscore chunk for tc_id (e.g., m02, s01, etc.).
# The previous pattern hard-coded 'm\d+' and failed for 'tc_s01_t1.0_rep1' style names,
# causing tc_id/api/temp/rep to be left empty in the CSV.
TC_SEGMENT_RX = re.compile(r"^tc_(?P<tc>[^_]+)_t(?P<temp>[^_]+)_rep(?P<rep>\d+)$", re.IGNORECASE)

@dataclass
class Config:
    repo_root: Path
    venv_path: Path
    output_path: Path
    mutmut_timeout_seconds: int
    jobs: int
    python_hash_seed: Optional[str]

@dataclass
class TestDir:
    root_name: str
    test_dir: Path
    mutate_target: str
    test_file: Path

@dataclass
class Row:
    tc_id: str
    api: str
    temp: str
    rep: str
    duration: Optional[float]
    file_size: int
    killed: int
    total: int
    score: float
    actual_test_path: str
    status: str  # 'ok', 'failed', 'timeout', or 'error'

# --- global state for cleanup ---
_active_procs_lock = threading.Lock()
_active_procs: Dict[int, subprocess.Popen] = {}
_stdout_lock = threading.Lock()
_per_dir_locks: Dict[Path, threading.Lock] = {}
_per_dir_locks_lock = threading.Lock()

def get_per_dir_lock(test_dir: Path) -> threading.Lock:
    with _per_dir_locks_lock:
        lk = _per_dir_locks.get(test_dir)
        if lk is None:
            lk = threading.Lock()
            _per_dir_locks[test_dir] = lk
        return lk

# ---------------------------
# CLI parsing and validation
# ---------------------------

def parse_args(argv: Optional[List[str]] = None) -> Config:
    p = argparse.ArgumentParser(description="Mutmut benchmark builder (sweeps directories; no input CSV).")
    p.add_argument("--repo-root", type=str, default=os.getcwd(), help="Repository root (default: CWD).")
    p.add_argument("--venv-path", type=str, default=DEFAULT_VENV, help="Venv dir relative to repo-root (default: .venv-invicto).")
    p.add_argument("--output-path", type=str, default=DEFAULT_OUTPUT, help="Output CSV path (overwritten).")
    p.add_argument("--mutmut-timeout-seconds", type=int, default=DEFAULT_TIMEOUT, help="Timeout per 'mutmut run' (seconds, > 0).")
    p.add_argument("--jobs", "-j", type=int, default=DEFAULT_JOBS, help="Max concurrent mutmut processes (1..8).")
    p.add_argument(
        "--python-hash-seed",
        type=str,
        default="0",
        help="Value assigned to PYTHONHASHSEED for each mutmut run (default: 0, set to '' to inherit ambient value).",
    )

    ns = p.parse_args(argv)
    repo_root = Path(ns.repo_root).resolve()
    venv_path = (repo_root / ns.venv_path).resolve()
    output_path = Path(ns.output_path).resolve()
    mutmut_timeout_seconds = int(ns.mutmut_timeout_seconds)
    jobs = int(ns.jobs)
    python_hash_seed = str(ns.python_hash_seed)

    if mutmut_timeout_seconds <= 0:
        p.error("--mutmut-timeout-seconds must be > 0")
    if not (1 <= jobs <= MAX_JOBS):
        p.error(f"--jobs must be in 1..{MAX_JOBS}")
    if python_hash_seed == "":
        python_hash_seed = None

    roots_present = [r for r in SCAN_ROOTS if (repo_root / r).exists()]
    if not roots_present:
        p.error(f"No scan roots found under {repo_root}. At least one of {', '.join(SCAN_ROOTS)} must exist.")

    return Config(repo_root, venv_path, output_path, mutmut_timeout_seconds, jobs, python_hash_seed)

# ---------------------------
# Logging helpers
# ---------------------------

def log(msg: str) -> None:
    with _stdout_lock:
        print(msg, flush=True)

def warn(msg: str) -> None:
    with _stdout_lock:
        print(f"[WARN] {msg}", flush=True)

def err(msg: str) -> None:
    with _stdout_lock:
        print(f"[ERROR] {msg}", flush=True, file=sys.stderr)

def quote_if_needed(s: str) -> str:
    s = str(s)
    if " " in s and not (s.startswith('"') and s.endswith('"')):
        return f'"{s}"'
    return s

def as_posix_relative(path: Path, base: Path) -> str:
    try:
        rel = path.relative_to(base)
    except Exception:
        rel = path
    return rel.as_posix()

def resolve_executable(repo_root: Path, venv_path: Path, exe_basename: str, fallback: str) -> str:
    candidate = venv_path / "Scripts" / exe_basename
    if candidate.exists():
        return str(candidate)
    return fallback

# ---------------------------
# Discovery
# ---------------------------

def choose_mutate_target(test_dir: Path) -> Optional[str]:
    if (test_dir / "put.py").exists():
        return "put.py"
    if (test_dir / "nds_script.py").exists():
        return "nds_script.py"
    return None

def find_test_dirs(cfg: Config) -> List[TestDir]:
    discovered: List[TestDir] = []
    for root_name in SCAN_ROOTS:
        root_dir = cfg.repo_root / root_name
        if not root_dir.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root_dir):
            d = Path(dirpath)
            if "test_final.py" not in filenames:
                continue
            mutate = choose_mutate_target(d)
            if not mutate:
                warn(f"Skipping {as_posix_relative(d, cfg.repo_root)}: no mutate target (put.py|nds_script.py) found.")
                continue
            discovered.append(TestDir(root_name, d, mutate, d / "test_final.py"))
    discovered.sort(key=lambda td: as_posix_relative(td.test_dir, cfg.repo_root))
    return discovered

# ---------------------------
# Metadata & duration
# ---------------------------

def derive_api_from_actual_test_path(rel_test: str) -> str:
    """Map the root of actual_test_path to api."""
    first = rel_test.split("/", 1)[0]
    if first in {"assistant", "assistant_clean"}:
        return "assistant"
    if first in {"completions", "completions_clean"}:
        return "completions"
    return ""

def derive_metadata(cfg: Config, td: TestDir, rel_test: str) -> Tuple[str, str, str, str]:
    """
    Populate (tc_id, api, temp, rep) by:
      - api from actual_test_path root segment
      - tc_id/temp/rep from 'tc_<tcid>_t<temp>_rep<rep>' in the FIRST path segment under the scan root
        e.g., assistant/tc_m02_t0.0_rep1/test_final.py -> (m02, assistant, 0.0, 1)
    Fallbacks: meta.json/metadata.json, then directory name (tc_id only).
    """
    api = derive_api_from_actual_test_path(rel_test)

    root_dir = cfg.repo_root / td.root_name
    try:
        rel_under_root = td.test_dir.relative_to(root_dir)
        first_seg = rel_under_root.parts[0] if rel_under_root.parts else td.test_dir.name
    except Exception:
        first_seg = td.test_dir.name

    m = TC_SEGMENT_RX.match(first_seg)
    if m:
        return m.group("tc"), api, m.group("temp"), m.group("rep")

    for meta_name in ("meta.json", "metadata.json"):
        meta_path = td.test_dir / meta_name
        if meta_path.exists():
            try:
                with meta_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                tc_id = str(data.get("tc_id", "") or "")
                temp = str(data.get("temp", "") or "")
                rep = str(data.get("rep", "") or "")
                if tc_id:
                    return tc_id, api, temp, rep
                else:
                    raise KeyError("tc_id missing")
            except Exception as e:
                warn(f"Failed to parse metadata in {as_posix_relative(meta_path, cfg.repo_root)}: {e!r}")
                break

    return td.test_dir.name, api, "", ""

def parse_duration_seconds(td: TestDir) -> Optional[float]:
    for name in ("sucess.txt", "success.txt"):
        p = td.test_dir / name
        if not p.exists():
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore").strip()
            m = FLOAT_RX.search(text)
            if m:
                if name == "success.txt":
                    warn(f"Used fallback {name} for duration at {td.test_dir}")
                return float(m.group(0))
            else:
                warn(f"Could not parse duration from {p.name} (no float found)")
                return None
        except Exception as e:
            warn(f"Could not read {p.name}: {e!r}")
            return None
    warn(f"No sucess.txt found in .; leaving duration empty")
    return None

# ---------------------------
# Mutmut run & process control
# ---------------------------

def _is_within(base: Path, target: Path) -> bool:
    try:
        target.relative_to(base)
        return True
    except Exception:
        return False

def remove_mutmut_cache(test_dir: Path, repo_root: Path) -> None:
    try:
        test_dir = test_dir.resolve()
        repo_root = repo_root.resolve()
    except Exception:
        # If resolution fails, skip deletion rather than risk unsafe cleanup.
        warn(f"Refusing to delete cache (path resolution failed) for {test_dir}")
        return

    if not _is_within(repo_root, test_dir):
        warn(f"Refusing to delete cache outside repo root: {as_posix_relative(test_dir, repo_root)}")
        return

    if not (test_dir / "test_final.py").exists():
        warn(f"Refusing to delete cache; missing test_final.py in {as_posix_relative(test_dir, repo_root)}")
        return

    if not ((test_dir / "put.py").exists() or (test_dir / "nds_script.py").exists()):
        warn(f"Refusing to delete cache; no mutate target in {as_posix_relative(test_dir, repo_root)}")
        return

    cache_dir = test_dir / ".mutmut-cache"
    try:
        if not cache_dir.exists():
            return
        if cache_dir.is_symlink() or cache_dir.is_file():
            cache_dir.unlink()
        elif cache_dir.is_dir():
            shutil.rmtree(cache_dir)
        else:
            warn(f"Unknown cache path type at {as_posix_relative(cache_dir, test_dir)}; skipping delete.")
    except Exception as e:
        warn(f"Failed to delete cache {as_posix_relative(cache_dir, test_dir)}: {e!r}")

def register_proc(p: subprocess.Popen) -> None:
    with _active_procs_lock:
        _active_procs[p.pid] = p

def unregister_proc(p: subprocess.Popen) -> None:
    with _active_procs_lock:
        _active_procs.pop(p.pid, None)

def _send_ctrl_break_to_group(pid: int) -> None:
    try:
        os.kill(pid, signal.CTRL_BREAK_EVENT)
    except Exception as e:
        warn(f"CTRL_BREAK_EVENT to {pid} failed: {e!r}")

def _taskkill_tree(pid: int) -> None:
    try:
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    except Exception as e:
        warn(f"taskkill failed for PID {pid}: {e!r}")

def run_mutmut(cfg: Config, td: TestDir, pytest_exe: str, mutmut_exe: str) -> Tuple[bool, Optional[int]]:
    runner_cmd = f"{quote_if_needed(pytest_exe)} .\\test_final.py"
    args = [
        mutmut_exe, "run",
        "--paths-to-mutate", td.mutate_target,
        "--tests-dir", ".",
        "--runner", runner_cmd,
        "--no-progress", "--CI", "--simple-output",
    ]
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    if cfg.python_hash_seed is not None:
        env["PYTHONHASHSEED"] = cfg.python_hash_seed
    remove_mutmut_cache(td.test_dir, cfg.repo_root)

    createflags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0

    with get_per_dir_lock(td.test_dir):
        start = time.time()
        p = subprocess.Popen(
            args, cwd=str(td.test_dir), env=env,
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, creationflags=createflags,
        )
        register_proc(p)
        try:
            try:
                stdout, stderr = p.communicate(timeout=cfg.mutmut_timeout_seconds)
                exit_code = p.returncode
                completed = True
            except subprocess.TimeoutExpired:
                _send_ctrl_break_to_group(p.pid)
                try:
                    p.communicate(timeout=5)
                except subprocess.TimeoutExpired:
                    pass
                _taskkill_tree(p.pid)
                try:
                    p.wait(timeout=5)
                except Exception:
                    pass
                completed = False
                exit_code = None
            finally:
                unregister_proc(p)
        finally:
            if p.poll() is None:
                _taskkill_tree(p.pid)
                try: p.kill()
                except Exception: pass
                try: p.wait(timeout=5)
                except Exception: pass

        elapsed = time.time() - start

    if not completed:
        warn(f"Timeout after {cfg.mutmut_timeout_seconds}s for {as_posix_relative(td.test_dir, cfg.repo_root)}; killed process tree (elapsed ~{elapsed:.1f}s)")
        return False, None
    return True, exit_code

# ---------------------------
# NEW: read counts from SQLite cache
# ---------------------------

def _venv_site_packages_candidates(venv_path: Path) -> List[Path]:
    cands = [
        venv_path / "Lib" / "site-packages",                 # Windows venv
        venv_path / "lib" / "site-packages",                 # generic
    ]
    # also add pythonXY path if present (e.g., lib/python3.10/site-packages)
    try:
        for sub in (venv_path / "lib").glob("python*/site-packages"):
            cands.append(sub)
    except Exception:
        pass
    return [p for p in cands if p.exists()]

def load_status_mapping_from_venv(venv_path: Path) -> Dict[str, str]:
    """
    Returns mapping {bucket: raw_status} from the installed mutmut.
    Falls back to a conservative static mapping if import fails.
    """
    # Default/fallback mapping (kept in sync with current mutmut):
    mapping = {
        "killed": "ok_killed",
        "timeout": "bad_timeout",
        "suspicious": "ok_suspicious",
        "survived": "bad_survived",
        "skipped": "skipped",
        "untested": "untested",
    }
    # Try to import mutmut from the venv site-packages
    for sp in _venv_site_packages_candidates(venv_path):
        try:
            if str(sp) not in sys.path:
                sys.path.insert(0, str(sp))
            import importlib
            mm = importlib.import_module("mutmut")
            mm_map = getattr(mm, "MUTANT_STATUSES", None)
            if isinstance(mm_map, dict) and mm_map:
                # ensure strings
                return {str(k): str(v) for k, v in mm_map.items()}
        except Exception:
            continue
    return mapping

def _open_sqlite_readonly(db_path: Path) -> sqlite3.Connection:
    """
    Open SQLite database read-only using URI (falls back to normal open).
    """
    try:
        uri = db_path.resolve().as_uri()
        # Append mode=ro for read-only
        sep = "&" if "?" in uri else "?"
        ro_uri = f"{uri}{sep}mode=ro"
        return sqlite3.connect(ro_uri, uri=True, timeout=5.0)
    except Exception:
        # Fallback (still safe; we only read)
        return sqlite3.connect(str(db_path), timeout=5.0)

def compute_counts_from_cache(td: TestDir, raw_status_map: Dict[str, str]) -> Tuple[bool, Dict[str, int]]:
    """
    Query `.mutmut-cache` and return counts for buckets:
    killed, timeout, suspicious, survived, skipped.
    Returns (ok, counts).
    """
    db_path = td.test_dir / ".mutmut-cache"
    if not db_path.exists():
        return False, {}
    # Reverse map raw->bucket
    raw_to_bucket = {raw: bucket for bucket, raw in raw_status_map.items()}
    wanted_buckets = ("killed", "timeout", "suspicious", "survived", "skipped")
    tallies: Dict[str, int] = {b: 0 for b in wanted_buckets}

    try:
        with _open_sqlite_readonly(db_path) as con:
            con.execute("PRAGMA query_only = 1")
            # Ensure Mutant table exists
            cur = con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Mutant'")
            if cur.fetchone() is None:
                return False, {}

            for status, count in con.execute("SELECT status, COUNT(*) FROM Mutant GROUP BY status"):
                bucket = raw_to_bucket.get(status, None)
                if bucket in tallies:
                    tallies[bucket] += int(count)
                # we ignore unknown/untested for the 'all' denominator per spec
        return True, tallies
    except Exception:
        return False, {}

def compute_score(killed: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round(killed / total, 6)

# ---------------------------
# Per-directory processing
# ---------------------------

def process_one(cfg: Config, td: TestDir, idx: int, totalN: int, pytest_exe: str, mutmut_exe: str, raw_status_map: Dict[str, str]) -> Row:
    rel_test = as_posix_relative(td.test_file, cfg.repo_root)
    log(f"Running mutmut for {as_posix_relative(td.test_dir, cfg.repo_root)} (target {td.mutate_target}) with timeout {cfg.mutmut_timeout_seconds}s...")
    tc_id, api, temp, rep = derive_metadata(cfg, td, rel_test)
    duration = parse_duration_seconds(td)
    file_size = td.test_file.stat().st_size

    completed, exit_code = run_mutmut(cfg, td, pytest_exe, mutmut_exe)

    killed = 0
    total_count = 0
    score = 0.0
    status = "ok"

    if not completed:
        # Timeout path
        status = "timeout"
        warn(f"[{idx}/{totalN}] {rel_test}: TIMEOUT - marked as failed")
    else:
        is_fatal = bool(exit_code & 1) if exit_code is not None else True
        if is_fatal:
            status = "failed"
            err(f"mutmut run reported fatal error (exit {exit_code}) in {as_posix_relative(td.test_dir, cfg.repo_root)}; counts set to zero, status=failed")
        else:
            ok, counts = compute_counts_from_cache(td, raw_status_map)
            if not ok:
                status = "error"
                err(f"Cache read error in {as_posix_relative(td.test_dir, cfg.repo_root)}; counts set to zero, status=error")
            else:
                killed = counts.get("killed", 0)
                total_count = sum(counts.get(k, 0) for k in ("killed", "timeout", "suspicious", "survived", "skipped"))
                score = compute_score(killed, total_count)
                status = "ok"

    log(f"[{idx}/{totalN}] {rel_test}: killed={killed} all={total_count} score={score} status={status}")
    return Row(tc_id, api, temp, rep, duration, file_size, killed, total_count, score, rel_test, status)

# ---------------------------
# CSV output
# ---------------------------

def write_csv(cfg: Config, rows: List[Row]) -> None:
    """Sort rows to match dataset expectations before writing the CSV."""

    # Ascending order: put (tc_id), api_mode (api), temperature (numeric), repetition_id (int).
    def _string_key(value: str) -> str:
        return (value or "").lower()

    def _temperature_key(value: str) -> float:
        try:
            return float(value)
        except Exception:
            return float("inf")  # unknown temps last

    def _repetition_key(value: str) -> int:
        try:
            return int(value)
        except Exception:
            return 2**31 - 1  # unknown reps last

    rows_sorted = sorted(
        rows,
        key=lambda r: (
            _string_key(r.tc_id),
            _string_key(r.api),
            _temperature_key(r.temp),
            _repetition_key(r.rep),
            r.actual_test_path,
        ),
    )
    with cfg.output_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(CSV_HEADER)
        for r in rows_sorted:
            duration_str = "" if r.duration is None else ("%.12g" % r.duration)
            w.writerow([
                r.tc_id, r.api, r.temp, r.rep,
                duration_str,
                r.file_size,
                r.killed,
                r.total,
                ("%.6f" % r.score) if r.total > 0 else "0.0",
                r.actual_test_path,
                r.status,
            ])
    # Report summary including failed counts
    ok_count = sum(1 for r in rows_sorted if r.status == "ok")
    failed_count = len(rows_sorted) - ok_count
    log(f"Wrote {len(rows_sorted)} rows to {cfg.output_path} ({ok_count} ok, {failed_count} failed/timeout/error)")

# ---------------------------
# Tool resolution & cleanup
# ---------------------------

def discover_validate(cfg: Config) -> List[TestDir]:
    tds = find_test_dirs(cfg)
    if not tds:
        warn("No qualifying test directories found (need test_final.py and a mutate target). Writing empty CSV with header only.")
    return tds

def resolve_tools(cfg: Config) -> Tuple[str, str]:
    pytest_exe = resolve_executable(cfg.repo_root, cfg.venv_path, "pytest.exe", "pytest")
    mutmut_exe = resolve_executable(cfg.repo_root, cfg.venv_path, "mutmut.exe", "mutmut")
    return pytest_exe, mutmut_exe

def cleanup_all_processes() -> None:
    with _active_procs_lock:
        procs = list(_active_procs.values())
    for p in procs:
        try: os.kill(p.pid, signal.CTRL_BREAK_EVENT)
        except Exception: pass
    time.sleep(1.0)
    for p in procs:
        try: subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception: pass
    for p in procs:
        try:
            if p.poll() is None:
                p.kill()
        except Exception:
            pass
        try: p.wait(timeout=3)
        except Exception: pass

# ---------------------------
# main
# ---------------------------

def main(argv: Optional[List[str]] = None) -> int:
    cfg = parse_args(argv)
    tds = discover_validate(cfg)
    pytest_exe, mutmut_exe = resolve_tools(cfg)

    rows: List[Row] = []
    totalN = len(tds)

    # Preload status mapping from the target venv (used for ALL dirs)
    raw_status_map = load_status_mapping_from_venv(cfg.venv_path)

    if totalN == 0:
        write_csv(cfg, rows)
        return 0

    counter_lock = threading.Lock()
    index_counter = {"i": 0}

    def wrap_process(td: TestDir) -> Row:
        with counter_lock:
            index_counter["i"] += 1
            idx = index_counter["i"]
        try:
            return process_one(cfg, td, idx, totalN, pytest_exe, mutmut_exe, raw_status_map)
        except Exception as e:
            err(f"Unhandled exception in {as_posix_relative(td.test_dir, cfg.repo_root)}: {e!r}")
            rel_test = as_posix_relative(td.test_file, cfg.repo_root)
            tc_id, api, temp, rep = derive_metadata(cfg, td, rel_test)
            duration = parse_duration_seconds(td)
            file_size = td.test_file.stat().st_size if td.test_file.exists() else 0
            return Row(tc_id, api, temp, rep, duration, file_size, 0, 0, 0.0, rel_test, "error")

    try:
        with ThreadPoolExecutor(max_workers=cfg.jobs) as ex:
            futures = [ex.submit(wrap_process, td) for td in tds]
            for fut in as_completed(futures):
                rows.append(fut.result())
    except KeyboardInterrupt:
        err("KeyboardInterrupt received; terminating all active processes...")
        cleanup_all_processes()
        raise

    write_csv(cfg, rows)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit as e:
        raise
    except Exception as e:
        err(f"Fatal error: {e!r}")
        cleanup_all_processes()
        sys.exit(1)
