# PRESENTATION SCRIPT — FINARTS C01 Progress Report

## Group 4: Sison, Opiana, Galedo, Patajo, Go, Cuenca

### July 17, 2026 \| \~14 minutes

------------------------------------------------------------------------

## SLIDE 1 — TITLE

**\[0:00 – 0:30\]**

Good afternoon. We're Group 4, and this is our progress report on the replication and extension of Beirne and Sugandi's 2023 paper on risk-off shocks and safe haven spillovers, published in the *Pacific-Basin Finance Journal*.

Our central question is simple: Is the Japanese Yen still a safe haven? The paper said yes — for the period 1999 to 2021. We test whether that claim survives the chaos of the last five years.

------------------------------------------------------------------------

## SLIDE 2 — CHOSEN ARTICLE & METHODOLOGY

**\[0:30 – 2:00\]**

The original paper uses a country-specific Structural Vector Autoregression — an SVAR — estimated separately for Japan, Switzerland, and the United States. Identification comes from Cholesky decomposition. The variables are ordered from most exogenous to most endogenous.

Here's the logic of that ordering. At the top sits the risk-off binary — a global panic indicator constructed from VIX spikes. It affects everything downstream but nothing domestic affects it. Next comes the World Uncertainty Index. Then financial markets respond: the yield spread and the Nikkei. Then the real economy: GDP and the real effective exchange rate. Finally, at the bottom, the slowest-moving variables: the four capital flow components — portfolio debt, portfolio equity, other investment, and direct investment.

The paper's three hypotheses: H1 — risk-off shocks cause the yen to *appreciate*. That's the classic safe haven story. H2 — these shocks do *not* trigger significant physical capital inflows. The yen moves, but money doesn't actually chase it. H3 — risk-off shocks cause negative spillovers to Japan's real economy. GDP contracts even as the currency strengthens.

These three hypotheses form the spine of everything that follows.

------------------------------------------------------------------------

## SLIDE 3 — REPLICATION MODIFICATIONS

**\[2:00 – 3:00\]**

We made three deliberate modifications.

First, scope. The original paper compared Japan, Switzerland, and the US. We focus exclusively on Japan. This lets us isolate and stress-test the "Safe Haven Yen" theory with far more granularity than a three-country comparison would allow.

Second, time. The original sample stopped in 2021. We extended it through June 2026 — capturing five additional years that include historic yen depreciation to 160 per dollar, the BOJ's exit from yield curve control and its first rate hikes in 17 years, the Iran-Israel conflict escalation, the August 2024 carry trade unwind that erased 4 trillion dollars in global equity in three days, "America First" trade policy shocks, and record currency intervention by the Ministry of Finance — 9.8 trillion yen in 2024 alone.

If the yen was ever going to stop being a safe haven, this was the stress test.

Third, data quality. The original paper used quarterly IMF capital flow data. We replaced it with monthly Bank of Japan data — sourced directly from the central bank's balance of payments API and historical Shift-JIS encoded files. This gives us three times the temporal resolution on the very variables that sit at the heart of the safe haven question.

------------------------------------------------------------------------

## SLIDE 4 — VARIABLES, DATA, & DATA SOURCE

**\[3:00 – 3:45\]**

This table maps each of the ten endogenous variables to its source. Risk-off is constructed from the VIX, sourced via LSEG. World Uncertainty Index from Ahir, Bloom, and Furceri's project. The spread is the 10-year JGB minus the 10-year US Treasury. The Nikkei, REER, and GDP come from LSEG and FRED. And the four capital flow variables — debt securities, equity, other investment, and direct investment — come from the Bank of Japan.

Every variable in this table is collected, cleaned, and aligned. No gaps remain. The data construction is fully reproducible — the pipeline is live at the URL on the slide.

------------------------------------------------------------------------

## SLIDE 5 — DATA PIPELINE & FEATURE ENGINEERING

**\[3:45 – 5:00\]**

I want to walk you through what's happening under the hood, because the pipeline is where most replications fail.

