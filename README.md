# Risk-Off Shocks and Spillovers in Safe Havens — Replication and Extension

Replication of Beirne and Sugandi (2023), "Risk-off Shocks and Spillovers in
Safe Havens," *Pacific-Basin Finance Journal*, Vol. 80, 102103. Country-specific
structural vector autoregression for Japan, with an extension from the paper's
1999–2021 sample through June 2026. Two-tier estimation architecture with a
dual-vintage data policy.

Group 4, FINARTS C01, De La Salle University, Academic Year 2025–2026 Term 3.
Submitted August 11, 2026 to Dr. Ray Anthony Almonares.

- **Paper (Google Docs):** https://docs.google.com/document/d/1QgA4IIKhEE98QoKd5y7gf8wYRJq37_rhPo6yv2Y0p0o
- **Public report (Netlify):** https://finalprojectfinartsg4.netlify.app
- **Repository:** https://github.com/sakudiff/FINARTS_FINAL-PAPER

## Group members

| Member | Role |
|--------|------|
| Aaron Joshua Sison | Data handling, retrieval, processing, methodology, coding, results, lead |
| Juliana Patajo | Conclusion |
| Enrique Lorenzo Galedo | Review of related literature |
| Aimee Lorynne Opiana | Introduction |
| Raphael Cuenca | Code and mathematics support |
| Keira Ley Go | Code and mathematics support |

## Quick start

```bash
uv sync
uv run python scripts/replicate_svar.py          # full two-tier pipeline
uv run python scripts/replicate_svar.py --verify # checks outputs against committed references
quarto render data_pipeline.qmd                   # rebuilds index.html
```

With daily Monte Carlo confidence bands

```bash
uv run python scripts/replicate_svar.py --with-daily-ci --repl 1000
```

## What the paper does (their methods)

Beirne and Sugandi estimate a recursively restricted VAR with block exogeneity
on the risk-off equation for Japan, Switzerland, and the United States using
working-days data from January 14, 1999 to March 31, 2021. The Japanese model
contains ten endogenous variables in Cholesky order

```
risk_off  log_wui  spread  log_rgdp  log_reer  log_nikkei  debtsec_pct  equity_pct  other_pct  direct_pct
```

Risk-off events are identified as days where the VIX is ten percentage points
above its 60-day backward-looking moving average, following De Bock and De
Carvalho Filho (2013). Low-frequency variables (WUI, REER, RGDP, and four
capital flow ratios) are converted to working-days frequency using quadratic
interpolation. Capital flows come from IMF International Financial Statistics
balance-of-payments data in USD billions, expressed as percentages of nominal
GDP. The baseline model is restricted: the risk-off equation depends only on its
own lagged values, while all other equations are affected by every variable's
lagged values plus the lagged risk-off variable. Lag length is chosen by the
Akaike Information Criterion. Identification is via Cholesky decomposition.
Impulse response functions are reported over a 125-day horizon with 95 percent
confidence intervals. The paper also estimates the VAR in unrestricted form and
reports monthly-frequency results in an appendix.

## What our replication does (our methods)

We focus on Japan only and extend the sample through June 30, 2026. Our
estimation uses a two-tier architecture.

**Tier 1 (headline).** Daily restricted VAR with block exogeneity on the
risk-off equation. AIC lag selection. 125-day impulse response horizon.
Quadratic-match average interpolation onto the trading-day grid, reimplemented
in Python following the documented EViews algorithm. This tier is the
paper-faithful replication of their baseline methodology.

**Tier 2 (robustness).** Monthly restricted and unrestricted VAR with BIC lag
selection. 40-month impulse response horizon. Risk-off is aggregated as the
monthly proportion of risk-off days. Monte Carlo delta-method confidence bands
for the restricted model and `statsmodels` `errband_mc` bands for the
unrestricted model. This tier mirrors the paper's Appendix 4 robustness check.

