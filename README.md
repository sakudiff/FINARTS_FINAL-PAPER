# Project Checklist — Beirne & Sugandi (2023) Replication

Pacific-Basin Finance Journal, Vol. 80 (ABDC 2025: A)
Updated: 2026-07-10

Report (Google Docs): https://docs.google.com/document/d/1QgA4IIKhEE98QoKd5y7gf8wYRJq37_rhPo6yv2Y0p0o/edit?usp=sharing
This repository is for code and data only.

## Group 4

- Sison, Aaron Joshua E.
- Opiana, Aimee Lorynne A.
- Galedo, Enrique Lorenzo
- Patajo, Juliana
- Go, Keira
- Cuenca, Raphael

---

## 1. Selected Article

**Beirne, J. & Sugandi, E. (2023).** Risk-off shocks and spillovers in safe havens. *Pacific-Basin Finance Journal*, 80, 102102. https://doi.org/10.1016/j.pacfin.2023.102102

- Journal: Pacific-Basin Finance Journal
- ABDC 2025 rating: **A** (A-rated in all editions 2010–2025)
- Topic: Safe haven currencies, risk-off shocks, structural VAR, Japan/Switzerland/US
- Methodology: Country-specific recursively restricted VAR with Cholesky decomposition

---

## 2. Compliance Against Project Guidelines

### 2.1 Article Requirements

| Requirement                     | Status | Notes                                                            |
| ------------------------------- | ------ | ---------------------------------------------------------------- |
| Finance journal article         | Done   | Safe haven currencies, FX dynamics, capital flows                |
| ABDC A*, A, or B classification | Done   | Pacific-Basin Finance Journal — A-rated consistently 2010–2025 |
| From ABDC Journal Quality List  | Done   | Listed in 2025 JQL spreadsheet in guidelines/                    |

### 2.2 Replication Type

Allowed options and applicability:

| Type                      | Description                                 | Applicability                                     |
| ------------------------- | ------------------------------------------- | ------------------------------------------------- |
| (i) Same sample/variables | Validate original results                   | Possible but limited interest                     |
| (ii) Modified sample      | Different market or extended period         | Chosen approach — extend 1999–2021 to June 2026 |
| (iii) Modified model      | New control variable or different technique | Possible addition                                 |
| (iv) Other modifications  | Subject to approval                         | —                                                |

Replication plan: Modified sample. The paper's data period (1999–2021) will be extended to June 30, 2026. This captures the recent yen depreciation, BOJ policy normalization, and the Iran conflict risk-off episode. Focus on Japan only (not Switzerland/US).

### 2.3 Theoretical Foundations

| Requirement                                         | Status          |
| --------------------------------------------------- | --------------- |
| Identify theoretical foundations guiding hypotheses | Not yet written |

The paper grounds its analysis in:

- Safe haven currency theory (Baur & Lucey 2010; Hossfeld & MacDonald 2015)
- Carry trade and UIRP deviations (Brunnermeier et al. 2009)
- Portfolio balance / Uncovered Equity Parity (Hau & Rey 2006)
- Flight-to-safety during risk-off episodes (Habib & Stracca 2012)

These need to be written up in the project's theoretical framework section.

### 2.4 LSEG Workspace Data Requirement

| Requirement                                               | Status  |
| --------------------------------------------------------- | ------- |
| Portion of analysis must include data from LSEG Workspace | Partial |

The paper uses Bloomberg for bond yields and stock indices. LSEG Workspace (formerly Refinitiv) data has been pulled for USD/JPY and REER. Additional LSEG data can supplement other series.

### 2.5 Statistical Concepts Required

| Requirement                                                           | Status           |
| --------------------------------------------------------------------- | ---------------- |
| (i) Null and alternative hypotheses based on theory                   | Not yet drafted  |
| (ii) Descriptive statistics of data used                              | Not yet computed |
| (iii) Results of econometric tests (t-test, correlation, regressions) | Not yet run      |
| (iv) Discussion of results                                            | Not yet          |

