homework 2 is an assignment that will require the student to:

Based on a current event, identify a causal relationship that you would want to explore.
Explain why you would want to explore this causal relationship.
Submissions can be in slides (saved in PDF format (we will use latex)). The opening slide should be a news article that motivated the selection of the causal relationship of interest.
In studying the causal relationship, think of: (1) the ideal experiment; and (2) identification strategy (you may refer to a journal article for this). Don’t forget to cite the article that serves as your basis in the identification strategy.


Group 5 members:
Sison, Aaron Joshua E. #this is me
Galedo, Enrique Lorenzo 
Patajo, Juliana
Go, Keira
Cuenca, Raphael

My group (group5) wanna use this article for motivation of the study:

https://au.investing.com/news/economy-news/japan-brands-yen-falls-as-speculative-as-iran-war-ignites-selloff-4338553?fbclid=IwY2xjawSCNqJleHRuA2FlbQIxMABicmlkETFxWjlIczNHZ3lmYUhMd3h1c3J0YwZhcHBfaWQQMjIyMDM5MTc4ODIwMDg5MgABHs3Ssch2e1jIvV1mm-gp4u-QnfP_2dv2b0UiSWhPq9mGOOI1bh2DM5y4FDPS_aem_Yx-rLj_t9Wo-ZamEzWz--g

the md file for llm reading is @Assignments/Homework 2/markdowns/Japan brands yen falls as ’speculative’ as Iran war ignites sell-off By Reuters.md


This article will be used as a base article for the methodology (we are open to finding more)

the md file is @Assignments/Homework 2/markdowns/Risk Premiums, Market Volatility, and Exchange Rate Dynamics Evidence from the Yen Carry Trade.md

A little info:

Their paper examines the Uncovered Interest Rate Parity (UIRP) puzzle using daily data from 2018 to 2024. It provides a model for how to empirically analyze the yen carry trade, focusing on "risk premiums, liquidity conditions, and relative equity market performance". You can adopt their framework, extending their data to the 2025-2026 period to capture the current crisis, and refine their identification with the event-study approach detailed above.



The causal effect we wanna find out is:

A positive shock to financial risk indicators (specifically the VIX or FX risk reversals) causes an appreciation of the Japanese Yen against the US Dollar over a 7‑day horizon, operating through the unwinding of yen‑funded carry trades and portfolio rebalancing channels, even after controlling for interest rate differentials, oil prices, and FX liquidity



Data sources (please organize into a table)

Data	Source	How to Access
USD/JPY Exchange Rate	FRED (Federal Reserve Economic Data)	Use DEXJPUS series via fredapi or pyfredapi in Python.
Japanese Interest Rates	FRED or BOJ website	Use IRLTLT01JPM156N (long-term) and call BOJ's API for policy rates.
Global Asset Prices	Yahoo Finance	Use yfinance library for S&P 500, U.S. bond yields, etc.
Carry Trade Positions	BIS (Bank for International Settlements)	Download Japan's cross-border portfolio data from BIS or BoJ statistics site.
Oil Price Data	FRED	Use DCOILWTICO (WTI) series.
Geopolitical Risk Index	Matteo Iacoviello's Website	Download the GPR index, which is free and widely used in academic research.



The model Equation from the study
Y 
t
​
 =α+ 
j=1
∑
p−1
​
 Γ 
j
​
 Y 
t−j
​
 +e 
t
​


with cholesky ordering from exogenous to most endogenous:
Y 
t
​
 =[ΔYCurve 
Diff
 ,Δ(i−i 
∗
 ),ΔBrent,VIX,Spread,RiskReversal,EGAP,ΔJPY/USD] 
′

make sure to specifcy A variable can instantly affect variables below it, but cannot instantly affect variables above it.

Position	Variable	Can instantly affect ↓	Is affected instantly by ↑
1 (most exogenous)	ΔYCurve^Diff (yield curve change)	Variables 2–8	None
2	Δ(i-i*) (interest rate differential)	Variables 3–8	Variable 1
3	ΔBrent (oil price change)	Variables 4–8	Variables 1–2
4	VIX (equity fear gauge)	Variables 5–8	Variables 1–3
5	Spread (bid-ask spread)	Variables 6–8	Variables 1–4
6	RiskReversal (FX hedging cost)	Variables 7–8	Variables 1–5
7	EGAP (equity gap)	Variable 8	Variables 1–6
8 (most endogenous)	ΔJPY/USD (exchange rate)	None	Variables 1–7



Why This Ordering? (From the Paper, pp. 16–18)
The authors justify each placement based on economic theory:

Variable	Justification for Position
ΔYCurve^Diff	Monetary policy – changes very slowly, does not react to same‑day FX moves (Eichenbaum & Evans, 1995).
Δ(i-i*)	Also monetary policy; central banks meet infrequently.
ΔBrent	Oil price is set globally; Japan is a price taker.
VIX	US equity fear affects global risk sentiment; not driven by JPY liquidity.
Spread	FX liquidity responds to global risk, but not vice versa.
RiskReversal	FX hedging demand responds to risk & liquidity.
EGAP	Equity return difference responds to risk, then drives FX through portfolio rebalancing (Hau & Rey, 2006).
ΔJPY/USD	Most endogenous – exchange rate absorbs all shocks last.


Identification rationale (pp. 16–18):

Monetary policy variables (yield curve, interest rate differential) are most exogenous – they do not respond to same‑day exchange rate movements.

Commodity risk (Brent) affects all other markets but is not affected by FX liquidity.

Equity risk (VIX) affects FX risk and liquidity, but not vice versa.

FX liquidity (spread) affects FX risk, but not global risk.

FX risk (risk reversal) affects equity gap and exchange rate.

Equity gap (EGAP) affects exchange rate through portfolio rebalancing (UEP).

Exchange rate return is the most endogenous – it reflects all shocks.
Data frequency: Daily (1 Jan 2018 – 31 Dec 2024), sourced from Bloomberg (p. 11–12).

Key causal finding (p. 33, Figure 10):
Risk indicators (VIX, risk reversal) and equity gap Granger‑cause exchange rate returns, while the interest rate differential does not – confirming that indirect financial risk channels transmit shocks to the yen.



Citations should include articles journal article and data sources in apa7 organize into a .bib file 






Proposal Paper Outline

Introduction 
    (Souce Article for Motigvtation of the study)
    The research question and causal relationship
Related Literature (our source article)
        https://doi.org/10.3390/risks14030046
        Guyot, O., Montgomery, H. A., & Yang, P. (2026). Risk Premiums, Market Volatility, and Exchange Rate Dynamics: Evidence from the Yen Carry Trade. Risks, 14(2), 46.
        Data source	Bloomberg Terminal
        Methodology	Reduced‑form VAR with Cholesky decomposition
        Key finding	Risk indicators (VIX, risk reversals) and equity gap Granger‑cause JPY/USD returns, confirming indirect financial risk transmission channels for UIRP deviations.
Methodology
    How we will apply the methodology / of the source article for the methodology
        Make sure to specify any changes, adjustments (if specificed) vs the source and justifications
    Data Gathering (Since we lack bloomberg terminal)
        We'll make use of FRED API yfinance etc specificed
References (APA7 using bib)

Paper ends here