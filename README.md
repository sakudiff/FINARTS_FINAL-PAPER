# Risk-Off Shocks and Spillovers in Safe Havens — Replication and Extension

Replication of Beirne and Sugandi (2023), "Risk-off Shocks and Spillovers in
Safe Havens," *Pacific-Basin Finance Journal*, Vol. 80, 102103. Country-specific
structural vector autoregression for Japan, extended from the paper's 1999–2021
sample through June 2026. Two-tier estimation with a dual-vintage data policy.

Group 4, FINARTS C01, De La Salle University, Academic Year 2025–2026 Term 3.
Submitted August 11, 2026 to Dr. Ray Anthony Almonares.

| Link | URL |
|------|-----|
| Paper | https://docs.google.com/document/d/1QgA4IIKhEE98QoKd5y7gf8wYRJq37_rhPo6yv2Y0p0o |
| Report | https://finalprojectfinartsg4.netlify.app |
| Repository | https://github.com/sakudiff/FINARTS_FINAL-PAPER |

## Group members

| Member | Role |
|--------|------|
| Aaron Joshua Sison | Data handling, retrieval, processing, methodology, coding, results, lead |
| Juliana Patajo | Conclusion |
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
| Lag selection | AIC (maxlags unreported) | AIC (Tier 1), BIC (Tier 2 — AIC overfits to boundary) |
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
| WUI | Smooth positive, then negative | Oscillates more in unrestricted | PARTIAL |
| Capital flows | Insignificant | Mostly insignificant, 2 significant cells (direct_pct h=3) | MATCH |
| Risk-off episodes | 15 episodes listed in Table 1 | All 15 dates exact to the day | MATCH |
| Restricted vs unrestricted | "Fully consistent" (paper's claim) | Diverge on current-vintage data | PARTIAL |

## What the paper did not disclose

| Detail | Implication |
|--------|------------|
| Exact lag count and AIC search ceiling | AIC always hits the boundary on our data; BIC adopted for monthly tier |
| EViews interpolation variant (average vs sum vs point) | Different variants produce meaningfully different daily paths |
| Monthly risk-off aggregation method | Tested sum, binary, and proportion; proportion chosen for correct signs |
| Confidence interval method | Replaced with Monte Carlo delta method (restricted) and asymptotic bands (unrestricted) |
| Software | Figure styling suggests EViews; pipeline uses Python and statsmodels |
| GDP data source vintage | 3.5–6.3% revision over 2019–2021 requires vintage data for replication |

## Why each decision was made

| Decision | Rationale | Paper's approach |
|----------|----------|------------------|
| Monthly frequency for Tier 2 | Daily VAR on interpolated quarterly GDP showed wrong RGDP sign | Daily baseline with monthly robustness |
| BIC instead of AIC for monthly | AIC consistently selected boundary lag at every tested cap | Stated AIC, did not report cap |
| Unrestricted as baseline for monthly | Restricted model failed on current-vintage RGDP (vintage substitution confirmed revision sensitivity) | Both restricted and unrestricted, claimed consistency |
| Proportion risk-off aggregation | Sum inflated shock SD to 2.23, binary gave wrong RGDP sign | Not specified |
| Dual-vintage data policy | Post-2022 GDP benchmark revisions changed RGDP sign; BIS REER retroactively rebased | Used current data at time of writing |
| BOJ instead of IMF capital flows | IMF IFS republishes BOJ/MOF data under BPM6; directly comparable | IMF IFS quarterly BOP |

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
immediate-positive impact effect is not reproduced. Daily RGDP magnitude is
shallower than the paper's charts. The restricted and unrestricted
specifications diverge on current-vintage data, contrary to the paper's
claim of full consistency. This divergence is presented as a finding about
sensitivity to GDP data revisions rather than a failure of either
specification.

## Limitations

The paper's EViews interpolation settings are unreported. The BIS REER
vintage relies on a single Wayback Machine snapshot. The paper states the
WUI is monthly, but the dataset begins January 2008. Quarterly WUI is the
defensible source. BOJ capital flows are higher frequency than the paper's
IMF series, introducing variation the paper's VAR would not have seen.
The monthly tier uses BIC for lag selection where the paper states AIC.
The unrestricted CIs use asymptotic bands rather than Monte Carlo. The
pipeline is in Python; the paper almost certainly used EViews. Cross-platform
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
├── data_pipeline.qmd              # QMD document: data construction, narrative, results
├── index.html                     # Rendered HTML (Netlify)
├── README.md
├── netlify.toml
├── pyproject.toml / uv.lock       # Python dependencies (uv)
├── references.bib
├── .gitignore
├── articles/                      # Reference PDFs
├── scripts/
│   └── replicate_svar.py          # Unified replication pipeline
├── data/
│   ├── raw/                       # Input data + vintage CSVs
│   ├── processed/
│   │   ├── final_dataset.csv      # Daily panel (1999–2026)
│   │   └── var_results/
│   │       ├── twotier/           # IRF and flow significance outputs
│   │       ├── figures/           # QMD-generated figures
│   │       ├── adf_tests_*.csv
│   │       └── lag_selection_*.csv
│   └── tmp_quadratic/             # Interpolation intermediates
├── docs/
│   └── methodology_dual_vintage.md
├── guidelines/
└── drafts/
```

## Citation

Beirne, J. and Sugandi, E. (2023). Risk-off shocks and spillovers in safe
havens. *Pacific-Basin Finance Journal*, 80, 102103.