### 2.6 Key Dates

| Date           | Deliverable                                    | Days Left |
| -------------- | ---------------------------------------------- | --------- |
| July 17, 2026  | In-class progress update (15 min presentation) | 7 days    |
| August 7, 2026 | Written report submission                      | 28 days   |

---

## 3. Dataset Status

### 3.1 Paper's Original Variables

From Beirne & Sugandi (2023), Section 4:

| #  | Variable                     | Original Source           | Original Freq | Original Period | In Repo                  |
| -- | ---------------------------- | ------------------------- | ------------- | --------------- | ------------------------ |
| 1  | Risk-off (binary 0/1)        | Constructed from VIX      | Daily         | 1999–2021      | Construct from VIX.csv   |
| 2  | WUI (log)                    | worlduncertaintyindex.com | Quarterly     | 1999–2021      | WUI_JPN.csv              |
| 3  | Spread (10Y JGB - 10Y US)    | Bloomberg                 | Daily         | 1999–2021      | JAPAN10Y.csv + US10Y.csv |
| 4  | RGDP (log)                   | IMF                       | Quarterly     | 1999–2021      | JAPAN_RGDP.csv           |
| 5  | REER (log)                   | BIS                       | Monthly       | 1999–2021      | REER.xlsx                |
| 6  | Stock Index (log Nikkei 225) | Bloomberg                 | Daily         | 1999–2021      | NIKKEI225.csv            |
| 7  | Debtsec (% GDP)              | IMF / CEIC                | Quarterly     | 1999–2021      | Partial (needs pre-2014) |
| 8  | Equity (% GDP)               | IMF                       | Quarterly     | 1999–2021      | Partial (needs pre-2014) |
| 9  | Other (% GDP)                | IMF / CEIC                | Quarterly     | 1999–2021      | BOJ_BPBP6JYNFL3.csv      |
| 10 | Direct (% GDP)               | IMF / CEIC                | Quarterly     | 1999–2021      | BOJ_BPBP6JYNFL13.csv     |

### 3.2 Full Dataset Status

| #  | Variable                          | File                                                                    | Source                      | Freq      | Period             | Status                 |
| -- | --------------------------------- | ----------------------------------------------------------------------- | --------------------------- | --------- | ------------------ | ---------------------- |
| 1  | VIX                               | `data/raw/VIX.csv`                                                    | LSEG`.VIX`                | Daily     | 1999-01 to 2026-06 | Done                   |
| 2  | Nikkei 225                        | `data/raw/NIKKEI225.csv`                                              | LSEG`.N225`               | Daily     | 1999-01 to 2026-06 | Done                   |
| 3  | S&P 500                           | `data/raw/SP500.csv`                                                  | LSEG`.SPX`                | Daily     | 1999-01 to 2026-06 | Done                   |
| 4  | US 10Y Yield                      | `data/raw/US10Y.csv`                                                  | LSEG`US10YT=RR`           | Daily     | 1999-01 to 2026-06 | Done                   |
| 5  | JPY/USD                           | `data/raw/USDJPY.csv`                                                 | LSEG`JPY=`                | Daily     | 1999-01 to 2026-06 | Done                   |
| 6  | Japan 10Y Yield                   | `data/raw/JAPAN10Y.csv`                                               | FRED`IRLTLT01JPM156N`     | Monthly   | 1989-01 to 2026-05 | Done                   |
| 7  | REER                              | `data/raw/REER.xlsx`                                                  | LSEG Datastream             | Monthly   | 1996-01 to 2026-05 | Done                   |
| 8  | Japan RGDP                        | `data/raw/JAPAN_RGDP.csv`                                             | FRED`JPNRGDPEXP`          | Quarterly | 1994-Q1 to 2026-Q1 | Done                   |
| 9  | WUI (Japan)                       | `data/raw/WUI_JPN.csv`                                                | worlduncertaintyindex.com   | Quarterly | 1952 to 2026-Q1    | Done                   |
| 10 | Japan Nominal GDP                 | `data/raw/JAPAN_NOMINAL_GDP.csv`                                      | FRED`NGDPSAXDCJPQ`        | Quarterly | 1994-Q1 to 2026-Q1 | Done                   |
| 11 | Direct (FDI liabilities)          | `data/raw/BOJ_BPBP6JYNFL13.csv`                                       | BOJ API                     | Monthly   | 1996-01 to 2026-05 | Done                   |
| 12 | Other (other invest. liabilities) | `data/raw/BOJ_BPBP6JYNFL3.csv`                                        | BOJ API                     | Monthly   | 1996-01 to 2026-05 | Done                   |
| 13 | Debtsec (portfolio debt)          | `data/raw/BOJ_BPPI6E3N5.csv` + `BOJ_BPPI6E4N5.csv` + pre-2014 merge | BOJ API (2014+) + 6pi-1 CSV | Monthly   | 2014-01 to 2026-05 | Pre-2014 needs parsing |
| 14 | Equity (portfolio equity)         | `data/raw/BOJ_BPPI6E2N5.csv` + pre-2014 merge                         | BOJ API (2014+) + 6pi-1 CSV | Monthly   | 2014-01 to 2026-05 | Pre-2014 needs parsing |

