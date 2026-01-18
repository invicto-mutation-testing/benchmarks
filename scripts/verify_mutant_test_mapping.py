#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mutant-Test Mapping Verifier

Determines which specific tests kill which specific mutants by running
each test individually against each mutant. This provides the granular
data needed to verify tables like tbl-extra-tests in the manuscript.

Usage:
    python verify_mutant_test_mapping.py --test-dir <path> [--venv-path <path>] [--repo-root <path>]

Output:
    - Console: per-mutant-per-test kill matrix
    - JSON file: detailed results for further analysis
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

DEFAULT_VENV = ".venv-invicto"
DEFAULT_TIMEOUT = 60  # per-test timeout (shorter than full suite)


@dataclass
class MutantInfo:
    id: int
    line: int
    operator: str
    description: str
    status_full_suite: str


@dataclass
class TestInfo:
    name: str
    class_name: Optional[str]
    full_name: str  # class.method or just method


@dataclass
class MutantTestResult:
    mutant_id: int
    test_name: str
    killed: bool
    error: Optional[str] = None


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Verify which tests kill which mutants for a specific test suite."
    )
    p.add_argument(
        "--test-dir",
        type=str,
        required=True,
        help="Path to test directory containing test_final.py and put.py/nds_script.py",
    )
    p.add_argument(
        "--venv-path",
        type=str,
        default=DEFAULT_VENV,
        help=f"Path to Python venv (default: {DEFAULT_VENV})",
    )
    p.add_argument(
        "--repo-root",
        type=str,
        default=None,
        help="Optional repository root to constrain --test-dir for cache deletion.",
    )
    p.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Timeout per individual test run in seconds (default: {DEFAULT_TIMEOUT})",
    )
    p.add_argument(
        "--output",
        type=str,
        default="mutant_test_mapping.json",
        help="Output JSON file path (default: mutant_test_mapping.json)",
    )
    p.add_argument(
        "--skip-full-run",
        action="store_true",
        help="Skip initial full mutmut run (use existing .mutmut-cache)",
    )
    return p.parse_args(argv)


def resolve_executable(venv_path: Path, exe_basename: str, fallback: str) -> str:
    """Find executable in venv or fall back to system PATH."""
    for subdir in ["Scripts", "bin"]:
        candidate = venv_path / subdir / exe_basename
        if candidate.exists():
            return str(candidate)
        # Try with .exe on Windows
        candidate_exe = venv_path / subdir / f"{exe_basename}.exe"
        if candidate_exe.exists():
            return str(candidate_exe)
    return fallback


def find_mutate_target(test_dir: Path) -> Optional[str]:
    """Determine the mutation target file."""
    if (test_dir / "put.py").exists():
        return "put.py"
    if (test_dir / "nds_script.py").exists():
        return "nds_script.py"
    return None


def _is_within(base: Path, target: Path) -> bool:
    try:
        target.relative_to(base)
        return True
    except Exception:
        return False


def remove_mutmut_cache(test_dir: Path, repo_root: Optional[Path] = None) -> None:
    """Remove existing .mutmut-cache to ensure fresh run."""
    try:
        test_dir = test_dir.resolve()
    except Exception:
        print(f"[WARN] Refusing to delete cache (path resolution failed) for {test_dir}")
        return

    if repo_root is not None:
        try:
            repo_root = repo_root.resolve()
        except Exception:
            print(f"[WARN] Refusing to delete cache (repo root resolution failed) for {repo_root}")
            return
        if not _is_within(repo_root, test_dir):
            print(f"[WARN] Refusing to delete cache outside repo root: {test_dir}")
            return

    if not (test_dir / "test_final.py").exists():
        print(f"[WARN] Refusing to delete cache; missing test_final.py in {test_dir}")
        return

    if not find_mutate_target(test_dir):
        print(f"[WARN] Refusing to delete cache; no mutate target in {test_dir}")
        return

    cache_path = test_dir / ".mutmut-cache"
    if not cache_path.exists():
        return
    try:
        if cache_path.is_symlink() or cache_path.is_file():
            cache_path.unlink()
        elif cache_path.is_dir():
            shutil.rmtree(cache_path)
        else:
            print(f"[WARN] Unknown cache path type at {cache_path}; skipping delete.")
    except Exception as e:
        print(f"[WARN] Failed to delete cache {cache_path}: {e!r}")


