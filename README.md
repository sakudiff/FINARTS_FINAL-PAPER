# Risk-Off Shocks and Spillovers in Safe Havens, Replication and Extension

Replication of Beirne and Sugandi (2023), "Risk-off Shocks and Spillovers in
Safe Havens," *Pacific-Basin Finance Journal*, Vol. 80, 102103. Country-specific
structural vector autoregression for Japan, extended from the paper's 1999–2021
sample through June 2026. Two-tier estimation with a dual-vintage data policy.

Group 4, FINARTS C01, De La Salle University, Academic Year 2025–2026 Term 3.
Submitted August 7, 2026 to Dr. Ray Anthony Almonares.

| Link | URL |
|------|-----|
| Paper | [main.pdf](main.pdf) |
| Report | https://finalprojectfinartsg4.netlify.app |
| Repository | https://github.com/sakudiff/FINARTS_FINAL-PAPER |

## Group members

| Member | Role |
|--------|------|
| Aaron Joshua Sison | Data handling, retrieval, processing, methodology, coding, results, lead |
| Enrique Lorenzo Galedo | Review of related literature |
| Aimee Lorynne Opiana | Introduction |
| Raphael Cuenca | Data handling, retrieval, processing, methodology, coding, results |
| Keira Ley Go | Data handling, retrieval, processing, methodology, coding, results |

## Quick start

```bash
uv sync
uv run python scripts/replicate_svar.py          # full pipeline (~4 min)
uv run python scripts/replicate_svar.py --verify # checks against committed references
quarto render data_pipeline.qmd                   # rebuilds index.html
```

With daily confidence bands

```bash
uv run python scripts/replicate_svar.py --with-daily-ci --repl 1000
```

## Their methods vs our methods

| Aspect | Paper | This replication |
|--------|-------|-----------------|
| Frequency | Daily (baseline), monthly (appendix) | Daily (Tier 1), monthly (Tier 2) |
| Model | Restricted VAR (block exogeneity) | Restricted (Tier 1) and unrestricted (Tier 2) |
| Lag selection | AIC (maxlags unreported) | AIC (Tier 1), BIC (Tier 2, AIC overfits to boundary) |
| Identification | Cholesky, risk-off first | Same ordering |
| Interpolation | EViews quadratic (settings unreported) | Python quadratic-match average reimplementation |
| Capital flows | IMF IFS quarterly BOP | BOJ BPM6 monthly (BPM6-equivalent, directly comparable) |
| Data vintage | Mid-2021 downloads | ALFRED 2021-06-01 vintage GDP, Wayback 2021-05-24 BIS REER |
| Software | EViews (inferred from figure styling) | Python (statsmodels + custom OLS) |
| Sample | 1999-01-14 to 2021-03-31 | Same, extended through 2026-06-30 |

## What matches and what does not

| Variable | Paper finding | Replication | Verdict |
|----------|--------------|-------------|---------|
| RGDP (monthly restricted, vintage data) | Negative, persistent, trough ~-0.002 | Negative, persistent, trough -0.00398 at h=3, sig through h=6 | MATCH |
| RGDP (daily restricted, vintage data) | Negative, sig through ~125 days | Negative, sig at every horizon h=1–125 | MATCH |
| RGDP (extended period) | Not applicable | Near-zero, not significant | Weakening |
| REER | Appreciation (positive) | Positive in all specs | MATCH |
| Spread | Widening (positive) | Positive in all specs | MATCH |
| Nikkei | Immediate positive, then negative | Negative from h=0 in every spec | PARTIAL |
| WUI | Smooth positive, then negative | Negative daily trough, positive monthly peak, sign unstable across frequencies | MISMATCH |
| Capital flows | Insignificant | Mostly insignificant, 2 significant cells (direct_pct h=3) | MATCH |
| Risk-off episodes | Fifteen in-sample dates in Table 1 | All fifteen reproduced exactly | MATCH |
| Restricted vs unrestricted | Paper reports both forms, no consistency claim | Diverge on current-vintage data | PARTIAL |

## What the paper did not disclose

| Detail | Implication |
|--------|------------|
| Exact lag count and AIC search ceiling | AIC always hits the boundary on our data. BIC adopted for monthly tier |
| EViews interpolation variant (average vs sum vs point) | Different variants produce meaningfully different daily paths |
| Monthly risk-off aggregation method | Tested sum, binary, and proportion. Proportion chosen for correct signs |
| Confidence interval method | Replaced with Monte Carlo delta method (restricted) and asymptotic bands (unrestricted) |
| Software | Figure styling suggests EViews. Pipeline uses Python and statsmodels |
| GDP data source vintage | 3.5–6.3% revision over 2019–2021 requires vintage data for replication |

## Why each decision was made

