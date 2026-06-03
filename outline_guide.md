# HW2 Presentation Outline Guide

> **Purpose:** This document serves as a detailed content blueprint for another agent to integrate into the `hw2.tex` Beamer/presentation template. Each slide section specifies exactly what content to place, why it matters, and how to phrase it. The integrating agent should use this as the authoritative source for slide content.

---

## Slide 1 — Introduction: Motivating Event

### Slide Title
**Introduction: Why This Study?**

### Content (Bullet Points)

- **Motivating event:** On March 31, 2026, Japan's Finance Minister Satsuki Katayama branded the yen's sharp decline as "speculative" for the first time since the Iran war began, signaling Tokyo's readiness to intervene "on all fronts" (Reuters, 2026).
- **What happened:** Escalating Middle East tensions (Iran war, Strait of Hormuz disruption) ignited a **triple sell-off** in Japanese assets:
  - Yen plunged to near ¥160/USD
  - Nikkei 225 lost over 11% in March
  - 10-year JGB yield rose to levels unseen since 1999
- **Why it matters:** This crisis is a natural experiment in risk transmission — the yen's behavior during acute geopolitical stress violates the standard UIRP prediction (high-yield currencies should depreciate). Instead, risk-off dynamics drove yen *appreciation* through carry trade unwinding and safe-haven flows, exposing the **forward premium puzzle** in real time.
- **Significance for research:** The event creates an exogenous shock to VIX, oil prices, and FX risk reversals — three key risk indicators — allowing us to trace their causal impact on JPY/USD while interest rate differentials remained relatively stable.

### Speaker Notes (for reference)
> The key selling point: this is not just another exchange rate study. The March 2026 Iran war crisis provides a real-world, exogenous shock that cleanly isolates the risk transmission channels the literature has been theorizing about. When a geopolitical event simultaneously spikes oil prices, equity fear, and hedging costs — while monetary policy settings remain anchored — the data speaks louder than any model.

### Source
- Reuters article: "Japan brands yen falls as 'speculative' as Iran war ignites sell-off" (March 31, 2026)
- Cite as: `reuters2026japan` in `.bib`

---

## Slide 2 — Causal Relationship & Research Question

### Slide Title
**Causal Relationship & Research Question**

### Content (Bullet Points)

- **Causal relationship under investigation:**
  > A one-standard-deviation positive shock to financial risk indicators (VIX or FX risk reversals) causes a statistically significant appreciation of the Japanese Yen against the US Dollar within 2–3 days, with effects persisting over a 7-day horizon. This causal effect operates through two indirect transmission channels: (1) **unwinding of yen-funded carry trades** and (2) **safe-haven portfolio rebalancing** (Uncovered Equity Parity). The effect holds after controlling for changes in interest rate differentials, oil prices, bid-ask spreads, and relative equity returns.

- **Formal research question:**
  > What is the causal effect of exogenous shocks to financial risk indicators (VIX, oil price, and FX risk reversals) on the JPY/USD exchange rate, operating through yen-funded carry trade unwinding and safe-haven demand channels, after controlling for interest rate differentials, FX liquidity, and relative equity performance?

- **Base article for methodology:**
  > Guyot, O., Montgomery, H. A., & Yang, P. (2026). Risk Premiums, Market Volatility, and Exchange Rate Dynamics: Evidence from the Yen Carry Trade. *Risks*, 14(2), 46. https://doi.org/10.3390/risks14030046

  - **Method adopted:** Reduced-form VAR with Cholesky decomposition
  - **Key finding replicated/extended:** Risk indicators (VIX, risk reversals) and equity gap Granger-cause JPY/USD returns, while interest rate differentials do not — confirming indirect financial risk transmission channels
  - **Our extension:** We extend the sample to include the 2025–2026 Iran crisis period and substitute Bloomberg Terminal data with public APIs (FRED, Yahoo Finance, MOF Japan, BIS, Iacoviello GPR) to ensure reproducibility

### Speaker Notes
> Emphasize that this is not just a replication. The 2025–2026 extension captures *extreme* stress conditions absent from Guyot et al.'s (2026) sample (which ends Dec 2024). This lets us test whether the carry trade unwinding channel holds under severe geopolitical shock, or whether Brunnermeier et al.'s (2009) VIX threshold nonlinearity attenuates the effect.

---

## Slide 3 — The Ideal Experiment

### Slide Title
**The Ideal Experiment**

### Content (Bullet Points)

- **Definition:** An ideal experiment establishes clear cause-and-effect relationships by scientifically manipulating variables while controlling external factors. It requires three core pillars:

