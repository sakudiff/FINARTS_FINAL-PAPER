# Journal Compliance & Article Comparison

> Generated: 2026-07-10
> Context: FINARTS Term Project — Group 5 replication study

---

## 1. Current Article: ABDC Compliance Check

### Selected Article
**Guyot, Montgomery & Yang (2026)** — *Risk Premiums, Market Volatility, and Exchange Rate Dynamics: Evidence from the Yen Carry Trade*
- Published in: **Risks**, 14(2), 46, MDPI
- DOI: `10.3390/risks14030046`

### ABDC Rating

| Edition | Status | Rating |
|---------|--------|--------|
| **2025 JQL** (provided in guidelines) | **NOT LISTED** | — |
| **2022 JQL** | Listed | **B** |
| 2019 JQL | Not listed | — |

The journal *Risks* held a B rating in the 2022 ABDC list but was **dropped in the 2025 update**. Since the guidelines folder ships the 2025 edition (`ABDC-JQL-2025-v2-270526.xlsx`), the operative reference is presumably the 2025 list.

---

## 2. ABDC 2025-Rated Finance Journals (A*, A, B) Relevant to This Topic

Key journals in the **3502 (Finance)** FoR code from the 2025 ABDC list that publish FX / carry trade / exchange rate research:

| Journal | ABDC 2025 | Relevance |
|---------|-----------|-----------|
| *Journal of International Money and Finance* | **A** | Core FX/UIRP journal |
| *Journal of International Financial Markets, Institutions and Money* | **A** | International finance |
| *Global Finance Journal* | **A** | Global FX and risk |
| *Research in International Business and Finance* | **A** | International finance |
| *Finance Research Letters* | **A** | Short-format empirical finance |
| *Pacific-Basin Finance Journal* | **A** | Asia-Pacific focus |
| *International Finance* | **B** | International finance |
| *International Journal of Finance & Economics* | **B** | Finance & economics |
| *Journal of Multinational Financial Management* | **B** | Multinational finance |
| *Borsa Istanbul Review* | **B** | Broad finance |
| *Journal of Risk* | **B** | Risk-focused |
| *Journal of Banking & Finance* | **A\*** | Broad finance |
| *Journal of Financial Markets* | **A\*** | Financial markets |
| *Journal of Financial Stability* | **A\*** | Financial stability |
| *Annals of Finance* | **B** | General finance |
| *Journal of Emerging Market Finance* | **B** | Emerging markets |

---

## 3. Recommended Replacement: Beirne & Sugandi (2023)

**Beirne, J. & Sugandi, E. (2023).** Risk-off shocks and spillovers in safe havens. *Pacific-Basin Finance Journal*, 80, 102102. DOI: `10.1016/j.pacfin.2023.102102`

| Criterion | Status |
|-----------|--------|
| **Journal** | *Pacific-Basin Finance Journal* |
| **ABDC 2025 Rating** | **A** |
| **Topic** | Yen safe-haven, risk-off shocks, spillovers |
| **Methodology** | Country-specific structural VAR |
| **Japan focus** | Yes (alongside Switzerland and US) |
| **Data** | Public (IMF, BIS, national statistics) |
| **Replicability** | High — no Bloomberg required |
| **Published** | 2023 (recent, relevant) |

### Full Details

| Aspect | Detail |
|--------|--------|
| **Research Question** | What are the real and financial spillovers of risk-off shocks to safe haven destinations (Japan, Switzerland, US)? |
| **Methodology** | Country-specific structural VAR (SVAR) with theory-based identifying restrictions |
| **Model Equation** | $A_0 Y_t = \alpha + \sum_{j=1}^{p} A_j Y_{t-j} + \varepsilon_t$ |
| **Data Frequency** | Monthly (1990–2021) |
| **Data Source** | IMF, BIS, national statistics, ADB databases |
| **Core Variables** | Risk-off shock indicator, REER, industrial production, portfolio flows, economic policy uncertainty |
| **Identification** | Short-run restrictions from economic theory; risk-off shock as external financial shock |
| **Key Tools** | Structural impulse response functions, variance decomposition |
| **Key Findings** | (1) Yen REER appreciates significantly and persistently (~25 days) in risk-off episodes; (2) no significant portfolio flow effects on Japan; (3) negative real GDP spillover in Japan only; (4) no significant effect on Japan's economic policy uncertainty |