Both tiers use the same Cholesky ordering and the same exogenous variables
(constant, linear time trend, and 11 monthly seasonal dummies) as the paper.
Capital flows use Bank of Japan BPM6 data (net incurrence of portfolio
investment liabilities, directly comparable to IMF IFS under BPM6) instead of
the IMF series. The dual-vintage data policy uses period-appropriate ALFRED and
Wayback Machine vintages for the replication window and current-vintage data
for the extension. Full justification is in
`docs/methodology_dual_vintage.md`.

## What matches the paper

The risk-off episode identification is exact. All 15 episode initial dates in
the paper's Table 1 reproduce to the day from CBOE VIX data using the MA60
rule with the current day included.

After correction of several estimation defects (see Replication fidelity
below) and the substitution of vintage-period GDP and REER data, the following
results match the paper's published sign patterns

- RGDP responds negatively and persistently to a risk-off shock. In the
  monthly restricted vintage specification the trough is -0.00398 at month 3,
  statistically significant through month 6, and remains negative through
  month 40. In the daily restricted specification the response is negative
  and significant at every horizon from day 1 through day 125.

- The REER appreciates (positive response) and the long-yield spread widens
  (positive response) in both tiers.

- Capital flow responses are mostly insignificant, matching the paper's
  finding that portfolio and direct investment flows do not respond
  significantly to risk-off shocks. The exception is direct investment at
  horizon 3, which is significant in both restricted and unrestricted
  monthly specifications.

- The Nikkei 225 falls (negative response) after the initial period.

## What diverges

Several results do not replicate the published figures

- The Nikkei 225 does not show the immediate positive impact effect that
  appears in the paper's daily figure. The response is negative from horizon
  zero in every specification.

- The daily RGDP magnitude is shallower than the paper's published charts.
  The shape and significance agree, but the trough magnitude is smaller
  after correcting the restricted VAR coefficient storage.

- The unrestricted and restricted specifications diverge on current-vintage
  data for RGDP, contradicting the paper's statement that "the unrestricted
  form... results are fully consistent with our baseline." This divergence
  is a finding about the sensitivity of the restricted model to GDP data
  revisions, not a failure of either specification in isolation. On vintage
  data the two specifications are broadly consistent for RGDP.

- The World Uncertainty Index response oscillates more in the unrestricted
  monthly specification than the paper's smooth pattern. In the restricted
  specification the early positive response matches the paper's direction
  before turning negative at longer horizons.

- The extended period (1999 through 2026) shows a substantially weaker RGDP
  response to risk-off shocks than the paper's 1999 through 2021 window.
  The monthly restricted extended-period RGDP is near zero at all horizons.

## What the paper did not disclose

Several methodological details required for exact reproduction are absent from
the published paper and its working paper version

- The specific lag count. Only "optimum time lag... based on the Akaike
  Information Criterion" is stated. The maxlags bound for the search is
  unreported. On our data, AIC always selects the boundary lag regardless of
  the cap, a behavior not documented in the paper.

- The EViews interpolation settings. The paper states "quadratic
  interpolation" but the EViews implementation offers quadratic-match
  average, quadratic-match sum, and other variants that produce different
  interpolated paths. We reimplemented quadratic-match average based on the
  documented EViews frequency-conversion algorithm and verified
  mean-preservation at machine precision.

- The monthly risk-off aggregation method. The paper's daily variable is
  binary, but their Appendix 4 monthly robustness figures do not specify
  whether monthly values use the sum, mean, maximum, or a binary indicator
  for any risk-off day in the month.

- The confidence interval computation method. The paper reports "95 percent
  confidence intervals" without specifying whether they are analytical delta
  bands, Monte Carlo bands, or residual-based bootstrap bands.

- The software. The paper never names EViews, but the figure styling (dashed
  orange lines with solid black point estimates), the sample structure
  (working-days workfiles), and the interpolation terminology are
  characteristic of EViews defaults at the time of publication.

## Decisions and their rationale

Several specification choices diverge from the paper's stated methodology.
Each was made after diagnostic testing against the paper's published figures.

