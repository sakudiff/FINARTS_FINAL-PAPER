# Project Checklist — Beirne & Sugandi (2023) Replication

Pacific-Basin Finance Journal, Vol. 80 (ABDC 2025: A)
Updated: 2026-07-10

Report (Google Docs): https://docs.google.com/document/d/1QgA4IIKhEE98QoKd5y7gf8wYRJq37_rhPo6yv2Y0p0o/edit?usp=sharing
This repository is for code and data only.

---

## 1. Selected Article

**Beirne, J. & Sugandi, E. (2023).** Risk-off shocks and spillovers in safe havens. *Pacific-Basin Finance Journal*, 80, 102102.

- Journal: Pacific-Basin Finance Journal
- ABDC 2025 rating: **A** (A-rated in all editions 2010–2025)
- Topic: Safe haven currencies, risk-off shocks, structural VAR, Japan/Switzerland/US
- Methodology: Country-specific recursively restricted VAR with Cholesky decomposition

---

## 2. Compliance Against Project Guidelines

### 2.1 Article Requirements

| Requirement | Status | Notes |
|-------------|--------|-------|
| Finance journal article | Done | Safe haven currencies, FX dynamics, capital flows |
| ABDC A*, A, or B classification | Done | Pacific-Basin Finance Journal — A-rated consistently 2010–2025 |
| From ABDC Journal Quality List | Done | Listed in 2025 JQL spreadsheet in guidelines/ |

### 2.2 Replication Type

Allowed options and applicability:

| Type | Description | Applicability |
|------|-------------|--------------|
| (i) Same sample/variables | Validate original results | Possible but limited interest |
| (ii) Modified sample | Different market or extended period | Chosen approach — extend 1999–2021 to June 2026 |
| (iii) Modified model | New control variable or different technique | Possible addition |
| (iv) Other modifications | Subject to approval | — |

Replication plan: Modified sample. The paper's data period (1999–2021) will be extended to June 30, 2026. This captures the recent yen depreciation, BOJ policy normalization, and the Iran conflict risk-off episode. Focus on Japan only (not Switzerland/US).

### 2.3 Theoretical Foundations

| Requirement | Status |
|-------------|--------|
| Identify theoretical foundations guiding hypotheses | Not yet written |

The paper grounds its analysis in:
- Safe haven currency theory (Baur & Lucey 2010; Hossfeld & MacDonald 2015)
- Carry trade and UIRP deviations (Brunnermeier et al. 2009)
- Portfolio balance / Uncovered Equity Parity (Hau & Rey 2006)
- Flight-to-safety during risk-off episodes (Habib & Stracca 2012)

These need to be written up in the project's theoretical framework section.

### 2.4 LSEG Workspace Data Requirement

| Requirement | Status |
|-------------|--------|
| Portion of analysis must include data from LSEG Workspace | Partial |

The paper uses Bloomberg for bond yields and stock indices. LSEG Workspace (formerly Refinitiv) data has been pulled for USD/JPY and REER. Additional LSEG data can supplement other series.

### 2.5 Statistical Concepts Required

| Requirement | Status |
|-------------|--------|
| (i) Null and alternative hypotheses based on theory | Not yet drafted |
| (ii) Descriptive statistics of data used | Not yet computed |
| (iii) Results of econometric tests (t-test, correlation, regressions) | Not yet run |
| (iv) Discussion of results | Not yet |

### 2.6 Key Dates

| Date | Deliverable | Days Left |
|------|-------------|-----------|
| July 17, 2026 | In-class progress update (15 min presentation) | 7 days |
| August 7, 2026 | Written report submission | 28 days |

---

## 3. Dataset Status

### 3.1 Paper's Original Variables

From Beirne & Sugandi (2023), Section 4:

| # | Variable | Original Source | Original Freq | Original Period | In Repo |
|---|----------|----------------|---------------|-----------------|---------|
| 1 | Risk-off (binary 0/1) | Constructed from VIX | Daily | 1999–2021 | Construct from VIX.csv |
| 2 | WUI (log) | worlduncertaintyindex.com | Quarterly | 1999–2021 | WUI_JPN.csv |
| 3 | Spread (10Y JGB - 10Y US) | Bloomberg | Daily | 1999–2021 | JAPAN10Y.csv + US10Y.csv |
| 4 | RGDP (log) | IMF | Quarterly | 1999–2021 | JAPAN_RGDP.csv |
| 5 | REER (log) | BIS | Monthly | 1999–2021 | REER.xlsx |
| 6 | Stock Index (log Nikkei 225) | Bloomberg | Daily | 1999–2021 | NIKKEI225.csv |
| 7 | Debtsec (% GDP) | IMF / CEIC | Quarterly | 1999–2021 | Pending |
| 8 | Equity (% GDP) | IMF | Quarterly | 1999–2021 | Pending |
| 9 | Other (% GDP) | IMF / CEIC | Quarterly | 1999–2021 | Pending |
| 10 | Direct (% GDP) | IMF / CEIC | Quarterly | 1999–2021 | Pending |

### 3.2 Data In Repo

| # | Variable | File | Source | Freq | Period | Status |
|---|----------|------|--------|------|--------|--------|
| 1 | VIX | `data/raw/VIX.csv` | LSEG `.VIX` | Daily | 1999-01 to 2026-06 | Done |
| 2 | Nikkei 225 | `data/raw/NIKKEI225.csv` | LSEG `.N225` | Daily | 1999-01 to 2026-06 | Done |
| 3 | S&P 500 | `data/raw/SP500.csv` | LSEG `.SPX` | Daily | 1999-01 to 2026-06 | Done |
| 4 | US 10Y Yield | `data/raw/US10Y.csv` | LSEG `US10YT=RR` | Daily | 1999-01 to 2026-06 | Done |
| 5 | JPY/USD | `data/raw/USDJPY.csv` | LSEG `JPY=` | Daily | 1999-01 to 2026-06 | Done |
| 6 | Japan 10Y Yield | `data/raw/JAPAN10Y.csv` | FRED `IRLTLT01JPM156N` | Monthly | 1989-01 to 2026-05 | Done |
| 7 | REER | `data/raw/REER.xlsx` | LSEG Datastream | Monthly | 1996-01 to 2026-05 | Done |
| 8 | Japan RGDP | `data/raw/JAPAN_RGDP.csv` | FRED `JPNRGDPEXP` | Quarterly | 1994-Q1 to 2026-Q1 | Done |
| 9 | WUI (Japan) | `data/raw/WUI_JPN.csv` | worlduncertaintyindex.com | Quarterly | 1952 to 2026-Q1 | Done |

### 3.3 Data Still Needed

To be pulled from Bloomberg terminal:

| # | Variable | Bloomberg Source | Freq | Use |
|---|----------|-----------------|------|-----|
| 10 | Debtsec | ECO -> Japan -> Balance of Payments -> Portfolio debt liabilities | Quarterly | Full 10-variable VAR |
| 11 | Equity | ECO -> Japan -> Balance of Payments -> Portfolio equity liabilities | Quarterly | Full 10-variable VAR |
| 12 | Other | ECO -> Japan -> Balance of Payments -> Other investment liabilities | Quarterly | Full 10-variable VAR |
| 13 | Direct | ECO -> Japan -> Balance of Payments -> FDI liabilities | Quarterly | Full 10-variable VAR |
| 14 | Japan Nominal GDP | ECO -> Japan -> National Accounts -> Nominal GDP | Quarterly | Denominator for %GDP ratios |

### 3.4 Constructed Variable

| Variable | Construction Method | Status |
|----------|-------------------|--------|
| Risk-off (binary) | = 1 when VIX >= (60-day MA of VIX + 10pp), else 0 | To construct in code |
| Spread | = Japan 10Y yield - US 10Y yield | To compute from JAPAN10Y + US10Y |
| JPY/USD return | = delta log(JPY/USD) x 100 | To compute from USDJPY |

---