---

## 4. Methodology Comparison

### Side-by-Side: Guyot et al. (2026) vs. Beirne & Sugandi (2023)

| Dimension | Guyot et al. (2026) | Beirne & Sugandi (2023) |
|-----------|---------------------|------------------------|
| **ABDC 2025** | Not listed | **A-rated** |
| **Journal** | *Risks* (MDPI) | *Pacific-Basin Finance Journal* |
| **Research Question** | Do financial risk indicators explain JPY/USD deviations from UIRP? | What are spillovers of risk-off shocks to safe haven destinations? |
| **Methodology** | Reduced-form VAR + Cholesky decomposition | Structural VAR (theory-identified) |
| **Countries** | Japan-US (bilateral) | Japan, Switzerland, US (3 separate models) |
| **Data Frequency** | Daily | Monthly |
| **Sample Period** | 2018–2024 | 1990–2021 |
| **Observations** | 1,640 | ~372 per country |
| **Risk Variables** | VIX, $\Delta$Brent, risk reversals, bid-ask spread | Financial stress / risk-off shock index |
| **Other Variables** | $\Delta(i-i^*)$, $\Delta$YCurve$^{Diff}$, EGAP (S&P500 − TOPIX), $\Delta$JPY/USD | REER, industrial production, portfolio flows, EPU |
| **Data Source** | Bloomberg (proprietary) | IMF, BIS, national statistics (public) |
| **Identification** | Cholesky ordering (monetary policy → commodities → VIX → spread → risk rev. → EGAP → FX) | Short-run theory-based restrictions on SVAR |
| **Key Finding** | VIX and risk reversals Granger-cause JPY/USD returns; UIRP fails | Yen appreciates during risk-off; negative GDP spillover unique to Japan |
| **Replicability** | Requires Bloomberg | High — public data |

### Variable Mapping

| Guyot et al. Variable | Beirne & Sugandi Proxy |
|----------------------|------------------------|
| $\Delta$JPY/USD (bilateral) | REER (trade-weighted) |
| VIX | Financial stress / risk-off indicator |
| $\Delta$Brent | Not directly included |
| Bid-ask spread | Not directly included |
| Risk reversals | Not directly included |
| $\Delta(i-i^*)$ | Not directly included |
| EGAP (equity return differential) | Not directly included |
| N/A | Industrial production (GDP proxy) |
| N/A | Portfolio flows |
| N/A | Economic policy uncertainty (EPU) |

---

## 5. Cholesky Ordering Comparison

### Guyot et al. (2026) — Full Model Ordering

| Position | Variable | Rationale |
|----------|----------|-----------|
| 1 (most exogenous) | $\Delta$YCurve$^{Diff}$ | Monetary policy — changes slowly, no same-day FX reaction (Eichenbaum & Evans, 1995) |
| 2 | $\Delta(i-i^*)$ | Also monetary policy; central banks meet infrequently |
| 3 | $\Delta$Brent | Oil price set globally; Japan is price taker |
| 4 | VIX | US equity fear affects global risk sentiment |
| 5 | Spread | FX liquidity responds to global risk, not vice versa |
| 6 | RiskReversal | FX hedging demand responds to risk & liquidity |
| 7 | EGAP (S&P500 − TOPIX) | Equity returns respond to risk, then drive FX (Hau & Rey, 2006) |
| 8 (most endogenous) | $\Delta$JPY/USD | Exchange rate absorbs all shocks last |

### Beirne & Sugandi (2023) — SVAR Identification

SVAR with short-run restrictions. Variables ordered and identified as:
1. **External financial shock** (risk-off indicator / VIX / global financial stress)
2. **Domestic real activity** (industrial production)
3. **Exchange rate** (REER)
4. **Portfolio flows** (equity + debt)
5. **Economic policy uncertainty**

The key structural restriction is that the risk-off shock is identified as an **external factor** — contemporaneously affecting all domestic variables but not affected by them.

---

## 6. Implications for Replication

### Required Changes If Switching to Beirne & Sugandi