---

## 4. Cholesky Ordering

From Beirne & Sugandi (2023), Section 4:

| Position             | Variable                  | Rationale                                                                      |
| -------------------- | ------------------------- | ------------------------------------------------------------------------------ |
| 1 (most exogenous)   | Risk-off                  | External financial shock; affects all domestic variables, not affected by them |
| 2                    | WUI                       | Global uncertainty rises during risk-off but responds slowly                   |
| 3                    | Spread (10Y JGB - 10Y US) | Bond market responds to risk and uncertainty                                   |
| 4                    | RGDP                      | Real economy responds with lag                                                 |
| 5                    | REER                      | Exchange rate responds to risk, rates, output                                  |
| 6                    | Stock Index (Nikkei 225)  | Equity market responds to macro-financial conditions                           |
| 7                    | Debtsec                   | Portfolio flows respond after macro variables                                  |
| 8                    | Equity                    | Equity flows respond similarly                                                 |
| 9                    | Other                     | Other investment flows                                                         |
| 10 (most endogenous) | Direct                    | FDI is slowest-moving                                                          |

---

## 5. Data Transformation Notes

### BOJ Capital Flow Series Merge

The portfolio investment data (Debtsec and Equity) comes from two sources that need to be combined:

| Period             | Source                                                        | Format                                                                                                                                                                            |
| ------------------ | ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1996-01 to 2013-12 | BOJ historical CSV (data/raw/BOJ_6pi-1_portfolio_summary.csv) | Shift-JIS encoded, multi-section layout. Sections for Liabilities / Long-term debt securities, Short-term debt securities, and Equity and investment fund shares need extraction. |
| 2014-01 to 2026-05 | BOJ API (data/raw/BOJ_BPPI6E*.csv)                            | Clean monthly CSV, 100 million Yen.                                                                                                                                               |

The merge can be done with a SQL UNION ALL or pandas concat on the month key:

```
SELECT date, value FROM pre_2014_data
UNION ALL
SELECT date, value FROM post_2014_data
ORDER BY date;
```

No dedup needed since the ranges do not overlap (split at 2014-01).

### Frequency Alignment

All variables must be aligned to daily frequency before running the VAR:

| Native Freq | Variables                                         | Interpolation Method             |
| ----------- | ------------------------------------------------- | -------------------------------- |
| Daily       | VIX, Nikkei 225, S&P 500, US 10Y, JPY/USD         | Native - no transform            |
| Monthly     | Japan 10Y, REER                                   | Quadratic interpolation to daily |
| Quarterly   | RGDP, Nominal GDP, Debtsec, Equity, Other, Direct | Quadratic interpolation to daily |
| Quarterly   | WUI                                               | Quadratic interpolation to daily |

