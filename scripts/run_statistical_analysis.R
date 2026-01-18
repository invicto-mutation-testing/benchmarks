#!/usr/bin/env Rscript

# -----------------------------------------------------------------------------
# Analysis pipeline:
# - Medians by configuration (PUT x Mode x Temp) for the "Results" tables.
# - Median-difference bootstraps (WRS2::pb2gen) with Cliff's delta and Holm
#   correction, matching "Statistical Methodology".
# - Shapiro-Wilk normality checks per configuration and LaTeX rows for the
#   "Shapiro-Wilk test results for normality" table (see "Distribution Analysis").
#
# NOTE ON BOOTSTRAP REPLICATES:
# Default nboot=1e3 for speed. Use --nboot=100000 to match the manuscript
# configuration (see "Technical Details" -> "INVICTO Software Environment").
# -----------------------------------------------------------------------------

suppressPackageStartupMessages({
  library(dplyr)
  library(tidyr)
  library(purrr)     # for pmap_dfr
  library(WRS2)      # percentile bootstrap for robust estimators (pb2gen)
  library(effsize)   # Cliff's delta (see "Statistical Methodology")
  library(jsonlite)
})

# -----------------------------------------------------------------------------
# CLI: accepts a dataset CSV path plus --nboot and --alpha (alpha=0.05).
# Usage:
#   Rscript run_statistical_analysis.R [DATASET_CSV] [--nboot=N] [--alpha=A]
# - DATASET_CSV (optional): defaults to "benchmark_dataset.csv"; semicolon-separated.
# - nboot controls pb2gen bootstrap replicates. INVICTO: 1e5; default here: 1e3.
# - alpha drives Holm-adjusted significance and Shapiro table labelling.
# -----------------------------------------------------------------------------
args <- commandArgs(trailingOnly = TRUE)
nboot <- 1000L
alpha <- 0.05
dataset_path <- "benchmark_dataset.csv"
generate_shapiro_tex <- TRUE

for (arg in args) {
  if (startsWith(arg, "--nboot=")) {
    candidate <- as.integer(sub("^--nboot=", "", arg))
    if (!is.na(candidate) && candidate > 0) {
      nboot <- candidate
    }
  }
  if (startsWith(arg, "--alpha=")) {
    candidate <- as.numeric(sub("^--alpha=", "", arg))
    if (!is.na(candidate) && candidate > 0 && candidate < 1) {
      alpha <- candidate
    }
  }
  if (startsWith(arg, "--data=")) {
    candidate <- sub("^--data=", "", arg)
    if (nzchar(candidate)) {
      dataset_path <- candidate
    }
  }
  if (arg == "--no-shapiro-tex") {
    generate_shapiro_tex <- FALSE
  }
}

# If a positional (non --flag) argument is provided, treat first as dataset CSV.
if (length(args) > 0) {
  for (arg in args) {
    if (!startsWith(arg, "--")) {
      dataset_path <- arg
      break
    }
  }
}

# Reproducibility seed = 100, as documented in "Technical Details" -> "INVICTO Software Environment".
set.seed(100)

# ---- Helpers ---------------------------------------------------------------
# Normalize mode names to manuscript labels (Assistant, Completions, Human, Copilot).
map_mode_labels <- function(x) {
  recode(
    x,
    "assistant" = "Assistant",
    "completions" = "Completions",
    "human" = "Human",
    "copilot" = "Copilot",
    .default = tools::toTitleCase(x)
  )
}

# Load the 40-run LLM dataset (2 modes x 2 temps x 10 reps) per PUT, as
# used throughout "Results". Compute ScorePct = score * 100 (see "Evaluation Protocol").
# Filters out rows with status != 'ok' if status column is present.
load_llm_data <- function(path = "benchmark_dataset.csv") {
  df <- read.csv(path, sep = ";", stringsAsFactors = FALSE)

  # Filter out failed/timeout/error rows if status column exists
  if ("status" %in% colnames(df)) {
    n_before <- nrow(df)
    df <- df %>% filter(status == "ok")
    n_after <- nrow(df)
    if (n_before != n_after) {
      message(sprintf("Filtered out %d failed/timeout/error rows (kept %d ok rows)",
                      n_before - n_after, n_after))
    }
  }

  df %>%
    mutate(
      PUT = put,                                  # S00, S01, M00, M01
      Mode = map_mode_labels(api_mode),           # Assistant/Completions
      Temp = as.integer(temperature),             # 0 or 1
      ScorePct = score * 100,                     # % mutation score
      Killed = killed_mutations,                  # raw killed mutants
      All = all_mutations                         # total mutants for this PUT
    )
}

