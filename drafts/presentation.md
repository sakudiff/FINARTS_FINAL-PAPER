FINARTS C01
PROGRESS REPORT

GROUP 4
Sison, Opiana, Galedo, Patajo, Go, Cuenca

JULY 17, 2026

CHOSEN ARTICLE & Methodology
Beirne, J. & Sugandi, E. (2023). Risk-off shocks and spillovers in safe havens. Pacific-Basin Finance Journal, 80, 102102.
Model: Country-Specific Structural Vector Autoregression (SVAR)
Same model per country

Identification Strategy: Cholesky Decomposition
Orders variables from most exogenous (external global shocks) to most endogenous (domestic capital flows).

Variable Ordering
1.Global Shocks: Risk-off binary, Log(WUI)
2.Financial Markets: Yield Spread, Log(Nikkei 225)
3.Macroeconomy: Log(RGDP), Log(REER)
4.Capital Flows (% GDP): Debtsec, Equity, Other, Direct
Hypothesis from the Paper
H1: Global risk-off shocks lead to a sharp appreciation of the Japanese Yen.
H2: Risk-off shocks do not trigger significant physical portfolio capital inflows into Japan.
H3: Global risk-off shocks cause negative spillovers to Japan's real economy (GDP contraction).

2

Replication Modifications - Sample & Scope Replication Modifications
Scope Shift:
Focusing exclusively on Japan (removing Switzerland and the US comparisons)
To isolate and retest the "Safe Haven Yen" theory.
Extended the original sample (1999–2021) up to June 30, 2026
This extension captures recent macroeconomic anomalies, including:
Historic Yen depreciation
BOJ policy normalization and rate hikes
Recent risk-off episodes (e.g., Iran conflict, carry trade unwind)
"America First" Trade Policies
BOJ Normalization vs. Global Pressures
Record Currency Interventions
Data
Higher Frequency Data:
Replaced the original paper's quarterly IMF/CEIC sourced capital flow data with monthly Bank of Japan (BOJ) sourced data.
Direct Central Bank Sourcing & LSEG / Bloomberg

2

Variables, Data, & Data Source

DATA PIPELINE & FEATURE
ENGINEERING
Filtered raw series to 1999-01-14–2026-06-30, anchoring daily financials to
VIX via left_join to preserve US trading days and accurate risk_off triggers.
Computed risk_off (VIX MA60+10), spread (JGB10Y - US10Y), and logtransformed Nikkei
Shift-JIS encoded BOJ files (1999–2013) using readLines, mapping Japanese
eras (Heisei/Reiwa) to Gregorian years
Combined cut off datasets 1999-2014 + 2014-2026
Converted "-" to NA_real_ in JGB yields, filtered zero WUI before logging, and
used full_join to preserve variable-specific temporal ranges without truncation
Converted 100M JPY BOJ flows and millions-JPY nominal GDP to USD billions
using EOM USD/JPY, expanding quarterly GDP to monthly via complete() and
forward-fill..
Exported all native-frequency raw files unfiltered (retaining pre-1999 data) to
supply boundary anchors for the quadratic spline and prevent artificial
extrapolation.
Transformed low-frequency variables to daily frequency using Python's
pandas.interpolate(method='quadratic')
Applied lubridate::wday() %in% 2:6 to restrict the interpolated daily calendar to
Monday–Friday trading days.
Merged ten endogenous variables via date-based full_join

≥

See full pipeline here

https://finalprojectfinartsg4.netlify.app/#variablereference

Descriptive Statistics
Sample: 7,164 trading days (5,795 paper / 1,369 extended) after data alignment
The Risk-off (VIX-based binary indicator) mean fell from 3.2% to 1.9% of trading days. Fewer systemic crises in the extended
period.
Its standard deviation compressed from 0.176 to 0.137, consistent with shorter VIX spike durations.
The Spread (JGB 10Y - US Treasury 10Y) mean widened from -2.44 to -2.70 as the Fed hiked while the BOJ remained pinned
to YCC.
The spread was policy-capped, not free-floating.
The Log Nikkei (log of Nikkei-225) mean rose from 9.56 to 10.46 (roughly 2.5x in levels) while its standard deviation dropped
from 0.33 to 0.24.
A post-2021 bull market with fewer crash episodes.
The Log REER (log real effective exchange rate) mean collapsed from 4.52 to 4.07 (~36% real depreciation in levels) with the
standard deviation halving from 0.171 to 0.091.
A one-way depreciation rather than the two-sided volatility of the paper period.
The Log RGDP (log real GDP) mean edged up from 13.19 to 13.28, but its standard deviation collapsed from 0.051 to 0.009 (F
= 31.14).
The paper period contained the GFC, 2011 earthquake, and COVID. The extended period is a flat post-pandemic
recovery.
The Log WUI (log World Uncertainty Index for Japan) mean became slightly more negative (-1.80 to -1.98) while its standard
deviation nearly doubled from 0.59 to 1.08. Uncertainty became more bimodal.
Sharper spikes, deeper troughs.
The Debtsec %GDP (net portfolio debt inflows) mean halved from 0.52% to 0.18% of GDP.
The only variable where the extended period is more volatile (F = 0.50, p < .0001).
The Equity %GDP (net portfolio equity inflows) means are nearly identical (0.22 to 0.17).
Stable equity flows across regimes.
The Other %GDP (net other investment inflows) mean more than doubled (0.39 to 1.13).
Driven by yen carry-trade expansion.
The Direct %GDP (net direct investment inflows) mean and SD more than doubled.
Consistent with continued outward FDI.