## 4. Cholesky Ordering

From Beirne & Sugandi (2023), Section 4:

| Position | Variable | Rationale |
|----------|----------|-----------|
| 1 (most exogenous) | Risk-off | External financial shock; affects all domestic variables, not affected by them |
| 2 | WUI | Global uncertainty rises during risk-off but responds slowly |
| 3 | Spread (10Y JGB - 10Y US) | Bond market responds to risk and uncertainty |
| 4 | RGDP | Real economy responds with lag |
| 5 | REER | Exchange rate responds to risk, rates, output |
| 6 | Stock Index (Nikkei 225) | Equity market responds to macro-financial conditions |
| 7 | Debtsec | Portfolio flows respond after macro variables |
| 8 | Equity | Equity flows respond similarly |
| 9 | Other | Other investment flows |
| 10 (most endogenous) | Direct | FDI is slowest-moving |

---

## 5. What Was Done

- [x] Paper selected and downloaded (articles/Beirne_Sugandi_2023.pdf)
- [x] Full text extracted (articles/Beirne_Sugandi_2023.md)
- [x] ABDC compliance verified
- [x] Methodology extracted and understood
- [x] Comparison with old paper documented (data/journal_comparison.md)
- [x] Reuters motivation article kept
- [x] 9 of 14 datasets collected
- [x] Old non-compliant data cleaned out

---

## 6. What Remains

### Before July 17 (Progress Update)

| Task | Priority | Effort | Assigned To |
|------|----------|--------|-------------|
| Draft hypotheses (H1-H3) from theoretical framework | High | 2-3 hours | |
| Specify VAR model equation and lag selection | High | 2 hours | |
| Define all variables operationally | High | 1 hour | |
| Pull capital flows data from Bloomberg | High | 2-3 hours | |
| Construct Risk-off binary variable in code | High | 1 hour | |
| Compute descriptive statistics | High | 1-2 hours | |
| Prepare 12-slide presentation | High | 3-4 hours | |
| Identify data issues (interpolation, gaps) | Medium | 1 hour | |

### Before August 7 (Final Submission)

| Task | Priority | Effort |
|------|----------|--------|
| Run VAR estimation | High | 3-4 hours |
| Generate impulse response functions | High | 2-3 hours |
| Run Granger causality tests | High | 1-2 hours |
| Compute forecast error variance decomposition | Medium | 1-2 hours |
| Write theoretical framework section | High | 3-4 hours |
| Write methodology section | High | 2-3 hours |
| Write results and discussion | High | 4-5 hours |
| Compile references in APA 7 | Medium | 1 hour |
| Format written report | Medium | 2 hours |

---

## 7. Hypotheses

Based on Beirne & Sugandi (2023) findings applied to the extended period (1999–2026):

- **H1**: Risk-off shocks lead to a statistically significant appreciation of the Japanese yen real effective exchange rate.
- **H2**: The yen's safe-haven property weakens during periods of extreme monetary policy divergence (post-2022).
- **H3**: Risk-off shocks have no significant contemporaneous effect on net portfolio flows to Japan, consistent with rapid market adjustment.

---

## 8. Presentation Outline (July 17)

| Slide | Content | Source |
|-------|---------|--------|
| 1 | Title — Paper, group members | Beirne & Sugandi (2023) |
| 2 | Motivation — Iran crisis, yen sell-off, carry trade unwind | Reuters article |
| 3 | Research question | Derived from paper |
| 4 | Paper summary — Key findings | Paper abstract |
| 5 | Theoretical framework — Safe haven, UIRP, flight-to-safety | Literature |
| 6 | Hypotheses H1-H3 | Derived from theory |
| 7 | Econometric model — VAR, Cholesky ordering | Paper Section 4 |
| 8 | Variable definitions with sources | Paper Table 2 |
| 9 | Data status — Collected vs pending | Progress tracking |
| 10 | Descriptive statistics | Computed from data |
| 11 | Challenges — Data gaps, frequency alignment | Assessment |
| 12 | Next steps | Work plan |
