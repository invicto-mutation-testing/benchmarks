#!/usr/bin/env python3
"""
Aggregate benchmark result CSV files using pandas.

For each row and for the columns ["killed_mutations", "all_mutations", "score"], compute
the mean, median, and standard deviation across all matching input CSVs.

Output structure per stats file (same row count as inputs):
  - Means:   [put, api_mode, temperature, repetition_id, duration_seconds, file_size_bytes,
              killed_means, all_means, score_means, actual_test_path]
  - Medians: [put, api_mode, temperature, repetition_id, duration_seconds, file_size_bytes,
              killed_medians, all_medians, score_medians, actual_test_path]
  - Stds:    [put, api_mode, temperature, repetition_id, duration_seconds, file_size_bytes,
              killed_stds, all_stds, score_stds, actual_test_path]

Filenames default to "<stem>_means.csv" etc., with <stem> derived from the
matched pattern (e.g., benchmark_results). You can override with --out-stem.

Additionally writes a consolidated CSV with schema:
  [put, api_mode, temperature, repetition_id, duration_seconds, file_size_bytes,
   killed_means, killed_medians, all_means,
   score_means, score_medians, score_stds,
   actual_test_path]
to "<stem>_aggregated.csv".
"""

from pathlib import Path
import sys
import argparse

import numpy as np
import pandas as pd


COLUMNS = ["killed_mutations", "all_mutations", "score"]
META_PREFIX = ["put", "api_mode", "temperature", "repetition_id", "duration_seconds", "file_size_bytes"]
META_SUFFIX = "actual_test_path"
STATUS_COLUMN = "status"  # Optional column: 'ok', 'failed', 'timeout', 'error'

# Allow legacy column names to be mapped into the new schema transparently.
RENAME_MAP = {
    "tc_id": "put",
    "api": "api_mode",
    "temp": "temperature",
    "rep": "repetition_id",
    "duration": "duration_seconds",
    "file_size": "file_size_bytes",
    "killed": "killed_mutations",
    "all": "all_mutations",
}

# Default search order: we pick the first pattern that matches at least one file.
# Supports both new naming (benchmark_results_*) and legacy naming (reproseed-*).
DEFAULT_PATTERNS = [
    "benchmark_results_*.csv",
    "@reproseed-10-*.csv",
    "reproseed-10-*.csv",
    "@reproseed-dd-*.csv",
    "reproseed-dd-*.csv",
]


def derive_stem_from_pattern(pat: str) -> str:
    p = pat.lower()
    if "benchmark_results" in p:
        return "benchmark_results"
    if "-10-" in p:
        return "reproseed-10"
    if "-dd-" in p:
        return "reproseed-dd"
    return "benchmark_results"


