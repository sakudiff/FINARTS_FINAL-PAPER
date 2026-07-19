# SVAR Analysis — Context Handoff

> Generated 2026-07-19. Update this file as work progresses.

## What This Implements

The SVAR analysis from `docs/grill-me-svar-implementation/SPEC.md` — replicating
Beirne & Sugandi (2023) restricted and unrestricted VAR models on two periods
(1999-2021 and 1999-2026) with analytical and bootstrap confidence intervals.

## Key Files

| File | Purpose |
|------|---------|
| `scripts/var_analysis.py` | Main SVAR analysis script. Run with `uv run python scripts/var_analysis.py` |
| `docs/grill-me-svar-implementation/SPEC.md` | Full implementation spec from grill-me |
| `docs/grill-me-svar-implementation/DISCLOSURE_BLOCKS.md` | Clarity Writer disclosure blocks for QMD integration |
| `data_pipeline.qmd` | The QMD file that needs VAR analysis chunks appended |
| `data/processed/var_results/` | All output files (figures, tables, CSVs) |

## Complete Outputs (as of 2026-07-19)

### Period 1: 1999-2021

| Output | File | Status |
|--------|------|--------|
| ADF tests | `adf_tests_1999_2021.csv` | Done |
| Lag selection (AIC) | `lag_selection_1999_2021.csv` | Done (selected lag=20) |
| Restricted VAR analytical IRF | `irf_restricted_1999_2021_analytical.png` | Done |
| Restricted VAR bootstrap IRF | `irf_restricted_1999_2021_bootstrap.png` | Done |
| Restricted VAR CI comparison | `irf_restricted_1999_2021_ci_comparison.png` | Done |
| Unrestricted VAR analytical IRF | `irf_unrestricted_1999_2021_analytical.png` | Done |
| Unrestricted VAR bootstrap IRF | `irf_unrestricted_1999_2021_bootstrap.png` | Done |
| Unrestricted VAR CI comparison | `irf_unrestricted_1999_2021_ci_comparison.png` | Done |
| Restricted FEVD | `fevd_restricted_1999_2021.csv` | Done |
| Unrestricted FEVD | `fevd_unrestricted_1999_2021.csv` | Done |
| IRF peaks (restricted) | `irf_peak_restricted_1999_2021.csv` | Done |
| IRF peaks (unrestricted) | `irf_peak_unrestricted_1999_2021.csv` | Done |

### Period 2: 1999-2026

| Output | File | Status |
|--------|------|--------|
| ADF tests | `adf_tests_1999_2026.csv` | Done |
| Lag selection (AIC) | `lag_selection_1999_2026.csv` | Done (selected lag=20) |
| Restricted VAR analytical IRF | `irf_restricted_1999_2026_analytical.png` | Done |
| Restricted VAR bootstrap IRF | `irf_restricted_1999_2026_bootstrap.png` | **Pending** |
| Restricted VAR CI comparison | `irf_restricted_1999_2026_ci_comparison.png` | **Pending** |
| Unrestricted VAR analytical IRF | `irf_unrestricted_1999_2026_analytical.png` | Done |
| Unrestricted VAR bootstrap IRF | `irf_unrestricted_1999_2026_bootstrap.png` | **Pending** |
| Unrestricted VAR CI comparison | `irf_unrestricted_1999_2026_ci_comparison.png` | **Pending** |
| Restricted FEVD | `fevd_restricted_1999_2026.csv` | Done |
| Unrestricted FEVD | `fevd_unrestricted_1999_2026.csv` | Done |
| IRF peaks (restricted) | `irf_peak_restricted_1999_2026.csv` | Done |
| IRF peaks (unrestricted) | `irf_peak_unrestricted_1999_2026.csv` | Done |

### Cross-Period

| Output | File | Status |
|--------|------|--------|
| Restricted period comparison | `irf_period_comparison_restricted.png` | Done |

## Key Findings So Far

### Stationarity (ADF at 5%)
- **Stationary**: risk_off, log_wui, debtsec_pct, equity_pct, other_pct, direct_pct
- **Non-stationary**: spread, log_rgdp, log_reer, log_nikkei — contradicts paper claim

### Lag Selection
- Both periods: AIC selects **lag 20** (the search boundary)
- AIC values decrease monotonically through lag 20, suggesting the true optimum may exceed 20

## What to Run Next

On the Mac Mini:

```bash
cd /path/to/FINARTS_FINAL-PAPER
uv run python scripts/var_analysis.py
```

This will regenerate all outputs (overwriting existing files) and fill in the 4
missing Period 2 bootstrap figures. Takes approximately 5-15 minutes depending on
CPU.

## QMD Integration Pending

The `data_pipeline.qmd` still needs the disclosure blocks + execution calls appended
after the `latex-table` chunk. The disclosure text is in
`docs/grill-me-svar-implementation/DISCLOSURE_BLOCKS.md` and needs to be adapted into
the QMD as markdown before each chunk call.

## Architecture Note

The script delegates to `var_analysis.py` via `system2("uv", c("run", "scripts/var_analysis.py"))`
from an R chunk in the QMD (same pattern as the existing quadratic interpolation call).
This avoids reticulate dependency issues.