| Current Design (Guyot-based) | Required Change |
|-----------------------------------|-----------------|
| Daily frequency (2018–2024) | Monthly frequency (or adapt their framework to daily) |
| Reduced-form VAR with Cholesky | Keep VAR approach or adopt SVAR |
| 7-day impulse response horizon | Longer horizon (months) |
| VIX, Brent, spread, risk reversals, EGAP | Use risk-off shock index instead |
| UEP hypothesis (equity gap) | Drop equity gap; add real GDP and portfolio flows |
| Causal claim: "risk indicators → yen within 7 days" | Broader: "financial stress → yen appreciation + real spillovers" |
| Data: FRED + LSEG | Data: IMF IFS + BIS + national statistics |
| One bilateral rate (JPY/USD) | Can still focus on JPY (as one of 3 countries) |

### What Stays the Same

- **Japan / yen remains the core focus**
- **VAR framework** (reduced-form or structural)
- **Risk transmission channels** as the central mechanism
- **Carry trade dynamics** as motivation
- News article motivation (Japan, Iran war, yen sell-off) still directly relevant

---

## 7. Recommendations

### Option A: Switch to Beirne & Sugandi (2023) — Recommend 

| Pros | Cons |
|------|------|
| Pacific-Basin Finance Journal — A-rated in ABDC 2025 | Monthly data, not daily |
| Publicly available data | Requires redesign of variable set |
| Directly about yen safe-haven dynamics | SVAR identification more complex than Cholesky |
| Sample can be extended to 2022–2026 crisis period | |
| Recent (2023) and well-cited | |

### Option B: Keep Guyot et al. (2026) and confirm with professor

| Pros | Cons |
|------|------|
| Current design is built around this paper | Journal only has 2022 B-rating, not in 2025 ABDC list |
| Daily VAR with Cholesky already specified | Risk that professor rejects it |

### Option C: Find a third paper closer to your current design

Possible candidates to investigate further:
- **Berg & Mark (2018)** — *Measures of global uncertainty and carry-trade excess returns* — Journal of International Money and Finance (A-rated) — directly about carry trade
- **Cho, Hyde & Liu (2022)** — *The yen-dollar risk premium* — Journal of International Financial Markets, Institutions and Money (A-rated) — uses regime-switching rather than VAR
- **"Risk appetite, carry trade and exchange rates" (2012)** — Global Finance Journal (A-rated) — about yen carry trade and VIX — but uses VECM, not VAR

---

## 8. ABDC 2025 Journal Quality List Reference

The full ABDC 2025 list is available at:
- **Local:** `guidelines/ABDC-JQL-2025-v2-270526.xlsx`
- **Sheets:** 2025 JQL, 2022 JQL, 2019 JQL, 2016 JQL, 2013 JQL, 2010 JQL
- **Key columns:** Journal Title, Publisher, ISSN, FoR code, Rating

Finance journals are classified under FoR code **3502**.

---

## 9. ABDC Classification History of "Risks" (ISSN 2227-9091)

| ABDC Edition | Status | Rating | Notes |
|-------------|--------|--------|-------|
| **2025 JQL** | **NOT LISTED** | — | Dropped in the 2025 review |
| **2022 JQL** | Listed | **B** | Rated B |
| **2019 JQL** | Listed | **B** | Rated B |
| **2016 JQL** | Listed | **B** | Rated B |
| **2013 JQL** | Not listed | — | Journal launched in 2013, may have been too new or not yet evaluated |
| **2010 JQL** | Not listed | — | Pre-dates journal launch |

### Timeline Context

- **Risks journal launched:** 2013
- **Guyot et al. paper published:** February 2026
- **2025 ABDC JQL published:** May 2026 (~3 months after the paper)

The paper was published ~3 months *before* the 2025 ABDC JQL was finalized. Had the journal retained its B rating, it would have been clearly compliant. However, *Risks* was dropped during the 2025 review, making it non-compliant under the current list.

### Key Question for Professor

Does the guidelines requirement ("a journal with an A*, A, or B classification from the ABDC Journal Quality List") refer to:

1. **The ABDC edition in effect at the time of the paper's publication** (Feb 2026) — at which point the 2022 list was still the current edition, and *Risks* was B-rated 
2. **The most current ABDC edition available at the time of submission** (Aug 2026) — the 2025 list, where *Risks* is not listed 

This needs clarification with the instructor before proceeding.