### Unit Conversions

- BOJ data is in 100 million Yen. Convert to billions of USD using USD/JPY exchange rate.
- Capital flow ratios: (Net inflow in USD bn / Nominal GDP in USD bn) x 100
- Japan nominal GDP from FRED is in millions of JPY. Convert to USD bn using USD/JPY.
- All constructed variables (Risk-off binary, log transforms, first differences, spread) will be computed in analysis scripts.

---

## 6. What Was Done

- [X] Paper selected and downloaded (articles/Beirne_Sugandi_2023.pdf)
- [X] Full text extracted (articles/Beirne_Sugandi_2023.md)
- [X] ABDC compliance verified
- [X] Methodology extracted and understood
- [X] Comparison with old paper documented (data/journal_comparison.md)
- [X] Reuters motivation article kept
- [X] 12 of 14 datasets collected
- [X] Old non-compliant data cleaned out

---

## 7. What Remains

### Before July 17 (Progress Update)

- [ ] Draft hypotheses (H1-H3) from theoretical framework — Raphael (High, 2-3 hrs)
- [ ] Specify VAR model equation and lag selection (High, 2 hrs)
- [ ] Define all variables operationally — Aimee (High, 1 hr)
- [ ] Complete BOJ portfolio data merge (pre-2014 parsing from 6pi-1 CSV) (High, 2-3 hrs)
- [ ] Construct Risk-off binary variable in code — Aaron (High, 1 hr)
- [ ] Compute descriptive statistics — Aaron (High, 1-2 hrs)
- [ ] Prepare 12-slide presentation (High, 3-4 hrs)
- [ ] Identify data issues (interpolation, gaps) — Aaron (Medium, 1 hr)

### Before August 7 (Final Submission)

- [ ] Run VAR estimation (High, 3-4 hrs)
- [ ] Generate impulse response functions (High, 2-3 hrs)
- [ ] Run Granger causality tests (High, 1-2 hrs)
- [ ] Compute forecast error variance decomposition (Medium, 1-2 hrs)
- [ ] Write theoretical framework section (High, 3-4 hrs)
- [ ] Write methodology section (High, 2-3 hrs)
- [ ] Write results and discussion (High, 4-5 hrs)
- [ ] Compile references in APA 7 (Medium, 1 hr)
- [ ] Format written report (Medium, 2 hrs)

### Paper Sections (Following Original Article)

- [ ] 1. Introduction — Motivation, research question, contribution
- [ ] 2. Related Literature — Safe haven currencies, UIRP, carry trade, flight-to-safety
- [ ] 3. Stylized Facts on Risk-off Episodes — VIX threshold method, risk-off event identification
- [ ] 4.1 Data — Variable sources, frequency, transformations — Aimee
- [ ] 4.2 Empirical Methodology — VAR specification, lag selection, stationarity tests
- [ ] 4.3 Cholesky Decomposition — Variable ordering, identification assumptions
- [ ] 5. Empirical Results — IRFs, Granger causality, FEVD
- [ ] 6. Conclusions — Summary, limitations, implications
- [ ] References — APA 7 formatting

---

## 9. Constructed Variables

