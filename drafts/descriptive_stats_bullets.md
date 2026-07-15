Descriptive Statistics - Key Points

Source: data/processed/descriptive_stats.csv (rendered in data_pipeline.qmd)

The Risk-off (VIX-based binary indicator) mean fell from 3.2% to 1.9% of trading days. Fewer systemic crises in the extended period. Its standard deviation compressed from 0.176 to 0.137, consistent with shorter VIX spike durations.

The Spread (JGB 10Y - US Treasury 10Y) mean widened from -2.44 to -2.70 as the Fed hiked while the BOJ remained pinned to YCC. Its standard deviation compressed from 0.93 to 0.77. The spread was policy-capped, not free-floating.

The Log Nikkei (log of Nikkei-225) mean rose from 9.56 to 10.46 (roughly 2.5x in levels) while its standard deviation dropped from 0.33 to 0.24. A post-2021 bull market with fewer crash episodes.

The Log REER (log real effective exchange rate) mean collapsed from 4.52 to 4.07 (~36% real depreciation in levels) with the standard deviation halving from 0.171 to 0.091. A one-way depreciation rather than the two-sided volatility of the paper period.

The Log RGDP (log real GDP) mean edged up from 13.19 to 13.28, but its standard deviation collapsed from 0.051 to 0.009 (F = 31.14). The paper period contained the GFC, 2011 earthquake, and COVID. The extended period is a flat post-pandemic recovery.

The Log WUI (log World Uncertainty Index for Japan) mean became slightly more negative (-1.80 to -1.98) while its standard deviation nearly doubled from 0.59 to 1.08. Uncertainty became more bimodal. Sharper spikes, deeper troughs.

The Debtsec %GDP (net portfolio debt inflows) mean halved from 0.52% to 0.18% of GDP, while its standard deviation increased from 1.72 to 2.42. The only variable where the extended period is more volatile (F = 0.50, p < .0001). Consistent with carry-trade disruption from YCC exit uncertainty.

The Equity %GDP (net portfolio equity inflows) means are nearly identical (0.22 to 0.17) with comparable standard deviations (1.16 to 1.32). Equity flows were stable across regimes.

The Other %GDP (net other investment inflows) mean nearly tripled from 0.39 to 1.13 with standard deviation rising from 3.16 to 4.40. Driven by yen carry-trade expansion.

The Direct %GDP (net direct investment inflows) mean more than doubled from 0.11 to 0.25 with standard deviation rising from 0.29 to 0.44. Consistent with continued outward FDI.

F-Test Summary (1999-2021 vs 2021-2026)

Variable: log_rgdp | F: 31.14 | Higher variance in: Paper Period
Variable: log_reer | F: 3.52 | Higher variance in: Paper Period
Variable: log_nikkei | F: 1.84 | Higher variance in: Paper Period
Variable: spread | F: 1.45 | Higher variance in: Paper Period
Variable: debtsec_pct | F: 0.50 | Higher variance in: Extended Period

All five significant at p < 0.0001. The paper period dominates GDP, FX, equity, and spread variance. Debt portfolio flows invert the pattern. The extended period is structurally more volatile there.

What the F-statistic means

The F-statistic is the ratio of the paper period variance to the extended period variance. F = 1 means equal variance. F > 1 means the paper period had higher variance. F < 1 means the extended period had higher variance.

log_rgdp (F = 31.14): The paper period had 31x the GDP variance of the extended period. The paper period contains the GFC, 2011 earthquake, and COVID. The extended period is a flat recovery.

log_reer (F = 3.52): The paper period had 3.5x the REER variance. The yen swung both ways during 1999-2021. After 2021 it was a one-way depreciation.

log_nikkei (F = 1.84): The paper period had 1.84x the equity variance. Crashes and recoveries in the paper period vs a steady bull run post-2021.

spread (F = 1.45): The paper period had 1.45x the spread variance. The spread was more volatile when the BOJ was not capping yields.

debtsec_pct (F = 0.50): The extended period had 2x the variance of the paper period (1 / 0.50 = 2). Debt flows became more volatile after 2021, not less.

The p-value (< 0.0001 for all five) means the probability of observing an F this extreme if the two periods actually had equal variance is less than 0.01%. These variance differences are not noise. They reflect a real structural change in the data-generating process between the two periods.