- **Pillar 1 — Random Assignment:**
  - Randomly assign trading days (or currency-market sessions) to a "treatment" group that receives an exogenous risk shock (e.g., a sudden VIX spike) and a "control" group that does not.
  - Randomization ensures that observed differences in JPY/USD returns are attributable to the shock, not to pre-existing differences between groups.

- **Pillar 2 — Control Group:**
  - A baseline set of observations where no risk shock occurs, allowing us to measure the *counterfactual* — what JPY/USD would have done in the absence of the shock.
  - In our context: compare JPY/USD behavior on "normal" days (low VIX, stable oil, narrow risk reversals) vs. "shock" days (high VIX, oil spike, wide risk reversals).

- **Pillar 3 — Manipulation of the Independent Variable:**
  - The researcher *exogenously* varies the risk indicator (e.g., VIX level, risk reversal magnitude) and observes the resulting change in the dependent variable (JPY/USD return).
  - The ideal manipulation would hold all other variables constant (interest rate differentials, liquidity, equity gap) while varying only the risk shock.

- **Why the ideal experiment is infeasible:**
  - We cannot *randomly assign* geopolitical risk events or manipulate VIX levels in real financial markets.
  - Exchange rates are determined by simultaneouse interactions across thousands of market participants — no experimenter can control the treatment.
  - This infeasibility motivates our **identification strategy**, which uses observational data and econometric assumptions to approximate the ideal experiment.

### Speaker Notes
> This slide is critical for establishing *why* we need an identification strategy. The ideal experiment sets the standard; the identification strategy explains how we get as close as possible with observational data. Make the three pillars crystal clear — they are the benchmark against which our method is evaluated.

---

## Slide 4 — Identification Strategy

### Slide Title
**Identification Strategy**

### Content (Bullet Points)

- **Definition:** An identification strategy is the specific set of assumptions and research designs used to isolate and measure a true causal effect from observational data — approximating the ideal experiment when random assignment is impossible.

- **Our strategy: Recursive (Cholesky)VAR identification** (based on Guyot et al., 2026)

  - **Core assumption:** A Wold causal ordering of variables from most exogenous to most endogenous. A variable at position *k* can contemporaneously affect variables at positions *k+1* through *8*, but cannot instantaneously affect variables at positions *1* through *k−1*.

  - **Variable ordering and economic justification:**

    | Pos. | Variable | Justification |
    |------|----------|---------------|
    | 1 | ΔYCurve^Diff | Monetary policy changes slowly; does not react to same-day FX (Eichenbaum & Evans, 1995) |
    | 2 | Δ(i − i*) | Central banks meet infrequently; same-day FX cannot move policy rates |
    | 3 | ΔBrent | Global oil prices are exogenous to JPY; Japan is a price taker |
    | 4 | VIX | US equity fear index reflects global risk; not driven by JPY liquidity |
    | 5 | Spread | FX liquidity responds to global risk, not vice versa |
    | 6 | RiskReversal | FX hedging demand responds to risk and liquidity |
    | 7 | EGAP | Equity return gap responds to risk, then drives FX via portfolio rebalancing (Hau & Rey, 2006) |
    | 8 | ΔJPY/USD | Most endogenous — the exchange rate absorbs all contemporaneous shocks |

  - **Key identification restrictions:**
    1. Monetary policy variables (positions 1–2) are ** contemporaneously exogenous** to same-day FX movements
    2. Global risk factors (positions 3–4) affect FX but are not caused by FX within the same day
    3. FX microstructure variables (positions 5–6) respond to risk but do not cause global risk
    4. The exchange rate (position 8) is the **residual clearing price** — it absorbs all contemporaneous shocks

- **Novel extension — GPR subsample segmentation:**
  - We use Iacoviello's daily Geopolitical Risk (GPR) index to classify trading days as "High Stress" (GPR > 90th percentile) vs. "Normal," enabling **subsample VAR estimation** that tests for nonlinear regime-dependent transmission (addressing Brunnermeier et al., 2009's VIX threshold finding).

- **Causal inference tests:**
  - **Granger causality:** Test whether risk indicators predict JPY/USD returns beyond lagged returns
  - **Orthogonalized IRFs:** Trace the dynamic response of JPY/USD to a one-SD shock in VIX/risk reversal
  - **FEVD:** Decompose forecast error variance of JPY/USD into fractions attributable to each shock

