# INVICTO Benchmarking Pipeline

Raw measurement data and reproduction scripts for comparing the two operation modes of INVICTO using mutation testing and a bootstrap-based statistical analysis.

## At a Glance

- Platform: **Windows-only** (PowerShell 5.1, Python **3.10**, R **4.4.2**).
- One command to reproduce the full pipeline with 10 replications:

  ```powershell
  .\run_benchmark_pipeline.ps1 -Count 10
  ```

* Outputs in repo root:

  * `benchmark_results_medians.csv` – median mutation scores per configuration.
  * `statistical_analysis.json` – medians, effect sizes, normality tests.
* Intermediate CSVs and `benchmark_dataset.csv` live in `temp_results/`.
  Use `-GenerateShapiroTable` to also get `generated/tbl_shapiro.tex`.

---

## Quick Start

The top-level orchestrator `run_benchmark_pipeline.ps1` performs:

1. Python venv setup (`.venv-invicto`) via `scripts/create_python_venv.ps1`.
2. Optional initial cache clean in `assistant/` and `completions/`.
3. `Count` replicated mutation test runs via `scripts/run_mutmut_iterations.ps1`.
4. Aggregation of per-run CSVs via `scripts/compute_benchmark_statistics.py`.
5. Construction of `temp_results/benchmark_dataset.csv`.
6. Statistical analysis via `scripts/run_statistical_analysis.R`.

**Full pipeline (10 replications, manuscript settings):**

```powershell
.\run_benchmark_pipeline.ps1 -Count 10
```

**Same, but also generate the Shapiro–Wilk LaTeX table:**

```powershell
.\run_benchmark_pipeline.ps1 -Count 10 -GenerateShapiroTable
```

**Key outputs:**

* `benchmark_results_medians.csv` – final median mutation scores (root).
* `statistical_analysis.json` – consolidated statistics (root).
* `temp_results/` – raw per-iteration CSVs (`benchmark_results_*.csv`), aggregated CSVs, and `benchmark_dataset.csv`.

`benchmark_dataset.csv` is built from the **per-suite medians** (`benchmark_results_medians.csv`), not from raw per-iteration CSVs.

---

## Requirements

### Platform

* OS: **64-bit Windows 10 Pro** (tested) or newer Windows with PowerShell 5.1 available.
* Shell: **Windows PowerShell 5.1** (not PowerShell 7).
* Python: **3.10 (64-bit)** on `PATH` (required; enforced by `create_python_venv.ps1`).
* R: **R 4.4.2** on `PATH` as `Rscript`.

Linux/macOS are not supported by the provided scripts (they rely on `taskkill`, Windows venv layout, and PowerShell 5.1).

### Python environment

`requirements-invicto.txt` pins the packages used by the benchmark builder, including:

* `pytest`, `mutmut`, `pytest-mock`, `PyYAML`, `colorama`
* `requests`, `SQLAlchemy`, `PySide6`