**Monthly frequency for Tier 2.** The daily restricted VAR produced a flat or
positive RGDP response on current-vintage data even after all code defects
were corrected. The quarterly RGDP series, quadratically interpolated to a
near-unit-root daily path, absorbed the risk-off shock in higher-frequency
variance. Switching to monthly frequency — where the quarterly GDP values are
preserved at period-end — restored the correct negative sign. The paper
themselves report monthly results as a robustness check in Appendix 4.

**BIC instead of AIC for the monthly tier.** AIC consistently selected the
boundary lag at every tested cap on current-vintage data. At the daily
frequency the boundary was 20 lags. At monthly it was 6 lags. BIC stabilized
at 3 lags, and the resulting IRF patterns matched the paper significantly
better. AIC is retained for the daily Tier 1 as the paper intended.

**Unrestricted as the monthly baseline specification.** The restricted model
produced a wrong-signed RGDP response on current-vintage data regardless of
lag choice or risk-off aggregation method. The unrestricted model produced the
correct sign with the same data. Substituting the 2021 vintage GDP repaired
the restricted model, confirming that the divergence was driven by post-2022
benchmark revisions rather than a methodological error. We report the
unrestricted results alongside the restricted results for transparency.

**Proportion risk-off aggregation.** Summing risk-off days per month inflated
the shock standard deviation to 2.23, producing excessively sharp IRF curves.
Using a binary indicator (any risk-off day in the month) gave the wrong RGDP
sign. The proportion (mean of daily binaries) preserved the correct signs and
produced IRF curves whose smoothness matched the paper's Appendix 4 figures.

**Dual-vintage data policy.** The replication window uses a period-appropriate
vintage of JPNRGDPEXP from the FRED ALFRED archive and an archived BIS REER
snapshot from the Wayback Machine. Japan's post-2022 GDP benchmark revisions
raised current-vintage RGDP by 3.5 to 6.3 percent over 2019 through 2021 and
flattened the COVID trough. The BIS REER was retroactively rebased from 2010
to 2020 in 2023 with updated trade weights. These revisions collectively
changed the sign of the restricted model's RGDP response. A current-vintage
download is not the data the original authors saw.

**BOJ instead of IMF capital flows.** IMF IFS republishes BOJ and Ministry of
Finance of Japan balance-of-payments data under BPM6. The BOJ series used here
are the primary source and are directly comparable. The BOJ data are monthly
rather than quarterly, which does not present a problem at the daily frequency
where both are interpolated.

## How the missing details were recovered

The risk-off episode dates listed in the paper's Table 1 served as the primary
ground truth. Our reconstructed series was validated against all 15 dates and
matched every one to the day. This confirmed that the VIX source, the MA60
window, and the threshold rule were correct before any VAR estimation began.

Interpolation was the next variable. The pandas piecewise-quadratic spline
(`interpolate(method='quadratic')`) produced a C1-continuous curve that did
not preserve the means of the source periods. The EViews documentation
describes a local quadratic constrained so that the high-frequency values
average to the source observation within each low-frequency period. This
method was reimplemented, tested against the native quarterly and monthly data
for mean preservation at machine precision, and adopted. The difference
between the two interpolation methods proved material for the daily VAR at
longer horizons.

Lag selection was diagnosed by running AIC across caps from 5 through 20 on
the daily data and from 4 through 12 on the monthly data. AIC consistently
hit the boundary. The AIC value continued decreasing as lags were added,
consistent with the penalty term being swamped by the likelihood improvement
in a system with ten variables and over 5,000 daily observations. BIC, with
its heavier penalty, selected stable and interpretable lags. This pattern was
documented and BIC was chosen for the monthly tier with the divergence from
the paper's stated AIC criterion disclosed.