def run_full_mutmut(
    test_dir: Path,
    mutate_target: str,
    pytest_exe: str,
    mutmut_exe: str,
    timeout: int,
    repo_root: Optional[Path] = None,
) -> bool:
    """Run full mutmut suite to generate mutants and baseline statuses."""
    print(f"[INFO] Running full mutmut suite on {test_dir}...")

    remove_mutmut_cache(test_dir, repo_root)

    runner_cmd = f"{pytest_exe} ./test_final.py"
    args = [
        mutmut_exe, "run",
        "--paths-to-mutate", mutate_target,
        "--tests-dir", ".",
        "--runner", runner_cmd,
        "--no-progress", "--CI", "--simple-output",
    ]

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONHASHSEED"] = "0"

    try:
        result = subprocess.run(
            args,
            cwd=str(test_dir),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout * 10,  # Full suite gets more time
        )
        print(f"[INFO] Full mutmut run completed with exit code {result.returncode}")
        return True
    except subprocess.TimeoutExpired:
        print(f"[ERROR] Full mutmut run timed out after {timeout * 10}s")
        return False
    except Exception as e:
        print(f"[ERROR] Full mutmut run failed: {e}")
        return False


def get_mutants_from_cache(test_dir: Path) -> List[MutantInfo]:
    """Read mutant information from .mutmut-cache SQLite database."""
    cache_path = test_dir / ".mutmut-cache"
    if not cache_path.exists():
        print(f"[ERROR] No .mutmut-cache found at {cache_path}")
        return []

    mutants = []
    try:
        with sqlite3.connect(str(cache_path), timeout=5.0) as con:
            # Get mutant details
            cursor = con.execute("""
                SELECT id, line, status
                FROM Mutant
                ORDER BY id
            """)

            for row in cursor:
                mutant_id, line, status = row
                mutants.append(MutantInfo(
                    id=mutant_id,
                    line=line,
                    operator="unknown",  # mutmut doesn't store operator name directly
                    description=f"Mutant {mutant_id} at line {line}",
                    status_full_suite=status,
                ))
    except Exception as e:
        print(f"[ERROR] Failed to read mutmut cache: {e}")

    return mutants


def extract_test_names(test_file: Path) -> List[TestInfo]:
    """Parse test_final.py to extract all test function/method names."""
    tests = []
    try:
        source = test_file.read_text(encoding="utf-8")
        tree = ast.parse(source)

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name.startswith("test_"):
                        tests.append(TestInfo(
                            name=item.name,
                            class_name=class_name,
                            full_name=f"{class_name}::{item.name}",
                        ))
            elif isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                # Top-level test function
                if not any(isinstance(parent, ast.ClassDef) for parent in ast.walk(tree)):
                    tests.append(TestInfo(
                        name=node.name,
                        class_name=None,
                        full_name=node.name,
                    ))

        # Deduplicate (walk can visit nodes multiple times in nested structures)
        seen = set()
        unique_tests = []
        for t in tests:
            if t.full_name not in seen:
                seen.add(t.full_name)
                unique_tests.append(t)

        return unique_tests
    except Exception as e:
        print(f"[ERROR] Failed to parse test file: {e}")
        return []