Create the environment from the repo root:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\create_python_venv.ps1
```

This:

* Verifies `python --version` starts with `3.10`.
* Creates `.venv-invicto`.
* Installs from `requirements-invicto.txt`.

### R packages

`run_statistical_analysis.R` requires the following in the R 4.4.2 environment:

* `dplyr`
* `tidyr`
* `purrr`
* `WRS2` (version **1.1.6**)
* `effsize` (version **0.8.1**)
* `jsonlite`

Install:

```r
install.packages(c("dplyr", "tidyr", "purrr", "WRS2", "effsize", "jsonlite"))
packageVersion("WRS2")     # should be '1.1.6'
packageVersion("effsize")  # should be '0.8.1'
```

The pipeline uses `--nboot=100000` and seed `100` by default via `run_benchmark_pipeline.ps1` to match the manuscript.

---

## Repository Layout

* `run_benchmark_pipeline.ps1` – main orchestrator for the full pipeline.
* `scripts/`

  * `create_python_venv.ps1` – create/update `.venv-invicto` and install pinned Python deps.
  * `remove_mutation_caches.ps1` – delete `.mutmut-cache`, `.pytest_cache`, `__pycache__` under `assistant/` and `completions/`.
  * `run_mutmut_iterations.ps1` – run `run_single_mutation_test.py` `Count` times with cache cleans in between.
  * `run_single_mutation_test.py` – sweep `assistant/` and `completions/`, run `mutmut`, and emit per-suite CSV.
  * `compute_benchmark_statistics.py` – aggregate multiple benchmark CSVs into means/medians/stds.
  * `run_statistical_analysis.R` – compute medians, bootstrap differences, effect sizes, Shapiro–Wilk, and LaTeX.
  * `preview_dataset_columns.R` – quick inspection of `benchmark_dataset.csv` columns.
* `requirements-invicto.txt` – pinned Python dependencies.
* `baseline.csv` – semicolon-separated baselines (`tc_id;api;temp;…`) for Human and Copilot.
* `assistant/` – Assistant-mode LLM test suites (`tc_<put>_t<temp>_rep<id>/...`).
* `completions/` – Completions-mode LLM test suites, mirroring `assistant/`.
* Generated:

  * `benchmark_results_*.csv` – per-iteration benchmark results (in `temp_results/`).
  * `benchmark_results_means.csv`, `benchmark_results_medians.csv`, `benchmark_results_stds.csv`, `benchmark_results_aggregated.csv`.
  * `temp_results/benchmark_dataset.csv` – semicolon-delimited dataset for R.
  * `statistical_analysis.json` – consolidated JSON of summary, effects, and Shapiro–Wilk.
  * `generated/tbl_shapiro.tex` – Shapiro–Wilk LaTeX table body (only if `-GenerateShapiroTable` is used).

> **NOTE — Proprietary Code (M00)**
> The mutation target source for **M00** is proprietary and not included. `assistant/tc_m00_*/` and `completions/tc_m00_*/` contain placeholders. Contact the authors for academic access if you need to reproduce M00.

> **NOTE**
> Run all commands from the repository root where `assistant/`, `completions/`, `baseline.csv`, and `scripts/` are located.

---

## Pipeline Details

### 1. Cache cleaning (optional manual step)

**Script:** `scripts/remove_mutation_caches.ps1`

Removes `.mutmut-cache`, `.pytest_cache`, and `__pycache__` under `assistant/` and `completions/`:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\remove_mutation_caches.ps1
# Dry-run:
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\remove_mutation_caches.ps1 -DryRun
```

* Requires both `assistant/` and `completions/` to exist; missing roots cause a hard failure.
* Safety check: expects `baseline.csv` in the repo root; use `-Force` to override.
* `run_mutmut_iterations.ps1` calls this after each iteration; `run_benchmark_pipeline.ps1` optionally calls it once before the loop.

### 2. Replicated mutation benchmarks

**Script:** `scripts/run_mutmut_iterations.ps1`

Runs `run_single_mutation_test.py` `Count` times and cleans caches between iterations.

Example (10 replications):

```powershell
powershell -File .\scripts\run_mutmut_iterations.ps1 -Count 10
```

Key points:

* Preferentially uses `.venv-invicto\Scripts\python.exe`, else `python`.
* Writes `benchmark_results_<i>.csv` to `-OutputDir` (default `.`; the orchestrator uses `temp_results/`).
* After each run, invokes `remove_mutation_caches.ps1`.
* Each per-iteration CSV has columns:

  ```text
  put, api_mode, temperature, repetition_id, duration_seconds,
  file_size_bytes, killed_mutations, all_mutations, score,
  actual_test_path, status
  ```

  where `status` is one of `ok`, `failed`, `timeout`, or `error`.

### 3. Single benchmark sweep (advanced / debugging)

**Script:** `scripts/run_single_mutation_test.py`

Sweeps `assistant/` and `completions/` for `test_final.py` test suites and runs `mutmut` on each corresponding `put.py`/`nds_script.py`.

Example:

```powershell
& ".\.venv-invicto\Scripts\python.exe" .\scripts\run_single_mutation_test.py `
  --repo-root "." `
  --venv-path ".venv-invicto" `
  --output-path "mut_benchmark_results.csv" `
  --mutmut-timeout-seconds 300 `
  --jobs 1 `
  --python-hash-seed 0
```

Behavior (aligned with the current implementation):

* Requires at least **one** of `assistant/` or `completions/` under `--repo-root`.
  If neither exists, it errors: “At least one of completions, assistant must exist.”
* Metadata extraction:

  * Parses `tc_<put>_t<temp>_rep<id>` from directory names when possible.
  * Falls back to `meta.json`/`metadata.json` or to the directory name.
* Mutation metrics:

  * Runs `mutmut run` with a Pytest runner.
  * Reads `.mutmut-cache` (SQLite) directly and buckets statuses into `killed`, `timeout`, `suspicious`, `survived`, `skipped`.
  * `killed_mutations` = count in the `killed` bucket.
  * `all_mutations` = sum of all five buckets.
  * `score = killed_mutations / all_mutations` (0 if `all_mutations == 0`).
  * Uses the installed `mutmut`’s `MUTANT_STATUSES` mapping when available; otherwise a conservative static mapping.