The raw inputs are heterogeneous in every dimension: frequency, encoding, currency, calendar. The pipeline has to reconcile all of this before a single regression can run.

Step one: we anchor all daily series to VIX trading days. VIX defines the calendar because risk-off is our primary shock. A left join ensures we preserve only US market days — no Japanese holidays injecting artificial gaps.

Step two: the risk-off binary. We compute a 60-day moving average of VIX and flag any day where VIX exceeds that average by 10 percentage points. This gives us a clean, replicable panic indicator — no discretionary crisis dating.

Step three: the BOJ historical data. Pre-2014 files are Shift-JIS encoded with Japanese era names — Heisei, Reiwa. We parse those, map to Gregorian dates, and merge with the 2014–2026 API data into a continuous monthly series from 1996.

Step four: unit harmonization. BOJ reports in 100-million yen. Nominal GDP from FRED is in millions of yen. We convert everything to billions of US dollars using end-of-month USD/JPY rates. Capital flows become percentages of GDP — exactly as the original paper specified.

Step five: frequency alignment. The biggest technical challenge. We have daily, monthly, and quarterly native frequencies. All must be daily for the Structural Vector Autoregression SVAR We use quadratic spline interpolation — pandas, not R, because R has no native quadratic spline — to upscale quarterly and monthly series to daily. Then we apply a weekday filter to restrict to Monday-through-Friday trading days, which removes the artificial weekend observations that linear interpolation would create.

Step six: the merge. Ten endogenous variables joined by date. 7,164 trading days — 5,795 from the paper's original window, 1,369 from our extension.

The key architectural decision: we export all raw files at native frequency, unfiltered, pre-1999 data included. Why? Because quadratic splines need boundary anchors. If you truncate before interpolating, the spline extrapolates at the edges — garbage in the first and last observations. Feeding pre-1999 data as left-boundary anchors prevents this. It's a detail that would never survive a cursory replication but would silently corrupt every impulse response.

------------------------------------------------------------------------

## SLIDE 6 — DESCRIPTIVE STATISTICS

**\[5:00 – 6:15\]**

Let's look at what changed between the paper's sample and ours. This table compares the 1999-to-2021 period against 2021-to-2026 across every variable.

The risk-off incidence fell from 3.2% of trading days to 1.9%. Fewer systemic crises in the extended period — but that doesn't mean calmer markets. The standard deviation compressed because VIX spikes are now shorter and sharper.

The spread widened dramatically: from -2.44 to -2.70. The Fed hiked aggressively while the BOJ remained pinned to yield curve control until March 2024. This spread was policy-capped, not free-floating. That matters for interpretation.

The log Nikkei rose from 9.56 to 10.46 — roughly a 2.5x gain in level terms — while its standard deviation dropped by a third. A post-2021 bull market with fewer crash episodes.

The log REER collapsed from 4.52 to 4.07. That's a 36% real depreciation. And the standard deviation halved. This wasn't two-sided yen volatility — it was a one-way depreciation.

Log GDP edged up marginally but its standard deviation collapsed by a factor of 31. The paper period contained the Global Financial Crisis, the 2011 Tohoku earthquake, and COVID. The extended period is a flat post-pandemic recovery. These are fundamentally different economic environments.

The World Uncertainty Index became more bimodal: sharper spikes, deeper troughs. Standard deviation nearly doubled.

Now the capital flows. This is where it gets interesting. Portfolio debt inflows halved as a share of GDP — and became twice as volatile. Equity flows were stable. Other investment — which includes yen carry trade positions — more than doubled. Direct investment also more than doubled, consistent with continued outward FDI by Japanese firms.

The takeaway: the extended period is not simply "more of the same." It is a structurally different regime.

------------------------------------------------------------------------

## SLIDE 7 — F STATISTIC

**\[6:15 – 7:00\]**

The F-test for equality of variances formalizes what the means suggested.

REER variance in the paper period was 3.5 times higher than the extended period. The yen swung both ways from 1999 to 2021. After 2021, it moved in one direction: down.

Equity variance was 1.84 times higher. Crashes and recoveries in the paper period; a steady bull run after.