### Speaker Notes
> Walk through the ordering slowly — each position is there for a reason grounded in institutional microstructure. The key insight: by placing the exchange rate last, we assume it is the most endogenous variable, absorbing all contemporaneous shocks. This is the standard FX microstructure assumption (Evans & Lyons, 2002). The GPR subsample is our original contribution — it tests whether the transmission channels behave differently under extreme geopolitical stress.

---

## Slide 5 — Dataset

### Slide Title
**Data Sources & Variable Construction**

### Content (Table — adapt from `tab:datasources` in `hw2.tex`)

| Variable | Proxy / Series Code | Source | Retrieval Method | Notes |
|----------|---------------------|--------|------------------|-------|
| ΔJPY/USD | DEXJPUS (FRED), USDJPY=X (Yahoo) | FRED, Yahoo | pandas-datareader, yfinance | 2026-06-01 |
| Δ(i − i*) | Japan 1Y JGB (MOF), DFF (US Fed Funds) | MOF Japan, FRED | pandas-datareader, web CSV | Substituted 1Y JGB for call rate⁽ᵃ⁾ |
| ΔYCurve^Diff | MOF JGB 10Y/2Y; DGS10/DGS2 (US) | MOF Japan, FRED | pandas-datareader, web CSV | 2026-06-01 |
| ΔBrent | DCOILWTICO (WTI), BZ=F (Brent) | FRED, Yahoo | pandas-datareader, yfinance | WTI primary; Brent for robustness |
| VIX | CBOE Volatility Index (^VIX) | Yahoo Finance | yfinance | Used as level (ADF-stationary) |
| Spread | JPY/USD Bid-Ask (OANDA); proxy (H−L)/C | OANDA, Yahoo | OANDA API, yfinance | Pending OANDA; using intraday range proxy⁽ᵃ⁾ |
| RiskReversal | 1-Month JPY/USD 25-Δ Risk Reversal | BIS (quarterly) | BIS Explorer (manual) | Cubic spline interpolation to daily⁽ᵇ⁾ |
| EGAP | Nikkei 225 (^N225), S&P 500 (^GSPC) | Yahoo Finance | yfinance | 2026-06-01 |
| GPR | Geopolitical Risk Index (daily) | Iacoviello (2026) | XLSX → CSV | To 2026-05-26; subsample segmentation only |

**Notes:**

- ⁽ᵃ⁾ **Data Substitution:** The original Guyot et al. (2026) study used Bloomberg Terminal data. Daily Japanese short-term bank rates are unavailable from public APIs (FRED publishes them only monthly); we substitute the 1Y JGB yield from MOF Japan. For the spread, pending OANDA API access, we use the intraday range proxy (High − Low) / Close, a standard liquidity proxy (Corwin & Schultz, 2012; Goyenko et al., 2009).

- ⁽ᵇ⁾ **Data Limitation:** The 1-month JPY/USD 25-delta risk reversal is published only at quarterly frequency by BIS. We interpolate to daily via cubic spline, flagging this as a limitation relative to Bloomberg-sourced daily data.

- **Sample period:** January 1, 2018 – May 31, 2026 (~2,100 trading days before alignment; ~1,800–2,000 after alignment)
- **Alignment:** Retain only dates where both NYSE and TSE are open, following Guyot et al. (2026, p. 11)

### Speaker Notes
> Emphasize that ALL data is from free, publicly accessible sources. This is a deliberate design choice — we prove the methodology is reproducible without a $24,000/year Bloomberg Terminal. The key limitation is the risk reversal interpolation; flag it honestly.

---

## Slide 6 — References (APA 7th Edition)

### Slide Title
**References**

### Content (Bibliographic Entries — APA 7 format)

> These entries should be added to `references.bib` in APA 7 style using `biblatex` with `style=apa`.

1. **Guyot, O., Montgomery, H. A., & Yang, P.** (2026). Risk premiums, market volatility, and exchange rate dynamics: Evidence from the yen carry trade. *Risks*, *14*(2), 46. https://doi.org/10.3390/risks14030046

2. **Brunnermeier, M. K., Nagel, S., & Pedersen, L. H.** (2009). Carry trades and currency crashes. *NBER Macroeconomics Annual*, *23*(1), 313–347. https://doi.org/10.1086/593086

3. **Eichenbaum, M., & Evans, C. L.** (1995). Some empirical evidence on the effects of shocks to monetary policy on exchange rates. *The Quarterly Journal of Economics*, *110*(4), 975–1009. https://doi.org/10.2307/2946646

4. **Engel, C.** (2016). Exchange rates, interest rates, and the risk premium. *American Economic Review*, *106*(2), 436–474. https://doi.org/10.1257/aer.20121349