# Load single-shot baselines (Human, Copilot). They appear in the summary
# only and are excluded from effect-size tests.
load_baseline_data <- function(path = "baseline.csv") {
  read.csv(path, sep = ";", stringsAsFactors = FALSE) %>%
    mutate(
      PUT = tc_id,
      Mode = map_mode_labels(api),
      Temp = as.integer(temp),
      ScorePct = score * 100,
      Killed = killed,
      All = all
    )
}

# Formatting utilities:
# - Scientific notation for p-values (JSON or LaTeX).
# - Clamp p < 1e-6 to "< 1e-6" to avoid impossible p=0 prints.
format_scientific <- function(x, digits = 1, style = c("latex", "plain")) {
  style <- match.arg(style)
  formatted <- formatC(x, format = "e", digits = digits)
  if (style == "plain") {
    return(formatted)
  }
  parts <- strsplit(formatted, "e", fixed = TRUE)[[1]]
  mantissa <- parts[1]
  exponent <- as.integer(parts[2])
  sprintf("%s\\times10^{%d}", mantissa, exponent)
}

# Render p-values for LaTeX and JSON.
# - Clamp p < 1e-6 to "< 1e-6"; otherwise format in scientific notation.
# - The caller handles bolding and markers.
format_p_value <- function(p, digits = 1, threshold = 1e-6, style = c("latex", "plain")) {
  style <- match.arg(style)
  vapply(p, function(val) {
    if (is.na(val)) {
      return(if (style == "latex") "--" else "--")
    }
    if (val < threshold) {
      formatted <- format_scientific(threshold, digits = digits, style = style)
      if (style == "latex") {
        return(sprintf("\\ensuremath{< %s}", formatted))
      }
      return(sprintf("< %s", formatted))
    }
    formatted <- format_scientific(val, digits = digits, style = style)
    if (style == "latex") {
      return(sprintf("\\ensuremath{%s}", formatted))
    }
    formatted
  }, character(1))
}

# Shapiro W statistic printed to 3 decimals (as in the table).
format_w_stat <- function(w) {
  formatC(w, format = "f", digits = 3)
}

# Significance markers (see the p-value thresholds table):
#  - (*) for 0.01 <= p < 0.05
#  - (**) for p < 0.01
sig_annotation <- function(p, alpha = 0.05) {
  case_when(
    is.na(p) ~ "",
    p < 0.01 ~ " \\textbf{(**)}",
    p < alpha ~ " \\textbf{(*)}",
    TRUE ~ ""
  )
}

# Print LaTeX table lines for the Shapiro-Wilk normality table ("Distribution Analysis").
#  - Bold rows when p < alpha (Non-normal).
#  - Show p-values in scientific notation; clamp p < 1e-6.
#  - Append (*) for p < 0.05, (**) for p < 0.01.
#  - Skipped rows (insufficient data) are marked with "--" and "Skipped".
write_shapiro_tex <- function(shapiro_tbl, alpha = 0.05, path = "generated/tbl_shapiro.tex") {
  # Order rows PUT-wise to match paper layout (S00, S01, M00, M01).
  order_puts <- c("S00", "S01", "M00", "M01")
  # Modes appear in this order in the LaTeX table.
  order_modes <- c("Assistant", "Completions", "Copilot", "Human")

  rows <- shapiro_tbl %>%
    arrange(match(PUT, order_puts), match(Mode, order_modes), Temp) %>%
    mutate(
      Significant = !is.na(P_Value) & P_Value < alpha,
      Stars = sig_annotation(P_Value, alpha = alpha),
      PutCell = ifelse(Significant, sprintf("\\textbf{%s}", PUT), PUT),
      ModeCell = ifelse(Significant, sprintf("\\textbf{%s}", Mode), Mode),
      TempCell = ifelse(Significant, sprintf("\\textbf{%d}", Temp), as.character(Temp)),
      WCellRaw = ifelse(is.na(W), "--", format_w_stat(W)),
      WCell = ifelse(Significant, sprintf("\\textbf{%s}", WCellRaw), WCellRaw),
      PFormatted = format_p_value(P_Value, style = "latex"),
      PCell = ifelse(Significant, sprintf("\\textbf{%s}", PFormatted), PFormatted),
      DistCell = case_when(
        Skipped ~ "\\textit{Skipped}",
        Significant ~ "\\textbf{Non-normal}",
        TRUE ~ "Normal"
      ),
      Row = sprintf("%s & %s & %s & %s & %s%s & %s\\\\",
                    PutCell, ModeCell, TempCell, WCell, PCell, Stars, DistCell)
    )

  dir.create(dirname(path), showWarnings = FALSE, recursive = TRUE)
  writeLines(rows$Row, con = path)
}