The spread variance was 1.45 times higher. The BOJ's yield curve control didn't just suppress the level — it suppressed the volatility.

But debt flow variance *doubled* in the extended period — the only variable where the post-2021 world is more volatile. Capital is moving more, not less.

And GDP variance: 31 times higher in the paper period. This single number tells you the two samples are different universes.

------------------------------------------------------------------------

## SLIDE 8 — ROLLING VOLATILITY

**\[7:00 – 8:00\]**

This figure shows 260-day rolling standard deviations — roughly one trading year — for the Nikkei, the REER, and the spread.

All three show classic volatility clustering. The Nikkei spikes in 2008 and again during the 2013-to-2016 period — Abenomics, the consumption tax hike, the China growth scare. Post-2021, the rolling volatility compresses to levels not seen since the mid-1990s. The market is trending, not churning.

The REER shows the same pattern: massive spikes in 2008 and 2015, then a dramatic compression after 2021. The yen stopped being a two-way bet.

The spread is the most striking. Look at 2000 to 2005 — erratic, high-amplitude swings. 2010 to 2020 — still volatile. Then 2021 onward: near-total compression. Yield curve control operated as a volatility suppressor, not just a level anchor. When the BOJ finally lifted YCC in March 2024, the spread had already been artificially stabilized for years.

The methodological implication: any VAR estimated across the full sample that does not account for this regime change is fitting a single linear model to a world that is not linear.

------------------------------------------------------------------------

## SLIDE 9 — PRE/POST 2021 DISTRIBUTIONS

**\[8:00 – 9:00\]**

This figure overlays kernel density estimates for the 1999-to-2021 period in blue and the 2021-to-2026 period in orange, for every variable.

The title says "wider dispersion after 2021," but that's only half the story. It's variable-dependent.

GDP, Nikkei, and REER all show dramatic *narrowing*. The orange GDP curve is a near-vertical spike — leptokurtic to the extreme. The Nikkei shifts right and narrows. The REER shifts left and narrows. These are distributional signatures of a regime change, not a continuation.

The WUI and debt flows, by contrast, show marked *widening* — platykurtosis. Uncertainty and capital flows became more dispersed in the extended period, not less.

This figure alone justifies our decision to split the sample. You cannot pool these distributions and expect a single VAR to produce meaningful inference.

------------------------------------------------------------------------

## SLIDE 10 — VARIABLE DISTRIBUTIONS (HISTOGRAMS)

**\[9:00 – 9:45\]**

The histograms reveal the underlying shapes.

The Nikkei and REER are clearly multimodal — distinct currency and equity regimes visible as separate peaks. GDP is highly non-normal, likely bimodal, reflecting the structural shock of COVID and the subsequent recovery. The spread has a heavy left tail — the JGB consistently traded below the US Treasury for the entire sample period. Direct and other investment flows are leptokurtic with massive spikes near zero — most months, net flows are trivial. And risk-off is binary, an exponential-looking decay from zero.

Why does this matter for methodology? Because the SVAR assumes the residuals are normally distributed. These histograms are a warning. We will need to test and potentially address non-normality in the estimation phase.

------------------------------------------------------------------------

## SLIDE 11 — REGIME SHIFT (STRUCTURAL BREAK)

**\[9:45 – 10:45\]**

This is the most important figure in the deck. Each panel plots one variable's time series with a vertical line at March 31, 2021 — the paper's sample endpoint and our extension's starting point.

The Nikkei shows a steep, persistent positive drift post-2021 that breaks from its prior historical trend. This is not a cycle — it's a level shift.

The REER shows a near-vertical drop at the break, then settles onto a lower, flatter trend. A stark structural break in Japanese external competitiveness.

The spread establishes a new, lower equilibrium — more negative values — after 2021 and stays there.

GDP shows the sharp COVID drop followed by a steep recovery, but post-2021 it's remarkably flat compared to the pre-2021 roller coaster.

And the capital flow variables — debt, equity, other — exhibit significantly increased high-frequency oscillations after 2021. This confirms the distributional widening we saw in the density plot. Capital is sloshing around faster.