5. **Evans, M. D. D., & Lyons, R. K.** (2002). Order flow and exchange rate dynamics. *Journal of Political Economy*, *110*(1), 170–180. https://doi.org/10.1086/324345

6. **Gagnon, J. E., & Chaboud, A. P.** (2007). What can the data tell us about carry trades? *International Journal of Finance & Economics*, *12*(2), 160–180. https://doi.org/10.1002/ijfe.311

7. **Habib, M. M., & Stracca, L.** (2012). Getting beyond carry trade: What makes a safe-haven currency? *Journal of International Economics*, *87*(1), 50–64. https://doi.org/10.1016/j.jinteco.2011.12.011

8. **Hau, H., & Rey, H.** (2006). Exchange rates, equity prices, and capital flows. *The Review of Economic Studies*, *73*(1), 273–292. https://doi.org/10.1111/j.1467-937X.2006.00379.x

9. **Lee, K. K.** (2017). Safe-haven currencies: What makes for a safe-haven currency? *International Review of Economics & Finance*, *48*, 205–219. https://doi.org/10.1016/j.iref.2016.12.001

10. **Masujima, Y., & Sato, K.** (2024). Drivers of the yen exchange rate: Time-varying parameter and CEE approach. *Journal of the Japanese and International Economies*, *63*, 101244. https://doi.org/10.1016/j.jjie.2024.101244

11. **Reuters.** (2026, March 31). Japan brands yen falls as 'speculative' as Iran war ignites sell-off. *Reuters*. [News article]

12. **FRED.** (2026). Federal Reserve Economic Data. Federal Reserve Bank of St. Louis. Retrieved June 1, 2026, from https://fred.stlouisfed.org/

13. **Iacoviello, M.** (2026). Geopolitical Risk Index (daily). Retrieved May 26, 2026, from https://www.matteoiacoviello.com/gpr.htm

14. **BIS.** (2026). BIS Statistics Explorer. Bank for International Settlements. Retrieved June 1, 2026, from https://stats.bis.org/

15. **Corwin, S. A., & Schultz, P.** (2012). A simple way to estimate bid-ask spreads from daily high and low prices. *The Journal of Finance*, *67*(2), 719–759. https://doi.org/10.1111/j.1540-6261.2012.01729.x

16. **Goyenko, R. Y., Holden, C. W., & Trzcinka, C. A.** (2009). Do liquidity measures measure liquidity? *Journal of Financial Economics*, *92*(2), 153–181. https://doi.org/10.1016/j.jfineco.2008.06.002

17. **Bollerslev, T., & Melvin, M.** (1994). Bid-ask spreads and volatility in the foreign exchange market. *Journal of International Economics*, *36*(3–4), 355–372. https://doi.org/10.1016/0022-1996(94)90010-5

### Speaker Notes
> All references must be in a proper `references.bib` file with APA 7 style. The `biblatex` package with `style=apa` handles formatting automatically. Ensure DOIs are included for all journal articles.

---

## Integration Notes for the Agent

### What the integrating agent needs to do:

1. **Read `hw2.tex`** to understand the current document structure, preamble, and macro definitions.
2. **This is a presentation/slides assignment** — verify with the user whether they want Beamer slides or continue with the article format. The instructions say "submissions can be in slides (saved in PDF format using LaTeX)."
3. **If Beamer slides:** Convert each slide section above into `\begin{frame}...\end{frame}` environments with appropriate `frametitle` and `itemize` environments.
4. **If article PDF (current `hw2.tex` format):** Each "slide" section maps to a `\section` or `\subsection` with appropriate headings and paragraph text.
5. **The `references.bib` file** must be created or updated with all 17 entries above.
6. **Tables** should use the existing `booktabs`/`tabularx`/`threeparttable` infrastructure in the preamble.
7. **The Cholesky ordering table** uses the exact format from `tab:cholesky` in the existing `hw2.tex`.
8. **All citations** should use `\parencite{}` and `\textcite{}` commands (already set up with `biblatex` APA style).

### Key Design Decisions (already made):

- **Causal relationship:** As stated in Slide 2 — this is non-negotiable per the group's decision.
- **Base article:** Guyot et al. (2026) — the methodology must reference this explicitly.
- **Extension:** Adding GPR subsample (2025–2026 Iran crisis period) and replacing Bloomberg data with public sources.
- **Ideal experiment section:** Must prominently feature the three pillars (random assignment, control group, manipulation of IV).
- **Identification strategy:** Cholesky decomposition with the specific 8-variable ordering justified by institutional microstructure theory.