# -----------------------------------------------------------------------------
# Compute medians by (PUT x Mode x Temp) for both LLM runs and baselines.
# Use medians (robust in small samples).
# -----------------------------------------------------------------------------
median_summary <- function(llm_df, baseline_df) {
  llm_tbl <- llm_df %>%
    group_by(PUT, Mode, Temp) %>%
    summarise(
      MedianScorePct = median(ScorePct, na.rm = TRUE),
      MedianKilled = median(Killed, na.rm = TRUE),   # may be .5 with even n
      TotalMutants = first(na.omit(All)),
      .groups = "drop"
    )

  # Baseline rows are singletons (Human, Copilot). Keep their values for the
  # summary table; exclude from effect-size tests.
  baseline_tbl <- baseline_df %>%
    transmute(
      PUT,
      Mode,
      Temp,
      MedianScorePct = ScorePct,
      MedianKilled = Killed,
      TotalMutants = All
    )

  bind_rows(llm_tbl, baseline_tbl) %>%
    arrange(match(PUT, c("S00", "S01", "M00", "M01")), Mode, Temp)
}

# -----------------------------------------------------------------------------
# Effect-size and significance testing (see "Statistical Methodology").
# Within each PUT: (a) Mode at T=0, (b) Mode at T=1, (c) T within Assistant,
# (d) T within Completions.
# - Estimator: difference in MEDIANS via percentile bootstrap (pb2gen).
# - Effect size: Cliff's delta (delta) with interpretation thresholds in the
#   effect-size thresholds table.
# - Multiplicity: Holm step-down within each PUT across the four tests.
# - Gracefully handles missing PUTs or insufficient data by skipping comparisons.
# -----------------------------------------------------------------------------
effect_comparisons <- function(llm_df, nboot, alpha) {
  # Get the list of PUTs actually present in the data

available_puts <- unique(llm_df$PUT)

  # Define four comparisons per PUT (labels "Fix" and "Compare" match columns
  # in the manuscript's table "Mutation score comparisons with large effect sizes").
  # Only include PUTs that exist in the data.
  all_puts <- c("S00", "S01", "M00", "M01")
  active_puts <- intersect(all_puts, available_puts)

  if (length(active_puts) == 0) {
    message("WARNING: No PUTs found in dataset for effect comparisons")
    return(tibble(
      PUT = character(),
      Fix = character(),
      Compare = character(),
      DiffPct = numeric(),
      CI_Low = numeric(),
      CI_High = numeric(),
      P_Value = numeric(),
      CliffDelta = numeric(),
      P_Adjusted = numeric(),
      Significant = logical(),
      Skipped = logical(),
      SkipReason = character()
    ))
  }

  # Report which PUTs are missing
  missing_puts <- setdiff(all_puts, available_puts)
  if (length(missing_puts) > 0) {
    message(sprintf("WARNING: The following PUTs are missing from the dataset and will be skipped: %s",
                    paste(missing_puts, collapse = ", ")))
  }

  # Build comparisons only for available PUTs
  comparisons <- tibble()
  for (put in active_puts) {
    comparisons <- bind_rows(comparisons, tribble(
      ~PUT, ~Grouping, ~Fix, ~Compare, ~FilterExpr,
      put, "Mode", "T=0", "Assistant vs Completions", quote(Temp == 0),
      put, "Mode", "T=1", "Assistant vs Completions", quote(Temp == 1),
      put, "Temp", "Mode=Assistant", "T=0 vs T=1", quote(Mode == "Assistant"),
      put, "Temp", "Mode=Completions", "T=0 vs T=1", quote(Mode == "Completions")
    ))
  }

  results <- purrr::pmap_dfr(comparisons, function(PUT, Grouping, Fix, Compare, FilterExpr) {
    data_subset <- llm_df %>%
      filter(PUT == !!PUT) %>%
      filter(!!FilterExpr)

    # Grouping determines whether we compare Mode or Temperature.
    if (Grouping == "Mode") {
      data_subset <- data_subset %>% mutate(Group = factor(Mode))
    } else {
      data_subset <- data_subset %>% mutate(Group = factor(Temp))
    }

    # Check for sufficient data: need at least 2 groups with at least 3 observations each
    # (pb2gen requires at least 2 observations per group, we use 3 for robustness)
    group_counts <- data_subset %>% count(Group)
    n_groups <- nrow(group_counts)
    min_per_group <- if (nrow(group_counts) > 0) min(group_counts$n) else 0

    if (n_groups < 2) {
      message(sprintf("  Skipping %s / %s: fewer than 2 groups available", PUT, Fix))
      return(tibble(
        PUT = PUT, Fix = Fix, Compare = Compare,
        DiffPct = NA_real_, CI_Low = NA_real_, CI_High = NA_real_,
        P_Value = NA_real_, CliffDelta = NA_real_,
        Skipped = TRUE, SkipReason = "fewer than 2 groups"
      ))
    }

    if (min_per_group < 3) {
      message(sprintf("  Skipping %s / %s: insufficient observations per group (min=%d, need>=3)",
                      PUT, Fix, min_per_group))
      return(tibble(
        PUT = PUT, Fix = Fix, Compare = Compare,
        DiffPct = NA_real_, CI_Low = NA_real_, CI_High = NA_real_,
        P_Value = NA_real_, CliffDelta = NA_real_,
        Skipped = TRUE, SkipReason = sprintf("insufficient observations (min=%d)", min_per_group)
      ))
    }

    # Attempt bootstrap - wrap in tryCatch for robustness
    result <- tryCatch({
      # Bootstrap medians with fixed seed to stabilize CIs across runs.
      set.seed(100)
      pb <- WRS2::pb2gen(ScorePct ~ Group, data = data_subset, est = "median", nboot = nboot)

      # Cliff's delta quantifies stochastic dominance (nonparametric effect size).
      set.seed(100)
      delta <- effsize::cliff.delta(ScorePct ~ Group, data = data_subset)

      tibble(
        PUT = PUT,
        Fix = Fix,
        Compare = Compare,
        DiffPct = as.numeric(pb$test),     # median(Group A) - median(Group B)
        CI_Low = pb$conf.int[1],           # 95% percentile CI
        CI_High = pb$conf.int[2],
        P_Value = pb$p.value,              # raw p from bootstrap test
        CliffDelta = as.numeric(delta$estimate),
        Skipped = FALSE,
        SkipReason = NA_character_
      )
    }, error = function(e) {
      message(sprintf("  Error in %s / %s: %s", PUT, Fix, conditionMessage(e)))
      tibble(
        PUT = PUT, Fix = Fix, Compare = Compare,
        DiffPct = NA_real_, CI_Low = NA_real_, CI_High = NA_real_,
        P_Value = NA_real_, CliffDelta = NA_real_,
        Skipped = TRUE, SkipReason = sprintf("error: %s", conditionMessage(e))
      )
    })

    result
  })

  # If no results, return empty tibble with proper structure
if (nrow(results) == 0) {
    return(tibble(
      PUT = character(), Fix = character(), Compare = character(),
      DiffPct = numeric(), CI_Low = numeric(), CI_High = numeric(),
      P_Value = numeric(), CliffDelta = numeric(),
      P_Adjusted = numeric(), Significant = logical(),
      Skipped = logical(), SkipReason = character()
    ))
  }

  # Control family-wise error within each PUT (4 tests) via Holm step-down
  # Apply Holm step-down within each PUT (S. Holm, 1979), then flag significance.
  # Only adjust p-values for non-skipped comparisons
  results %>%
    group_by(PUT) %>%
    mutate(
      P_Adjusted = ifelse(Skipped, NA_real_, p.adjust(P_Value, method = "holm")),
      Significant = ifelse(Skipped, NA, P_Adjusted < alpha)
    ) %>%
    ungroup()
}