The unified story: March 2021 is not an arbitrary break point. It demarcates two fundamentally different macroeconomic regimes. Any safe haven conclusion from the pre-2021 period must be retested against the post-2021 data.

------------------------------------------------------------------------

## SLIDE 12 — CORRELATION MATRIX

**\[10:45 – 11:30\]**

The correlation heatmap tells a clear and uncomfortable story.

Real GDP and the REER share a correlation of -0.92. Economic growth is almost perfectly associated with a weaker yen. The yen and the Nikkei share -0.82. A depreciated yen strongly drives equity market valuations.

These are textbook signs of extreme multicollinearity. If you regress GDP, REER, and the Nikkei against each other simultaneously, the variance inflation factors will be enormous. The Cholesky ordering becomes critical for identification — and sensitive to specification.

Now look at the risk-off row. The binary risk-off variable shows near-zero correlation with every macro series. This is exactly what we want to see. It means global panic shocks are independent, idiosyncratic tail events — they do not move linearly with the domestic baseline. They are true exogenous shocks, which validates the Cholesky identification strategy.

The capital flow rows show modest correlations with each other and with the macro variables, consistent with the original paper's finding that flows respond weakly to risk-off shocks.

------------------------------------------------------------------------

## SLIDE 13 — NEXT STEPS

**\[11:30 – 12:15\]**

We have the data. We have the pipeline. We have the descriptive evidence of a structural break. Now we run the formal analysis.

First: SVAR estimation in R. We determine optimal lag lengths via AIC and BIC, estimate the model, and generate impulse response functions to track how a risk-off shock propagates through all ten variables.

Second: Granger causality tests and forecast error variance decomposition. This isolates exactly how much of the yen's movement is driven by external risk-off shocks versus domestic fundamentals. This is the direct test of H1.

Third: integrate new theoretical frameworks into the literature review. The 2022-to-2026 period requires engaging with the carry trade unwind literature, the BOJ's monetary divergence, and the recent work on safe haven failure during policy-driven currency depreciation.

Fourth: draft the results section with a deliberate comparison framework. 1999-to-2021 baseline versus post-2021 structural break. Does the modern safe haven hypothesis hold? The descriptive statistics suggest the answer may be no — but the formal SVAR will tell us definitively.

Finally: compile everything via Quarto into a fully reproducible PDF appendix. Every figure, every table, every regression output — traceable from raw data to final result. This is the standard the project demands, and it's the standard we intend to meet.

------------------------------------------------------------------------

## SLIDE 14 — THANK YOU

**\[12:15 – 12:30\]**

Thank you. We're ready for questions.

**\[Q&A buffer: 2–3 minutes\]**

------------------------------------------------------------------------

## ANTICIPATED Q&A

**Q: Why quadratic spline instead of linear interpolation?** Linear interpolation creates artificial flat segments between observations, which suppresses variance and biases IRF standard errors downward. Quadratic interpolation preserves the curvature of the underlying series. It's the difference between connecting dots with straight lines and connecting them with the shape the data actually suggests.

**Q: How do you handle the structural break in the VAR?** Two approaches. First, we estimate the model on both samples separately and compare IRFs. Second, we can include a post-2021 dummy interacted with the risk-off shock to test whether the impulse response changes magnitude or sign after the break. The paper's original specification assumes parameter stability — we test that assumption.

**Q: Is the yen still a safe haven based on what you've seen?** The descriptive evidence points to no — at least not in the classic sense. The yen depreciated 36% in real terms during a period that included genuine risk-off episodes. But the descriptive statistics are not causal. The SVAR will tell us whether, controlling for everything else, risk-off shocks still produce yen appreciation. That's the question the August 7 report will answer.

**Q: Why Japan only? Why drop Switzerland and the US?** The paper already established the three-country comparison. Replicating it adds no new knowledge. Focusing on Japan lets us go deeper: higher-frequency data, a longer sample, and a direct test of whether the safe haven property survived the most extreme monetary policy divergence in modern Japanese history. One country, done rigorously, yields more insight than three countries done shallowly.