| Decision | Rationale | Paper's approach |
|----------|----------|------------------|
| Monthly frequency for Tier 2 | Daily VAR on interpolated quarterly GDP showed wrong RGDP sign | Daily baseline with monthly robustness |
| BIC instead of AIC for monthly | AIC consistently selected boundary lag at every tested cap | Stated AIC, did not report cap |
| Unrestricted as baseline for monthly | Restricted model failed on current-vintage RGDP (vintage substitution confirmed revision sensitivity) | Both restricted and unrestricted, claimed consistency |
| Proportion risk-off aggregation | Sum inflated shock SD to 2.23, binary gave wrong RGDP sign | Not specified |
| Dual-vintage data policy | Post-2022 GDP benchmark revisions changed RGDP sign. BIS REER retroactively rebased | Used current data at time of writing |
| BOJ instead of IMF capital flows | IMF IFS republishes BOJ/MOF data under BPM6. Directly comparable | IMF IFS quarterly BOP |

## Replication fidelity

Five code defects were identified and corrected. An IRF recursion transpose swapped
the effect of risk-off on RGDP with the effect of RGDP on risk-off. A plot
indexing error displayed the wrong variable responses. A missing constant term
omitted the intercept the paper's model includes. Flat confidence bands used
residual standard errors instead of propagating parameter uncertainty through
the IRF horizon. A coefficient-storage bug in the restricted VAR misplaced
own-lag coefficients of the risk-off equation into cross-variable slots.

After correction, the core findings reproduce in both tiers. The paper's RGDP
sign, spread widening, and REER appreciation are replicated. The Nikkei
immediate-positive impact effect is not reproduced. The daily RGDP trough is
deeper than the paper's charts (-0.00074 versus -0.0006 at day 45-50), and the
monthly trough is approximately twice as deep (-0.004 versus -0.002). The
restricted and unrestricted specifications diverge on current-vintage
data. This divergence is presented as a finding about sensitivity to GDP
data revisions rather than a failure of either specification.

## Limitations

The paper's EViews interpolation settings are unreported. The BIS REER
vintage relies on a single Wayback Machine snapshot. The paper states the
WUI is monthly, but the dataset begins January 2008 (available in the repo as
`data/raw/WUI_M_dataset_2026_05.xlsx`). Quarterly WUI is the
defensible source. BOJ capital flows are higher frequency than the paper's
IMF series, introducing variation the paper's VAR would not have seen.
The monthly tier uses BIC for lag selection where the paper states AIC.
The unrestricted CIs use asymptotic bands rather than Monte Carlo. The
pipeline is in Python. The paper almost certainly used EViews. Cross-platform
BLAS and LAPACK differences produce small numerical variations in coefficient
estimates and Monte Carlo bands between x86 and ARM machines.

## CLI reference

| Flag | Description |
|------|-------------|
| *(default)* | Full two-tier pipeline |
| `--with-daily-ci` | Daily restricted Monte Carlo confidence bands |
| `--repl N` | Bootstrap replications (default 1000) |
| `--verify` | Rerun pipeline, compare against committed git references |
| `--fetch-vintage-gdp` | Download vintage GDP from ALFRED |
| `--fetch-vintage-reer` | Download vintage REER from Wayback Machine |
| `--interpolate-v1` | Regenerate v1 daily CSVs (called by the QMD) |

## Repository layout