# -----------------------------------------------------------------------------
# Shapiro-Wilk tests per (PUT x Mode x Temp) ("Distribution Analysis").
# Add formatted display columns for LaTeX/JSON.
# NOTE: With highly discrete score distributions (e.g., M01/Completions/T=0 has
# only two distinct values: 21/22 and 20/22), p-values may underflow to 0,
# which we handle at rendering time ("< 1e-6") to avoid "impossible zeros".
# Shapiro-Wilk requires at least 3 observations; groups with fewer are skipped.
# -----------------------------------------------------------------------------
shapiro_results <- function(llm_df) {
  llm_df %>%
    group_by(PUT, Mode, Temp) %>%
    summarise(
      N = n(),
      W = if (n() >= 3) {
        tryCatch(unname(shapiro.test(ScorePct)$statistic), error = function(e) NA_real_)
      } else {
        NA_real_
      },
      P_Value = if (n() >= 3) {
        tryCatch(shapiro.test(ScorePct)$p.value, error = function(e) NA_real_)
      } else {
        NA_real_
      },
      Skipped = n() < 3,
      SkipReason = if (n() < 3) sprintf("insufficient observations (n=%d, need>=3)", n()) else NA_character_,
      .groups = "drop"
    ) %>%
    mutate(
      P_Value_Display = format_p_value(P_Value, style = "plain"),
      W_Display = ifelse(is.na(W), "--", format_w_stat(W))
    )
}