F Statistic

The paper period had 3.5x the REER variance. The yen swung both ways during 1999-2021. After 2021 it was a one-way depreciation.
The paper period had 1.84x the equity variance. Crashes and recoveries in the paper period vs a steady bull run post-2021.
The paper period had 1.45x the spread variance. The spread was more volatile when the BOJ was not capping yields.
The extended period had 2x the variance of the paper period (1 / 0.50 = 2). Debt flows became more volatile after 2021, not less.
The paper period had 31x the GDP variance of the extended period.
This contains the GFC, 2011 earthquake, and COVID.
The extended period is a flat recovery.

4

All three series exhibit significant temporal
heteroskedasticity (volatility clustering).
Log_nikkei Shows high volatility spikes corresponding
to the 2008 and 2013-2016.
Post-2021, underlying base volatility appears lower
than the historical extended period.
Log_reer has massive spikes in 2008 and 2015, but
from roughly 2021 onward, its 260-day standard
deviation compressed
Spread shows a drastic shrinkage in rolling volatility
after 2021 compared to the high, erratic variations
seen in the 2000–2005 and 2010–2020 periods.

While the title states "wider dispersion after 2021", a statistical
inspection reveals this is variable-dependent.
log_rgdp, log_nikkei, and log_reer display a dramatic narrowing of
distribution width
For log_rgdp, the orange curve is an extremely tall, leptokurtic
spike centered around 13.27, indicating massively reduced
variance.
Log_nikkei shows a pronounced rightward shift (higher mean value)
with a narrower, potentially bi-modal distribution in the recent
period.
log_reer exhibits a sharp leftward shift (depreciation/devaluation).
The variables log_wui and debtsec_pct show marked platykurtosis
Confirms overall capital flow variables have become more
widely dispersed in the later period.

log_nikkei and log_reer are clearly multimodal, reflecting distinct
historical currency and equity regimes.
log_rgdp is highly non-normal (likely bimodal), driven by the
structural economic shock and subsequent growth.
The spread variable shows a heavy left tail
Direct_pct and other_pct are leptokurtic with a massive spike near
zero
risk_off is a binary state variable, rendered as an exponentiallooking decay from zero.

A definitive regime shift occurs at the vertical line (approximately March
31, 2021).
log_nikkei shows a steep and persistent positive drift post-2021 that breaks
from its prior historical trend.
log_reer shows a sharp, nearly vertical drop at the break point, settling
onto a lower, relatively flat trendline, highlighting a stark structural break in
Japanese competitiveness.
spread establishes a new, lower equilibrium (more negative values) after
2021.
log_rgdp shows a sharp COVID-19 drop followed by a steep recovery, but
the post-2021 is relatively stable compared to the baseline.
debtsec_pct, equity_pct, and other_pct exhibit significantly increased highfrequency oscillations after 2021, reinforcing the distributional widening
observed in the 999–2021 vs. 2021–2026 figure density.

Real GDP, Real Effective Exchange Rate, and the Nikkei 225
suffer from extreme multicollinearity.
Economic growth shares a -0.92 correlation with the Real
Effective Exchange Rate, demonstrating that growth is
almost perfectly associated with a weaker yen.
The Yen and Nikkei share a -0.82 correlation, proving that a
depreciated yen strongly drives equity market valuations.
The risk-off binary variable exhibits near-zero correlation with
the macro series, verifying that global panic shocks act as
independent and idiosyncratic tail-events rather than moving
linearly with the domestic baseline.
Regressing GDP, REER, and the Nikkei against each other
simultaneously will trigger severe multicollinearity

NEXT STEPS
Run the formal Structural Vector Autoregression (SVAR) estimations in R (or python), determine optimal lag lengths via AIC/BIC, and
generate Impulse Response Functions (IRFs) to track shock propagation.
Execute Granger causality tests and compute Forecast Error Variance Decomposition (FEVD) to isolate how much of the Yen's
movement is driven by external risk-off shocks versus domestic fundamentals.
Integrate new theoretical frameworks into the literature review specifically addressing the 2022–2026 Yen carry trade unwind and the
Bank of Japan's extreme monetary divergence.
Draft the results section with a focus on comparing the 1999–2021 baseline against the post-2021 structural break to test the modern
safe-haven hypothesis.
Compile the entire R-based data pipeline and statistical outputs via Quarto into a fully reproducible PDF appendix for the final August
submission.

2

The End

THANK YOU FOR LISTENING

GROUP 4
Sison, Opiana, Galedo, Patajo, Go, Cuenca

JULY 17, 2026