def is_aggregate_output(path: Path) -> bool:
    name = path.name.lower()
    return (
        name.endswith("_means.csv")
        or name.endswith("_medians.csv")
        or name.endswith("_stds.csv")
        or name.endswith("_aggregated.csv")
        # Also match legacy hyphen-separated names
        or name.endswith("-means.csv")
        or name.endswith("-medians.csv")
        or name.endswith("-stds.csv")
        or name.endswith("-aggregated.csv")
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate benchmark result CSVs with pandas")
    parser.add_argument(
        "--pattern",
        "-p",
        action="append",
        help=(
            "Glob pattern to match inputs (can be repeated). "
            "If multiple are provided, the first with matches is used."
        ),
    )
    parser.add_argument(
        "--out-stem",
        "-o",
        help=(
            "Stem for output files (e.g., 'benchmark_results'). "
            "Defaults to a value derived from the matched pattern."
        ),
    )

    args = parser.parse_args()

    base = Path.cwd()

    patterns = args.pattern if args.pattern else DEFAULT_PATTERNS
    selected_pattern = None
    files = []
    for pat in patterns:
        matched = [p for p in sorted(base.glob(pat)) if not is_aggregate_output(p)]
        if matched:
            selected_pattern = pat
            files = matched
            break
    if not files:
        print(
            "No files found. Tried patterns: "
            + ", ".join(repr(p) for p in patterns)
            + f" in {base}",
            file=sys.stderr,
        )
        return 1

    frames = []
    lengths = []
    total_failed_rows = 0

    for i, fp in enumerate(files):
        try:
            df = pd.read_csv(fp)
        except Exception as exc:
            print(f"ERROR: Failed to read {fp.name}: {exc}", file=sys.stderr)
            return 2

        # Normalize legacy column names to the latest schema.
        rename_pairs = {old: new for old, new in RENAME_MAP.items() if old in df.columns and new not in df.columns}
        if rename_pairs:
            df = df.rename(columns=rename_pairs)

        missing = [c for c in COLUMNS if c not in df.columns]
        if missing:
            print(
                f"ERROR: {fp.name} is missing required columns: {missing}",
                file=sys.stderr,
            )
            return 3

        # Ensure meta columns exist in the selected dataset
        meta_missing = [c for c in (META_PREFIX + [META_SUFFIX]) if c not in df.columns]
        if meta_missing:
            print(
                f"ERROR: {fp.name} is missing required meta columns: {meta_missing}",
                file=sys.stderr,
            )
            return 3

        # Select only the required columns and coerce to numeric (non-numeric -> NaN)
        sub = df.loc[:, COLUMNS].apply(pd.to_numeric, errors="coerce")

        # If status column exists, set failed rows to NaN so they are excluded from statistics
        if STATUS_COLUMN in df.columns:
            failed_mask = df[STATUS_COLUMN] != "ok"
            failed_count = failed_mask.sum()
            if failed_count > 0:
                total_failed_rows += failed_count
                print(f"  {fp.name}: {failed_count} failed/timeout/error rows will be excluded from statistics")
                # Set failed rows to NaN - they will be ignored by nanmean/nanmedian/nanstd
                sub.loc[failed_mask, :] = np.nan

        frames.append(sub)
        lengths.append(len(sub))

        # Capture meta columns from the first file to carry over into outputs
        if i == 0:
            meta_prefix_df = df.loc[:, META_PREFIX].copy()
            meta_suffix_df = df.loc[:, [META_SUFFIX]].copy()
            # Also capture status if present
            if STATUS_COLUMN in df.columns:
                status_df = df.loc[:, [STATUS_COLUMN]].copy()
            else:
                status_df = None

    # All inputs must have identical row counts to preserve dimensions
    if len(set(lengths)) != 1:
        print("ERROR: Input CSVs do not have the same number of rows:", file=sys.stderr)
        for fp, n in zip(files, lengths):
            print(f"  {fp.name}: {n}", file=sys.stderr)
        return 4

    # Stack into a 3D array: (num_files, num_rows, 3)
    arr = np.stack([f.to_numpy() for f in frames], axis=0)

    # Compute statistics across files, ignoring NaNs if present
    mean_arr = np.nanmean(arr, axis=0)
    median_arr = np.nanmedian(arr, axis=0)
    ddof = 1 if arr.shape[0] > 1 else 0  # sample std if multiple files
    std_arr = np.nanstd(arr, axis=0, ddof=ddof)

    mean_df = pd.DataFrame(
        mean_arr, columns=["killed_means", "all_means", "score_means"]
    )
    median_df = pd.DataFrame(
        median_arr, columns=["killed_medians", "all_medians", "score_medians"]
    )
    std_df = pd.DataFrame(
        std_arr, columns=["killed_stds", "all_stds", "score_stds"]
    )

    # Assemble final outputs with required column order
    means_out = pd.concat([meta_prefix_df.reset_index(drop=True), mean_df, meta_suffix_df], axis=1)
    medians_out = pd.concat([meta_prefix_df.reset_index(drop=True), median_df, meta_suffix_df], axis=1)
    stds_out = pd.concat([meta_prefix_df.reset_index(drop=True), std_df, meta_suffix_df], axis=1)

    # Determine output stem
    out_stem = args.out_stem or derive_stem_from_pattern(selected_pattern)

    # Save outputs (no index to keep column count to three)
    means_out.to_csv(base / f"{out_stem}_means.csv", index=False, lineterminator="\n")
    medians_out.to_csv(base / f"{out_stem}_medians.csv", index=False, lineterminator="\n")
    stds_out.to_csv(base / f"{out_stem}_stds.csv", index=False, lineterminator="\n")

    # Consolidated output with the requested schema
    consolidated = pd.concat(
        [
            meta_prefix_df.reset_index(drop=True),
            mean_df[["killed_means"]],
            median_df[["killed_medians"]],
            mean_df[["all_means", "score_means"]],
            median_df[["score_medians"]],
            std_df[["score_stds"]],
            meta_suffix_df,
        ],
        axis=1,
    )
    consolidated.to_csv(base / f"{out_stem}_aggregated.csv", index=False, lineterminator="\n")

    msg = f"Matched pattern {selected_pattern!r} with {len(files)} files."
    if total_failed_rows > 0:
        msg += f"\n  NOTE: {total_failed_rows} total failed/timeout/error rows across all files were excluded from statistics."
    msg += f"\nWrote {out_stem}_means.csv, {out_stem}_medians.csv, {out_stem}_stds.csv, {out_stem}_aggregated.csv"
    print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