# -----------------------------------------------------------------------------
# Write JSON and the LaTeX table body for the Shapiro-Wilk table (user-friendly to \input in LaTeX).
# - digits=6 preserves precise comparisons while keeping file sizes reasonable.
# -----------------------------------------------------------------------------
write_outputs <- function(summary_tbl, effects_tbl, shapiro_tbl, alpha, generate_tex = TRUE) {
  if (generate_tex) {
    write_shapiro_tex(shapiro_tbl, alpha = alpha)
  }

  # Consolidate all JSON outputs into one structured object
  combined_output <- list(
    summary = summary_tbl,
    effects = effects_tbl,
    shapiro = shapiro_tbl
  )

  write_json(
    combined_output,
    path = "statistical_analysis.json",
    pretty = TRUE,
    auto_unbox = TRUE,
    digits = 6
  )
}

# ---- Main -----------------------------------------------------------------
# Load data (within-PUT design; see "Evaluation Protocol")
# and includes baselines for the summary but not for effect-size tests.
llm_df <- load_llm_data(dataset_path)
baseline_df <- load_baseline_data("baseline.csv")

summary_tbl <- median_summary(llm_df, baseline_df)
effects_tbl <- effect_comparisons(llm_df, nboot = nboot, alpha = alpha)
shapiro_tbl <- shapiro_results(llm_df)

write_outputs(summary_tbl, effects_tbl, shapiro_tbl, alpha = alpha, generate_tex = generate_shapiro_tex)

# Summary report
n_effects_ok <- sum(!effects_tbl$Skipped, na.rm = TRUE)
n_effects_skipped <- sum(effects_tbl$Skipped, na.rm = TRUE)
n_shapiro_ok <- sum(!shapiro_tbl$Skipped, na.rm = TRUE)
n_shapiro_skipped <- sum(shapiro_tbl$Skipped, na.rm = TRUE)

message(sprintf("Analysis complete. Results written to statistical_analysis.json."))
message(sprintf("  Effect comparisons: %d completed, %d skipped", n_effects_ok, n_effects_skipped))
message(sprintf("  Shapiro-Wilk tests: %d completed, %d skipped", n_shapiro_ok, n_shapiro_skipped))
