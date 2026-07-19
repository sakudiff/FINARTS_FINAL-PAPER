# Validation Checklist — Beirne & Sugandi (2023) Replication

After running `quarto render data_pipeline.qmd`, open `index.html` and compare each section against the original paper.

## Quick Start

```bash
quarto render data_pipeline.qmd
```

Then open `index.html` in a browser.

---

## 1. Stylized Facts on Risk-off Episodes (Before Descriptive Stats)

Three charts matching paper Figures 1-3.

| Chart | What to Check |
|-------|---------------|
| VIX + 60-day MA + episodes | Risk-off bands should align with 2008 GFC, 2011 Euro crisis, 2020 COVID, 2022 Ukraine |
| USD/JPY + episodes | Yen should spike during risk-off (JPY strengthens, line drops) |
| REER + episodes | Yen REER should rise during risk-off episodes |

---

## 2. Core Paper Findings to Validate

From Beirne and Sugandi (2023) Section 5:

| Finding | Our Panel | Expected Shape |
|---------|-----------|----------------|
| Yen REER appreciates sharply and persists | `log_reer` | Positive spike day 0-5, stays above zero for ~125 days |
| No significant effect on portfolio debt flows | `debtsec_pct` | CI bands straddle zero at all horizons |
| No significant effect on equity flows | `equity_pct` | CI bands straddle zero at all horizons |
| Negative real spillovers (GDP declines) | `log_rgdp` | Negative response, persists |
| Spread widens (JGB vs US) | `spread` | Positive movement (JGB yield rises relative to US) |
| Stock market dips then recovers | `log_nikkei` | Initial negative, returns toward zero |
| WUI rises on risk-off | `log_wui` | Positive response, persists |
| Other investment flows | `other_pct` | May show significance (paper is ambiguous) |
| Direct investment (FDI) | `direct_pct` | Slowest moving, likely insignificant |

---

## 3. Main IRF Figures vs Paper

### Restricted VAR (Paper's Primary Specification)

Compare against paper Figures 4-10 and Appendix 2 (Figure A2.1 for Japan).

| Paper Reference | Our Panel | What to Match |
|-----------------|-----------|---------------|
| Fig 4 / A2.1 row 2: WUI | `log_wui` | Response of LOG(WUI_JP) to RISK Innovation. Positive, peaks around day 25-50, persists |
| Fig 5 / A2.1 row 4: RGDP | `log_rgdp` | Response of LOG(RGDP_JP) to RISK Innovation. Negative, persists entire horizon |
| Fig 6 / A2.1 row 5: REER | `log_reer` | Response of LOG(REER_JP) to RISK Innovation. Positive, sharp initial move, persists |
| Fig 7 / A2.1 row 3: Spread | `spread` | Response of SPREAD_JP to RISK Innovation. Positive, peaks then decays |
| Fig 8 / A2.1 row 6: Stock Index | `log_nikkei` | Response of LOG(STOCK_IDX_JP) to RISK Innovation. Negative initially |
| Fig 9 / A2.1 row 7: Debtsec | `debtsec_pct` | Response of DEBTSEC_JP to RISK Innovation. Insignificant (CI straddles zero) |
| Fig 10 / A2.1 row 8: Equity | `equity_pct` | Response of EQUITY_JP to RISK Innovation. Insignificant (CI straddles zero) |
| A2.1 row 9: Other | `other_pct` | Response of OTHER_JP to RISK Innovation. May show significance |
| A2.1 row 10: Direct | `direct_pct` | Response of DIRECT_JP to RISK Innovation. Insignificant |

Note: paper uses 125-day horizon. Our x-axis shows 0-125 days matching exactly.

---

## 4. CI Method Comparison

| Plot | What It Shows |
|------|---------------|
| Monte Carlo (analytical label) | Parametric MC from N(0, Sigma_u). Bands widen over horizon |
| Bootstrap | Residual-based resampling, 100 reps. Bands also widen over horizon |
| CI comparison overlay | Both methods overlaid. Should be similar; bootstrap may be slightly wider |

---

## 5. Appendix Figures

Located after the IRF section in the QMD.

| Figure | Content |
|--------|---------|
| A1.1 | JGB 10Y yield with risk-off shading |
| A1.2 | Nikkei 225 index with risk-off shading |
| A1.3 | Net debt securities investment (% GDP) with risk-off shading |
| A1.4 | Net equity investment (% GDP) with risk-off shading |
| A1.5 | Net other investment (% GDP) with risk-off shading |
| A1.6 | Net direct investment (% GDP) with risk-off shading |
| A1.7 | Yield spread (JGB 10Y - US 10Y) with risk-off shading |

---

## 6. Frequency Robustness

Located before the appendix. Weekly and monthly restricted VAR IRFs should show
the same qualitative patterns as the daily baseline.

---

## 7. Stationarity Check

From the ADF table in the QMD: the paper claims all variables are stationary.
Our tests show **spread, log_rgdp, log_reer, and log_nikkei** are non-stationary
at 5%. This discrepancy should be addressed in the write-up.

---

## 8. If Results Don't Match

Likely causes in order:

1. **Lag selection**: AIC picks lag 20 (search boundary). Paper may have used fewer lags
2. **Sample period**: Our data is 1999-01-14 to 2021-03-31. Paper uses same start but may have slightly different end
3. **Capital flow definitions**: Our BOJ-based %GDP calculation differs from paper's IMF/CEIC data
4. **Interpolation**: Quadratic interpolation adds artificial smoothness vs paper's method

---

## 9. Next Steps

- [ ] Validate all IRF shapes match paper qualitatively
- [ ] Note any discrepancies for the write-up
- [ ] Export key figures as PDF for LaTeX report
- [ ] Run weekly/monthly robustness (already generated)
- [ ] Draft results section using figures as evidence