The restricted model's RGDP sign failure was traced to the data vintage by A/B
comparison. The restricted model on current-vintage data gave a positive RGDP
response. The same model on the 2021 vintage gave a negative response. The
only change was the RGDP series. The magnitude of the vintage revision (3.5 to
6.3 percent) was verified against the original paper's estimation window by
comparing the 2021-06-01 ALFRED vintage to the current FRED download for every
overlapping quarter.

The IRF computation was verified against the standard formulation in Lutkepohl
(2005), and several defects were identified and corrected during the
diagnostic phase. See Replication fidelity below.

## Replication fidelity

Five code defects were identified and corrected during the replication

- An IRF recursion transpose that swapped equation and variable indices,
  corrupting every impulse response in every specification. The effect of
  risk-off on RGDP was replaced with the effect of RGDP on risk-off.

- A plot indexing error that displayed the response of risk-off to other
  variables' shocks rather than the response of each variable to a risk-off
  shock. The visual comparison against the paper was meaningless until this
  was corrected.

- A missing constant term in all estimated equations despite the paper's
  model explicitly including one. With trending log-level variables, omitting
  the intercept forced every equation through zero.

- Flat confidence bands built from residual standard errors that did not
  propagate parameter uncertainty through the IRF horizon. These were
  replaced with Monte Carlo bands that widen with the forecast horizon.

- A coefficient-storage bug in the restricted VAR where own-lag coefficients
  for the risk-off equation were stored contiguously but read as if they were
  laid out in a lag-major, variable-minor array. Own-lag-2 and own-lag-3
  coefficients were incorrectly interpreted as lag-1 cross-variable
  coefficients, and the true higher-lag own-coefficient slots remained zero.

After correction of all five defects and the application of the dual-vintage
policy, the core findings reproduce. The replication is closest to the paper
in the monthly restricted vintage specification, where RGDP is negative and
significant at every horizon through month 6 with consistent signs for REER
and spread. The daily restricted specification reproduces the signs but at a
shallower magnitude. The areas of divergence — Nikkei impact, RGDP magnitude,
WUI oscillation, and the restricted/unrestricted consistency — are documented
in the paper and in the HTML report under the Replication Fidelity heading.

## CLI reference

| Flag | Description |
|------|-------------|
| *(default)* | Run the full two-tier pipeline and write all outputs |
| `--with-daily-ci` | Compute daily restricted Monte Carlo confidence bands |
| `--repl N` | Bootstrap replications (default 1000) |
| `--verify` | Rerun pipeline and compare outputs against committed git references |
| `--fetch-vintage-gdp` | Download JPNRGDPEXP from ALFRED for vintage date 2021-06-01 |
| `--fetch-vintage-reer` | Download BIS broad REER from Wayback Machine snapshot |
| `--interpolate-v1` | Regenerate v1 pandas-spline daily CSVs from natives (called by the QMD) |

## Limitations

This replication carries several limitations that are disclosed in the paper
itself. Three are unresolved constraints of the published source material.
Three are choices we made with acknowledged trade-offs.

The paper's EViews interpolation settings are unreported. The choice of
quadratic-match average, quadratic-match sum, or quadratic-match point
affects the interpolated daily path, and the difference propagates through
the VAR coefficient estimates at longer horizons. Our reimplementation uses
quadratic-match average, which is the default EViews setting, but the paper
does not confirm this.

The BIS REER vintage relies on a single Wayback Machine snapshot from May 24,
2021. The BIS does not publicly archive retrospective REER vintages. There is
no way to verify that this snapshot is the exact series the paper's authors
used.

The paper states that the WUI is converted from monthly frequency, but the
World Uncertainty Index monthly dataset begins in January 2008. The paper's
sample starts in January 1999. The quarterly WUI must be the source, and the
conversion from quarterly to working-days frequency is a modeling decision,
not a reproduction of the paper's method.

Our capital flow series use BOJ BPM6 data rather than IMF IFS data. Both
follow the same international statistical standard and the IMF republishes
BOJ figures, making the two directly comparable. The BOJ data are at a higher
monthly frequency than the IMF's quarterly, which introduces high-frequency
variation the paper's VAR would not have seen.