| Variable          | Construction                                             | Data Source                                                                         | Status      |
| ----------------- | -------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------- |
| Risk-off (binary) | = 1 when VIX >= (60-day MA of VIX + 10pp), else 0        | data/raw/VIX.csv                                                                    | Pending     |
| Spread            | = Japan 10Y yield - US 10Y yield                         | data/raw/JAPAN10Y.csv - data/raw/US10Y.csv                                          | Pending     |
| JPY/USD return    | = delta log(JPY/USD) x 100                               | data/raw/USDJPY.csv                                                                 | Pending     |
| Log(WUI)          | = log(World Uncertainty Index)                           | data/raw/WUI_JPN.csv                                                                | Pending     |
| Log(RGDP)         | = log(Real GDP)                                          | data/raw/JAPAN_RGDP.csv                                                             | Pending     |
| Log(REER)         | = log(Real Effective Exchange Rate)                      | data/raw/REER.xlsx                                                                  | Pending     |
| Log(Nikkei 225)   | = log(Nikkei 225 Index)                                  | data/raw/NIKKEI225.csv                                                              | Pending     |
| Debtsec (% GDP)   | = (Net portfolio debt liabilities / Nominal GDP) x 100   | data/raw/BOJ_BPPI6E3N5.csv + BPPI6E4N5.csv + pre-2014 merge + JAPAN_NOMINAL_GDP.csv | Pending     |
| Equity (% GDP)    | = (Net portfolio equity liabilities / Nominal GDP) x 100 | data/raw/BOJ_BPPI6E2N5.csv + pre-2014 merge + JAPAN_NOMINAL_GDP.csv                 | Pending     |
| Other (% GDP)     | = (Net other investment liabilities / Nominal GDP) x 100 | data/raw/BOJ_BPBP6JYNFL3.csv + JAPAN_NOMINAL_GDP.csv                                | Data pulled |
| Direct (% GDP)    | = (Net FDI liabilities / Nominal GDP) x 100              | data/raw/BOJ_BPBP6JYNFL13.csv + JAPAN_NOMINAL_GDP.csv                               | Data pulled |

---

## 10. Hypotheses

| Hypothesis | Original (Beirne & Sugandi 2023)                                           | Ours |
| ---------- | -------------------------------------------------------------------------- | ---- |
| H1         | Risk-off shocks lead to yen REER appreciation                              |      |
| H2         | Yen safe-haven property weakens under extreme monetary divergence          |      |
| H3         | Risk-off shocks have no significant effect on net portfolio flows to Japan |      |

---

## 11. Presentation Outline (July 17)

| Slide | Content                                                     | Source                  | Assigned To |
| ----- | ----------------------------------------------------------- | ----------------------- | ----------- |
| 1     | Title — Paper, group members                               | Beirne & Sugandi (2023) |             |
| 2     | Motivation — Iran crisis, yen sell-off, carry trade unwind | Reuters article         |             |
| 3     | Research question                                           | Derived from paper      |             |
| 4     | Paper summary — Key findings                               | Paper abstract          |             |
| 5     | Theoretical framework — Safe haven, UIRP, flight-to-safety | Literature              |             |
| 6     | Hypotheses H1-H3                                            | Derived from theory     | Raphael     |
| 7     | Econometric model — VAR, Cholesky ordering                 | Paper Section 4         |             |
| 8     | Variable definitions with sources                           | Paper Table 2           | Aimee       |
| 9     | Data status — Collected vs pending                         | Progress tracking       |             |
| 10    | Descriptive statistics                                      | Computed from data      | Aaron       |
| 11    | Challenges — Data gaps, frequency alignment                | Assessment              | Aaron       |
| 12    | Next steps                                                  | Work plan               |             |

---

## 12. Paper Outline

| Section                           | Content                                                              | Assigned To |
| --------------------------------- | -------------------------------------------------------------------- | ----------- |
| 1. Introduction                   | Motivation, research question, contribution statement                |             |
| 2. Related Literature             | Safe haven currencies, UIRP puzzle, carry trade, flight-to-safety    |             |
| 3. Stylized Facts                 | Risk-off episodes, VIX threshold method, yen behavior during crises  |             |
| 4. Data and Empirical Methodology | Variable descriptions, sources, VAR specification, Cholesky ordering | Aaron       |
| 5. Empirical Results              | Impulse response functions, Granger causality, FEVD                  |             |
| 6. Conclusions                    | Summary of findings, limitations, policy implications                |             |
| References                        | APA 7                                                                |             |
| Appendix                          | Additional IRFs, robustness checks                                   |             |