* Uses Windows process groups and `taskkill` to enforce `--mutmut-timeout-seconds` and clean up on timeouts.
* `status` in the CSV indicates `ok`, `failed`, `timeout`, or `error`.

### 4. Aggregation of replicated CSVs

**Script:** `scripts/compute_benchmark_statistics.py`

Aggregates multiple benchmark CSVs (e.g., `benchmark_results_*.csv`) into per-row means, medians, stds, and a consolidated summary.

Example:

```powershell
& ".\.venv-invicto\Scripts\python.exe" .\scripts\compute_benchmark_statistics.py `
  --pattern "benchmark_results_*.csv" `
  --out-stem "benchmark_results"
```

Behavior:

* By default, looks for `benchmark_results_*.csv`.
* Expects metric columns: `killed_mutations`, `all_mutations`, `score`.
* Expects meta columns: `put`, `api_mode`, `temperature`, `repetition_id`, `duration_seconds`, `file_size_bytes`, `actual_test_path`.
* Applies a `RENAME_MAP` to support older column names (`tc_id`→`put`, `api`→`api_mode`, etc.).
* If a `status` column exists, rows with `status != "ok"` are excluded from statistics (set to NaN).
* Outputs (underscore naming, matching the current code):

  * `<stem>_means.csv`
  * `<stem>_medians.csv`
  * `<stem>_stds.csv`
  * `<stem>_aggregated.csv`

---

### 5. Statistical analysis

**Script:** `scripts/run_statistical_analysis.R`

Implements the manuscript’s statistics pipeline on `benchmark_dataset.csv` plus `baseline.csv`.

Example (matching orchestrator configuration):

```powershell
Rscript .\scripts\run_statistical_analysis.R --data=benchmark_dataset.csv --nboot=100000 --alpha=0.05
```

Inputs:

* `benchmark_dataset.csv` – semicolon-delimited, built from the raw per-iteration CSVs.
  Columns (in order):

  ```text
  put, api_mode, temperature, repetition_id, duration_seconds,
  file_size_bytes, killed_mutations, all_mutations, score, actual_test_path
  ```

* `baseline.csv` – Human and Copilot baselines (`tc_id;api;temp;rep;duration;file_size;killed;all;score`).

Key behavior:

* Uses `set.seed(100)` for reproducibility.

* Constructs `PUT`, `Mode` (Assistant/Completions/Human/Copilot), `Temp` (0/1), and percentage scores (`ScorePct`).

* Per PUT, runs four comparisons:

  1. Assistant vs Completions at T=0
  2. Assistant vs Completions at T=1
  3. T=0 vs T=1 within Assistant
  4. T=0 vs T=1 within Completions

* For each comparison:

  * Estimates differences in medians using `WRS2::pb2gen` with `nboot` replicates.
  * Computes Cliff’s delta via `effsize::cliff.delta`.
  * Applies Holm step-down correction within each PUT (`P_Adjusted`) and flags `Significant`.

* Shapiro–Wilk tests are run per `(PUT, Mode, Temp)`; p-values are formatted (very small p-values reported as `< 1e-6`).

Outputs:

* `statistical_analysis.json` – one JSON with:

  * `summary` – median summaries, including baselines.
  * `effects` – effect sizes, CIs, adjusted p-values, and skip reasons if a comparison could not be run.
  * `shapiro` – Shapiro–Wilk statistics and formatted p-values.

* `generated/tbl_shapiro.tex` – LaTeX rows for the Shapiro–Wilk table (only if `--no-shapiro-tex` is **not** passed; the orchestrator suppresses it unless `-GenerateShapiroTable` is used).

---

## Orchestrator flags

`run_benchmark_pipeline.ps1` supports:

* `-Count` – number of replicated runs (default `1`; use `10` to match the manuscript).
* `-EnvPath` – venv path (default `.venv-invicto`).
* `-Requirements` – requirements file (default `requirements-invicto.txt`).
* `-AggregatePattern` – pattern for per-iteration CSVs (default `benchmark_results_*.csv`).
* `-AggregateStem` – aggregation stem (default `benchmark_results`).
* `-DatasetOutput` – dataset filename under `temp_results/` (default `benchmark_dataset.csv`).
* `-BootstrapSamples` – `nboot` for `pb2gen` (default `100000`).
* `-Alpha` – significance level (default `0.05`).
* `-SkipInitialClean` – skip the initial `remove_mutation_caches.ps1` call before the loop.
* `-GenerateShapiroTable` – omit `--no-shapiro-tex` so `generated/tbl_shapiro.tex` is produced.

By running the orchestrator with the defaults on a populated `assistant/`/`completions/` tree and the provided `baseline.csv`, you can reproduce the benchmark and statistical analysis workflow used in the INVICTO study.
