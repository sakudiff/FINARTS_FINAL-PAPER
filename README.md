# Beirne & Sugandi (2023) Replication — Japan SVAR

Replication and extension of Beirne & Sugandi (2023), *Risk-off shocks and
spillovers in safe havens*, Pacific-Basin Finance Journal 80, 102102.
The project extends the original 1999–2021 sample to June 2026, applying
a recursively restricted structural VAR with Cholesky decomposition to
Japanese data. A two-tier daily/monthly design uses quadratic-match-average
interpolation (EViews-equivalent) and a dual-vintage policy: vintage GDP
and REER for the paper period, current-vintage data for the extension.
All results are documented in the rendered HTML report.

## Repository Layout

```
data/
  raw/                   — Raw source files (LSEG, FRED, BOJ API, BIS)
  raw/vintage/           — Vintage RGDP and REER snapshots
  processed/
    final_dataset.csv    — Daily aligned dataset (built by pipeline)
    descriptive_stats.csv
    var_results/
      twotier/           — Canonical IRF outputs (8 CSV files)
      figures/           — Risk-off episode charts (10 PNG files)
      adf_tests_*.csv
      lag_selection_*.csv
  tmp_quadratic/         — Native and quadratic-match interpolation cache
    v2/                  — Mean-preserving qdmatch files for VAR
scripts/
  replicate_svar.py      — Unified two-tier pipeline (self-contained)
  fetch_alfred_vintage.py
  fetch_reer_vintage.py
drafts/                  — LaTeX tables and presentation materials
docs/
  methodology_dual_vintage.md
articles/                — Reference PDFs
guidelines/              — Course requirements and ABDC journal list
references.bib
data_pipeline.qmd        — Quarto document (narrative + code)
index.html               — Rendered report
netlify.toml
pyproject.toml
uv.lock
```

## Professor Replication Instructions

All commands run from the repo root with `uv` (Python package manager).

### (a) Install dependencies

```
uv sync
```

### (b) Run the full two-tier pipeline

```
uv run python scripts/replicate_svar.py
```

This runs the complete pipeline: quadratic-match interpolation, daily
restricted VAR with AIC-selected lag, monthly restricted and unrestricted
VAR with BIC-selected lags, Monte Carlo confidence intervals (1000
replications), and flow significance tests. Expected runtime ~4 minutes.

### (c) Verify against committed reference outputs

```
uv run python scripts/replicate_svar.py --verify
```

Reference CSVs were generated on Linux x86. Monte Carlo confidence bands
and AIC/BIC values are machine-dependent due to BLAS/LAPACK differences
across platforms (ARM vs x86). Response/point-estimate columns and
deterministic CIs match at machine precision on all platforms; MC-based
CI columns may show non-zero diffs on different hardware. The qualitative
results — signs, significance, and magnitude order — are invariant.

### (d, optional) Quarto HTML report

```
quarto render data_pipeline.qmd
```

Generates `index.html` with the full narrative, tables, and figures.
The Quarto pipeline calls `replicate_svar.py --interpolate-v1`
for the initial pandas-spline interpolation step.

### (e, optional) Daily confidence bands

Add `--with-daily-ci` to any run of `replicate_svar.py`:

```
uv run python scripts/replicate_svar.py --with-daily-ci
```

Computes Monte Carlo confidence intervals for the daily restricted
VAR (1000 replications by default). Expected runtime increases
from ~4 minutes to ~25 minutes.

### (d) Build the HTML report (optional)

```
quarto render data_pipeline.qmd
```

Generates `index.html` with the full narrative, tables, and figures.

## Data

All raw data is in `data/raw/`:

- **VIX, Nikkei 225, US 10Y, USD/JPY** — LSEG Workspace (daily)
- **Japan 10Y JGB** — Japan Bond Trading Co., via `jgbcme_all.csv`
- **REER** — BIS (monthly, via Datastream)
- **Real GDP, Nominal GDP** — FRED (quarterly)
- **World Uncertainty Index** — `worlduncertaintyindex.com` (quarterly)
- **Capital flows** — Bank of Japan API and historical CSV (monthly)

The dual-vintage policy (vintage GDP/REER for the paper period,
current-vintage for the extension) is documented in
`docs/methodology_dual_vintage.md`. All flow variables are converted to
percent of nominal GDP using USD/JPY exchange rates.

## Results

All canonical IRF outputs reside in `data/processed/var_results/twotier/`.
The rendered report is hosted at the repository's Netlify URL and also
available locally as `index.html` after running `quarto render`.