```
finarts-final-paper/
├── main.tex                           # LaTeX manuscript root
├── main.pdf                           # Compiled paper (77 pages)
├── chapters/                          # LaTeX manuscript sections (00-06)
├── guidelines.md                      # Course project guidelines summary
├── data_pipeline.qmd                  # Quarto document: data construction, narrative, and results
├── index.html                         # Rendered HTML (hosted via Netlify)
├── README.md                          # This file
├── LICENSE                            # MIT license
├── netlify.toml                       # Netlify deployment configuration
├── pyproject.toml                     # Python project metadata and dependencies
├── uv.lock                            # Deterministic dependency lock file
├── references.bib                     # BibTeX references
├── dlsu_logo.png                      # Title page logo
├── .gitignore
├── articles/                          # Reference PDFs and paper full-text markdown
│   ├── Beirne_Sugandi_2023.pdf
│   ├── Beirne_Sugandi_2023.md
│   └── Japan brands yen falls as speculative as Iran war ignites sell-off By Reuters.pdf
├── scripts/
│   └── replicate_svar.py              # Unified A-Z replication pipeline
├── data/
│   ├── raw/                           # Raw input data (15 files)
│   │   ├── VIX.csv                    # CBOE Volatility Index (daily)
│   │   ├── NIKKEI225.csv              # Nikkei 225 index (daily)
│   │   ├── US10Y.csv                  # US 10-year Treasury yield (daily)
│   │   ├── USDJPY.csv                 # USD/JPY exchange rate (daily)
│   │   ├── jgbcme_all.csv             # JGB yield curve (daily)
│   │   ├── REER.xlsx                  # BIS broad real effective exchange rate (monthly)
│   │   ├── JAPAN_RGDP.csv             # Japan real GDP (quarterly, FRED JPNRGDPEXP)
│   │   ├── JAPAN_NOMINAL_GDP.csv      # Japan nominal GDP (quarterly, FRED)
│   │   ├── WUI_JPN.csv                # World Uncertainty Index for Japan (quarterly)
│   │   ├── BOJ_6pi-1_portfolio_summary.csv  # BOJ portfolio investment (pre-2014)
│   │   ├── BOJ_BPPI6E3N5.csv          # BOJ long-term debt securities (post-2014)
│   │   ├── BOJ_BPPI6E4N5.csv          # BOJ short-term debt securities (post-2014)
│   │   ├── BOJ_BPPI6E2N5.csv          # BOJ equity securities (post-2014)
│   │   ├── BOJ_BPBP6JYNFL3.csv        # BOJ other investment (post-2014)
│   │   ├── BOJ_BPBP6JYNFL13.csv       # BOJ direct investment (post-2014)
│   │   └── vintage/                   # Period-appropriate data vintages
│   │       ├── JPNRGDPEXP_vintage_2021-06-01.csv   # ALFRED vintage GDP
│   │       └── REER_JPN_BIS_vintage.csv            # Wayback Machine BIS REER snapshot
│   ├── processed/
│   │   ├── final_dataset.csv          # Daily panel of all 10 endogenous variables (1999-2026)
│   │   ├── descriptive_stats.csv      # Variable descriptive statistics
│   │   └── var_results/               # Estimation outputs
│   │       ├── twotier/               # Two-tier final IRF results (8 CSV files)
│   │       │   ├── daily_paper_irf.csv
│   │       │   ├── daily_extended_irf.csv
│   │       │   ├── monthly_paper_restricted_irf.csv
│   │       │   ├── monthly_paper_unrestricted_irf.csv
│   │       │   ├── monthly_extended_restricted_irf.csv
│   │       │   ├── monthly_extended_unrestricted_irf.csv
│   │       │   ├── comparison_paper_vs_extended.csv
│   │       │   └── flow_significance.csv
│   │       ├── adf_tests_1999_2021.csv
│   │       ├── adf_tests_1999_2026.csv
│   │       ├── lag_selection_1999_2021.csv
│   │       ├── lag_selection_1999_2026.csv
│   │       └── figures/               # Generated figures (21 PNG files)
│   │           ├── stylized_*_risk_off.png     # Stylized facts panels (11)
│   │           ├── irf_grid_*.png              # Impulse response grids (8)
│   │           └── infographics_*.png          # ADF and lag diagnostics (2)
│   └── tmp_quadratic/                 # Interpolation intermediates
│       ├── *_native.csv               # Native-frequency series (7 files, QMD output)
│       ├── *_daily.csv                # Pandas-spline daily interpolation (7 files, QMD+v1 output)
│       └── v2/                        # Quadratic-match daily interpolation (7 files, Python output)
│           └── *_qdmatch.csv
├── docs/
│   └── methodology_dual_vintage.md     # Dual-vintage data policy with citations
├── guidelines/                         # Course project guidelines and journal ranking
│   ├── FINARTS - Term Project Details - AY2526 T3.pdf
│   ├── FINARTS - Progress Update Details - AY2526 T3.pdf
│   └── ABDC-JQL-2025-v2-270526.xlsx
└── drafts/                             # Regenerable LaTeX table sources (QMD outputs)
```

## Configuration

The pipeline runs on Python 3.10 or newer, managed with `uv`. The estimation
uses a dual-vintage data policy. The paper period, 14 January 1999 to 31 March
2021, uses the ALFRED 2021-06-01 GDP vintage and the Wayback Machine BIS REER
snapshot of 24 May 2021. The extended period, through 30 June 2026, uses
current-vintage data. The policy is documented in
`docs/methodology_dual_vintage.md`.

## Contributing

This repository is a course replication project. Forks are welcome for
verification and extension. Pull requests that reproduce or extend the
analysis are reviewed on a best-effort basis. For questions about the
replication, open an issue in the repository.

## License

MIT. See the `LICENSE` file.

## Citation

Beirne, J. and Sugandi, E. (2023). Risk-off shocks and spillovers in safe
havens. *Pacific-Basin Finance Journal*, 80, 102103.

To cite this replication, Sison, A. J., Galedo, E. L., Opiana, A. L., Cuenca,
R., and Go, K. L. (2026). Risk-off shocks and spillovers in safe havens,
replication and extension [Manuscript and code]. De La Salle University.
https://github.com/sakudiff/FINARTS_FINAL-PAPER
