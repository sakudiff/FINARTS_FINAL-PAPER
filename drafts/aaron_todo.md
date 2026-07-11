# Aaron — To Do

Exact steps to replicate Beirne & Sugandi (2023) Section 4 methodology.
Cross-referenced against the paper. Each item below maps to a specific part of the paper.

---

## Data Construction

Paper reference: Section 4, Table 2.

| # | Task | Paper Method | Files / Source | Status |
|---|------|-------------|---------------|--------|
| 1 | Risk-off binary | = 1 when VIX >= (60-day MA of VIX + 10pp), else 0. Same threshold as De Bock & De Carvalho Filho (2013). First 60 obs will be NaN. | data/raw/VIX.csv | Pending |
| 2 | Log(WUI) | Natural log of World Uncertainty Index (Japan). Quarterly, interpolate to daily. | data/raw/WUI_JPN.csv | Pending |
| 3 | Spread | Japan 10Y government bond yield minus US 10Y Treasury yield. JGB yield is monthly, interpolate to daily. US yield is daily. | data/raw/JAPAN10Y.csv - data/raw/US10Y.csv | Pending |
| 4 | Log(RGDP) | Natural log of constant-price GDP. Quarterly, interpolate to daily. | data/raw/JAPAN_RGDP.csv | Pending |
| 5 | Log(REER) | Natural log of BIS real effective exchange rate (broad index). Monthly, interpolate to daily. | data/raw/REER.xlsx | Pending |
| 6 | Log(Nikkei 225) | Natural log of Nikkei 225 stock index. Daily, no transform. | data/raw/NIKKEI225.csv | Pending |
| 7 | Debtsec (% GDP) | (Net portfolio debt liabilities / Nominal GDP) x 100. Monthly BOJ data in 100M JPY. Convert to USD bn via USD/JPY. Interpolate to daily. | BOJ API (2014+) + BOJ_6pi-1 CSV merge + data/raw/JAPAN_NOMINAL_GDP.csv | Pending |
| 8 | Equity (% GDP) | (Net portfolio equity liabilities / Nominal GDP) x 100. Same unit conversion and interpolation as Debtsec. | BOJ API (2014+) + BOJ_6pi-1 CSV merge + data/raw/JAPAN_NOMINAL_GDP.csv | Pending |
| 9 | Other (% GDP) | (Net other investment liabilities / Nominal GDP) x 100. Same conversion. | data/raw/BOJ_BPBP6JYNFL3.csv + JAPAN_NOMINAL_GDP.csv | Pending |
| 10 | Direct (% GDP) | (Net FDI liabilities / Nominal GDP) x 100. Same conversion. | data/raw/BOJ_BPBP6JYNFL13.csv + JAPAN_NOMINAL_GDP.csv | Pending |

---

## Data Transformations

Paper reference: Section 4 footnotes 3-4, Table 2.

| # | Task | Paper Specification | Implementation |
|---|------|-------------------|----------------|
| 11 | Frequency alignment | Monthly variables (Japan 10Y, REER) converted to working days via quadratic interpolation | Python pandas.Series.interpolate(method=quadratic) |
| 12 | Frequency alignment | Quarterly variables (RGDP, Nominal GDP, Debtsec, Equity, Other, Direct, WUI) converted to working days via quadratic interpolation | Same method |
| 13 | Unit conversion (BOJ data) | BOJ series are in 100 million JPY. Paper uses USD bn. Convert using USD/JPY spot rate from data/raw/USDJPY.csv. | value_usd_bn = (value_100m_jpy * 100,000,000) / usd_jpy_rate / 1e9 |
| 14 | Unit conversion (Nominal GDP) | FRED series is in millions of JPY. Need JPY to USD at current rate, then to USD bn. | gdp_usd_bn = gdp_million_jpy * 1e6 / usd_jpy_rate / 1e9 |
| 15 | Working days alignment | Paper uses only working days (14 Jan 1999 to 31 Mar 2021 for Japan). Our extended period: working days from 1 Jan 1999 to 30 Jun 2026. | Filter to weekdays only, align across all series |
| 16 | Log transforms | WUI, RGDP, REER, Nikkei 225 are in logs per paper. | numpy.log() |

---

## VAR Estimation

Paper reference: Section 4 (Equation 1), Section 5.

| # | Task | Paper Method | Details |
|---|------|-------------|---------|
| 17 | Lag selection | Akaike Information Criterion (AIC). Paper uses monthly data; paper's optimal lag is determined per model. | statsmodels.tsa.var_model.VAR with lag_order search |
| 18 | Stationarity tests | All series tested for unit roots before estimation. Paper confirms all endogenous variables are stationary. | ADF test on each variable |
| 19 | Recursively restricted VAR | Risk-off variable restricted: only affected by its own lagged values. Other variables unrestricted. | Set coefficient matrix A_j to zero for non-Risk-off rows in Risk-off equation |
| 20 | Unrestricted VAR | All endogenous variables affected by lagged values of all variables. | Standard VAR estimation |
| 21 | Cholesky decomposition | Ordering: Risk-off -> WUI -> Spread -> RGDP -> REER -> Stock Index -> Debtsec -> Equity -> Other -> Direct | statsmodels.tsa.var_model.VAR with ordering |
| 22 | Impulse Response Functions | Response to one-standard deviation structural shock on Risk-off variable. 95% CI from bootstrap (1000 runs). | irf = results.irf(periods=N); irf.plot() |
| 23 | Granger causality tests | Paper reports Granger causality from each variable to exchange rate and capital flows. | results.test_causality() |
| 24 | FEVD | Forecast error variance decomposition to show relative importance of each shock. | results.fevd() |

---

## Robustness

Paper reference: Appendix 4, footnotes.

| # | Task | Paper Method |
|---|------|-------------|
| 25 | Weekly frequency robustness | Re-run restricted VAR at weekly frequency |
| 26 | Monthly frequency robustness | Re-run restricted VAR at monthly frequency |
| 27 | Unrestricted VAR | Re-run without block restrictions on Risk-off |

---

## Presentation Slides

| # | Slide | Status |
|---|-------|--------|
| 28 | Title, group members | Ready |
| 29 | Motivation (Iran crisis, carry trade) | Ready from Reuters article |
| 30 | Research question | Ready |
| 31 | Paper summary | Ready from abstract |
| 32 | Theoretical framework | Ready from literature |
| 33 | Hypotheses H1-H3 | Pending (Raphael) |
| 34 | VAR model, Cholesky ordering | Ready from paper Section 4 |
| 35 | Variable definitions | Pending (Aimee) |
| 36 | Data status | Ready |
| 37 | Descriptive statistics | After tasks 1-16 completed |
| 38 | Data challenges | After tasks 1-16 completed |
| 39 | Next steps | Ready |

---

## Key Paper Specifics to Match

- Paper uses data from 14 Jan 1999 to 31 Mar 2021 (Japan). Our extension: to 30 Jun 2026.
- Paper uses daily working days frequency. Align all series to a common working days calendar.
- Paper interpolates monthly (WUI, REER) and quarterly (RGDP, capital flows, Nominal GDP) to working days using quadratic interpolation.
- Paper computes capital flows as % of nominal GDP (current prices, USD).
- Paper estimates both restricted (Risk-off block) and unrestricted VAR.
- Paper uses AIC for lag selection.
- Paper reports IRFs, Granger causality, and FEVD for all models.
- 95% confidence intervals from residual-based bootstrap with 1000 runs.
- Paper uses seasonal dummies and time dummy as exogenous variables.