The monthly VAR uses BIC for lag selection where the paper states AIC. AIC
overfits to the boundary on our data, a pattern we verified across multiple
caps. The monthly BIC-selected lag of 3 produces IRFs that match the paper's
Appendix 4 figures more closely than any AIC-selected lag from 1 through 12.

The estimation is in Python using `statsmodels` and custom OLS. The paper
almost certainly used EViews. LAPACK and BLAS differences between platforms
may produce small numerical differences in coefficient estimates that
propagate through impulse response computations. The observable effect is
that Monte Carlo confidence bands differ across machines even with a fixed
seed, a behavior documented in the README and in the `--verify` documentation.

## Repository layout

```
finarts-final-paper/
├── data_pipeline.qmd                  # Quarto document: data construction, narrative, and results
├── index.html                         # Rendered HTML (hosted via Netlify)
├── README.md                          # This file
├── netlify.toml                       # Netlify deployment configuration
├── pyproject.toml                     # Python project metadata and dependencies
├── uv.lock                            # Deterministic dependency lock file
├── references.bib                     # BibTeX references
├── .gitignore
├── articles/                          # Reference PDFs and paper full-text markdown
│   ├── Beirne_Sugandi_2023.pdf
│   ├── Beirne_Sugandi_2023.md
│   └── Japan brands yen falls as 'speculative' as Iran war ignites sell-off By Reuters.pdf
├── scripts/
│   └── replicate_svar.py              # Unified A-Z replication pipeline
├── data/
│   ├── raw/                           # Raw input data
│   │   ├── VIX.csv                    # CBOE Volatility Index (daily)
│   │   ├── NIKKEI225.csv             # Nikkei 225 index (daily)
│   │   ├── US10Y.csv                  # US 10-year Treasury yield (daily)
│   │   ├── USDJPY.csv                 # USD/JPY exchange rate (daily)
│   │   ├── jgbcme_all.csv             # JGB yield curve (daily)
│   │   ├── REER.xlsx                  # BIS broad real effective exchange rate (monthly)
│   │   ├── JAPAN_RGDP.csv             # Japan real GDP (quarterly, FRED JPNRGDPEXP)
│   │   ├── JAPAN_NOMINAL_GDP.csv      # Japan nominal GDP (quarterly, FRED)
│   │   ├── WUI_JPN.csv                # World Uncertainty Index for Japan (quarterly)
│   │   ├── BOJ_6pi-1_portfolio_summary.csv
│   │   ├── BOJ_BPPI6E3N5.csv
│   │   ├── BOJ_BPPI6E4N5.csv
│   │   ├── BOJ_BPPI6E2N5.csv
│   │   ├── BOJ_BPBP6JYNFL3.csv
│   │   ├── BOJ_BPBP6JYNFL13.csv
│   │   └── vintage/
│   │       ├── JPNRGDPEXP_vintage_2021-06-01.csv
│   │       └── REER_JPN_BIS_vintage.csv
│   ├── processed/
│   │   ├── final_dataset.csv
│   │   ├── descriptive_stats.csv
│   │   └── var_results/
│   │       ├── twotier/               # Two-tier final IRF results
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
│   │       └── figures/               # QMD-generated figures
│   └── tmp_quadratic/                 # Interpolation intermediates
│       ├── *_native.csv               # Native-frequency series (QMD output)
│       ├── *_daily.csv                # Pandas-spline daily interpolation (QMD+v1 output)
│       └── v2/*_qdmatch.csv           # Quadratic-match daily interpolation (Python output)
├── docs/
│   └── methodology_dual_vintage.md     # Dual-vintage data policy
├── guidelines/                         # Course project guidelines
└── drafts/                             # Paper sections and presentation materials
```

## Citation

Beirne, J. and Sugandi, E. (2023). Risk-off shocks and spillovers in safe
havens. *Pacific-Basin Finance Journal*, 80, 102103.