def run_single_test_against_mutant(
    test_dir: Path,
    mutate_target: str,
    mutant_id: int,
    test_name: str,
    pytest_exe: str,
    mutmut_exe: str,
    timeout: int,
) -> Tuple[bool, Optional[str]]:
    """
    Run a single test against a specific mutant.
    Returns (killed: bool, error: Optional[str]).
    """
    # Use mutmut's apply mechanism to apply the mutant
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONHASHSEED"] = "0"

    try:
        # Apply the mutant
        apply_result = subprocess.run(
            [mutmut_exe, "apply", str(mutant_id)],
            cwd=str(test_dir),
            env=env,
            capture_output=True,
            text=True,
            timeout=10,
        )

        if apply_result.returncode != 0:
            return False, f"Failed to apply mutant: {apply_result.stderr}"

        # Run the specific test
        test_result = subprocess.run(
            [pytest_exe, "-xvs", f"test_final.py::{test_name}"],
            cwd=str(test_dir),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        # Test failure (non-zero exit) means the mutant was killed
        killed = test_result.returncode != 0

        return killed, None

    except subprocess.TimeoutExpired:
        return False, "timeout"
    except Exception as e:
        return False, str(e)
    finally:
        # Always try to restore original code
        try:
            subprocess.run(
                [mutmut_exe, "apply", "0"],  # Apply mutant 0 = restore original
                cwd=str(test_dir),
                env=env,
                capture_output=True,
                timeout=10,
            )
        except Exception:
            pass


def verify_mutant_test_mapping(
    test_dir: Path,
    venv_path: Path,
    timeout: int,
    skip_full_run: bool,
    repo_root: Optional[Path] = None,
) -> Tuple[List[MutantInfo], List[TestInfo], List[MutantTestResult]]:
    """
    Main verification logic.
    Returns (mutants, tests, results).
    """
    # Resolve executables
    pytest_exe = resolve_executable(venv_path, "pytest", "pytest")
    mutmut_exe = resolve_executable(venv_path, "mutmut", "mutmut")

    print(f"[INFO] Using pytest: {pytest_exe}")
    print(f"[INFO] Using mutmut: {mutmut_exe}")

    # Find mutation target
    mutate_target = find_mutate_target(test_dir)
    if not mutate_target:
        print(f"[ERROR] No mutation target (put.py or nds_script.py) found in {test_dir}")
        return [], [], []

    print(f"[INFO] Mutation target: {mutate_target}")

    # Run full mutmut if needed
    if not skip_full_run:
        if not run_full_mutmut(
            test_dir, mutate_target, pytest_exe, mutmut_exe, timeout, repo_root
        ):
            print("[ERROR] Full mutmut run failed")
            return [], [], []

    # Get mutants from cache
    mutants = get_mutants_from_cache(test_dir)
    if not mutants:
        print("[ERROR] No mutants found in cache")
        return [], [], []

    print(f"[INFO] Found {len(mutants)} mutants")

    # Extract test names
    test_file = test_dir / "test_final.py"
    tests = extract_test_names(test_file)
    if not tests:
        print("[ERROR] No tests found in test_final.py")
        return mutants, [], []

    print(f"[INFO] Found {len(tests)} tests:")
    for t in tests:
        print(f"       - {t.full_name}")

    # Run each test against each mutant
    results: List[MutantTestResult] = []
    total_runs = len(mutants) * len(tests)
    current_run = 0

    print(f"\n[INFO] Running {total_runs} test-mutant combinations...")

    for mutant in mutants:
        for test in tests:
            current_run += 1
            print(f"[{current_run}/{total_runs}] Mutant {mutant.id} vs {test.full_name}...", end=" ", flush=True)

            killed, error = run_single_test_against_mutant(
                test_dir,
                mutate_target,
                mutant.id,
                test.full_name,
                pytest_exe,
                mutmut_exe,
                timeout,
            )

            results.append(MutantTestResult(
                mutant_id=mutant.id,
                test_name=test.full_name,
                killed=killed,
                error=error,
            ))

            status = "KILLED" if killed else ("ERROR: " + error if error else "SURVIVED")
            print(status)

    return mutants, tests, results


def print_kill_matrix(
    mutants: List[MutantInfo],
    tests: List[TestInfo],
    results: List[MutantTestResult],
) -> None:
    """Print a readable kill matrix."""
    # Build lookup
    kill_map: Dict[Tuple[int, str], bool] = {}
    for r in results:
        kill_map[(r.mutant_id, r.test_name)] = r.killed

    print("\n" + "=" * 80)
    print("MUTANT-TEST KILL MATRIX")
    print("=" * 80)

    # Header
    test_names = [t.full_name for t in tests]
    max_test_len = max(len(n) for n in test_names) if test_names else 20

    print(f"\n{'Mutant':<10} | " + " | ".join(f"{t[:15]:<15}" for t in test_names))
    print("-" * (12 + 18 * len(tests)))

    for mutant in mutants:
        row = f"M{mutant.id:<9} | "
        kills_by = []
        for test in tests:
            killed = kill_map.get((mutant.id, test.full_name), False)
            row += f"{'KILL':<15} | " if killed else f"{'    ':<15} | "
            if killed:
                kills_by.append(test.full_name)
        print(row)

    # Summary: which tests kill which mutants
    print("\n" + "=" * 80)
    print("SUMMARY: Tests that kill each mutant")
    print("=" * 80)

    for mutant in mutants:
        killers = [
            t.full_name for t in tests
            if kill_map.get((mutant.id, t.full_name), False)
        ]
        if killers:
            print(f"Mutant {mutant.id}: {', '.join(killers)}")
        else:
            print(f"Mutant {mutant.id}: NOT KILLED by any individual test")

    # Reverse summary: which mutants each test kills
    print("\n" + "=" * 80)
    print("SUMMARY: Mutants killed by each test")
    print("=" * 80)

    for test in tests:
        killed_mutants = [
            m.id for m in mutants
            if kill_map.get((m.id, test.full_name), False)
        ]
        if killed_mutants:
            print(f"{test.full_name}: kills mutants {killed_mutants}")
        else:
            print(f"{test.full_name}: kills NO mutants")


def save_results(
    output_path: Path,
    test_dir: Path,
    mutants: List[MutantInfo],
    tests: List[TestInfo],
    results: List[MutantTestResult],
) -> None:
    """Save results to JSON file."""
    data = {
        "test_dir": str(test_dir),
        "mutants": [asdict(m) for m in mutants],
        "tests": [asdict(t) for t in tests],
        "results": [asdict(r) for r in results],
        "summary": {
            "total_mutants": len(mutants),
            "total_tests": len(tests),
            "total_combinations": len(results),
            "kills": sum(1 for r in results if r.killed),
        },
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"\n[INFO] Results saved to {output_path}")


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    test_dir = Path(args.test_dir).resolve()
    venv_path = Path(args.venv_path).resolve()
    output_path = Path(args.output).resolve()
    repo_root = None
    if args.repo_root:
        repo_root = Path(args.repo_root).resolve()
        if not repo_root.exists():
            print(f"[ERROR] Repo root does not exist: {repo_root}")
            return 1
        if not _is_within(repo_root, test_dir):
            print(f"[ERROR] Test directory is outside repo root: {test_dir}")
            return 1

    if not test_dir.exists():
        print(f"[ERROR] Test directory does not exist: {test_dir}")
        return 1

    if not (test_dir / "test_final.py").exists():
        print(f"[ERROR] No test_final.py found in {test_dir}")
        return 1

    print(f"[INFO] Test directory: {test_dir}")
    print(f"[INFO] Venv path: {venv_path}")
    print(f"[INFO] Timeout per test: {args.timeout}s")
    if repo_root is not None:
        print(f"[INFO] Repo root: {repo_root}")

    mutants, tests, results = verify_mutant_test_mapping(
        test_dir,
        venv_path,
        args.timeout,
        args.skip_full_run,
        repo_root,
    )

    if mutants and tests and results:
        print_kill_matrix(mutants, tests, results)
        save_results(output_path, test_dir, mutants, tests, results)
        return 0
    else:
        print("[ERROR] Verification failed - no results generated")
        return 1


if __name__ == "__main__":
    sys.exit(main())
