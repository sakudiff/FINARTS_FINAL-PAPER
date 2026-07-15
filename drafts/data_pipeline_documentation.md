Data Pipeline - Full Process Documentation

Source: data_pipeline.qmd

================================================================================
STEP 0: SETUP & CONFIGURATION
================================================================================

- Set START_DATE = 1999-01-14 (first working day with all financial data available per paper).
- Set END_DATE = 2026-06-30 (extended sample end).
- Set PAPER_END = 2021-03-31 (boundary between original paper period and extended period).
- Created era_map for Japanese calendar conversion: Heisei 1 = 1989 (offset 1988), Reiwa 1 = 2019 (offset 2018). Needed because BOJ historical data uses Japanese era years.
- Defined a custom ggplot theme (theme_quant) and period color palette (blue for paper, orange for extended, gray for full sample).


================================================================================
STEP 1: LOAD DAILY FINANCIAL DATA (LSEG CSVs)
================================================================================

Source files: VIX.csv, NIKKEI225.csv, SP500.csv, US10Y.csv, USDJPY.csv

Decision: All five LSEG daily CSVs share identical 6-column format (Date, Close, High, Low, Open, Volume). We only need Close.
Action: Created read_lseg_daily() - parses column types, extracts Date and Close, renames Close to the variable name.
Transformation: Filtered to date >= START_DATE (1999-01-14).

Special case - JGB yields (jgbcme_all.csv):
- Different format: row 1 is a title, row 2 is the actual header.
- 10-year JGB yield is column 11 (0-indexed 10).
- Values use "-" as missing marker.
- Action: skipped first row, read with defaults, renamed, converted dashes to NA, parsed as numeric.

Files loaded: vix, nikkei225, sp500, us10y, usdjpy, jgb10y.


================================================================================
STEP 2: LOAD MACROECONOMIC DATA (Mixed Frequencies)
================================================================================

REER.xlsx (BIS, monthly):
- Excel file, sheet name detected dynamically (not hardcoded).
- First row is a sub-header with NA date and "Close" text - filtered out.
- Date stored as datetime (ymd_hms), extracted to date.
- Filtered to START_DATE.

JAPAN_RGDP.csv (FRED, quarterly):
- Straightforward 2-column CSV: Date, Value.
- Filtered to START_DATE.

JAPAN_NOMINAL_GDP.csv (FRED, quarterly, millions of JPY):
- Same format, needed for %GDP conversions.
- Filtered to START_DATE.

WUI_JPN.csv (World Uncertainty Index, quarterly):
- 2 columns: observation_date, WUIJPN.
- Filtered to START_DATE.

Files loaded: reer, rgdp, nominal_gdp, wui.


================================================================================
STEP 3: PARSE BOJ 6pi-1 CSV (PRE-2014 CAPITAL FLOWS)
================================================================================

Source: BOJ_6pi-1_portfolio_summary.csv

Critical problem: File uses Shift-JIS (CP932) encoding. readr crashes on this encoding.
Decision: Used base R readLines with explicit CP932 encoding instead of readr.

Challenge: The file has a mixed layout - title rows, metadata, then a data section.
Action: Located the "(Monthly figures)" marker in the raw text, extracted everything after it as the data region.

Challenge: Data uses Japanese era years (e.g., "平成15年" = Heisei 15 = 2003).
Action: Strip the "年" kanji, handle the special case "元年" (first year of era = year 1), extract the era type (Heisei/Reiwa), convert to Gregorian using era_map offsets.

Challenge: 29 columns, but we only need columns for equity net (X22), long-term debt net (X25), short-term debt net (X28) from the liabilities section.

Challenge: Values are comma-formatted and use "--" for missing.
Action: Created parse_boj_val() - strips commas, converts "--" to NA, parses as numeric.

Decision: Debt securities = long-term + short-term debt (per BOJ D-04 definition).

Decision: Only keep data up to 2013-12-01. Post-2014 data comes from the cleaner BOJ API.

Output: debtsec_pre2014 and equity_pre2014 series at monthly frequency.


================================================================================
STEP 4: LOAD POST-2014 BOJ API DATA
================================================================================

Source files: BOJ_BPPI6E3N5.csv (long-term debt), BOJ_BPPI6E4N5.csv (short-term debt),
              BOJ_BPPI6E2N5.csv (equity), BPBP6JYNFL3.csv (other investment),
              BPBP6JYNFL13.csv (direct investment).

These are clean 2-column CSVs (Date, value) in units of 100 million JPY.
Created read_boj_api() helper.

Action: Filtered to START_DATE. Post-2014 data starts from 2014 onward.


================================================================================
STEP 5: MERGE CAPITAL FLOWS (PRE-2014 + POST-2014)
================================================================================

Decision: Need continuous series spanning the full sample from two different data sources.

For debt securities:
- Pre-2014: debtsec_pre2014 (from parsed BOJ 6pi-1, debtsec = long-term + short-term).
- Post-2014: debtsec_post2014 = boj_lt + boj_st (two separate API files summed).

For equity:
- Pre-2014: equity_pre2014 (from parsed BOJ 6pi-1).
- Post-2014: equity_post2014 = single BOJ API series.

Action: row-bind pre-2014 and post-2014, sort by date.

Other and Direct investment: single-source series (BOJ API covers the full range), no merge needed.

Output: debtsec_all, equity_all, other_all, direct_all (all monthly frequency).


================================================================================
STEP 6: CONSTRUCT RISK-OFF INDICATOR
================================================================================

Decision: Follow Beirne & Sugandi (2023) definition exactly.

Algorithm:
1. Compute 60-day rolling mean of VIX (trailing window, right-aligned).
2. risk_off = 1 if VIX >= VIX_60MA + 10, else 0.

Critical detail: Left_join sequence uses VIX as anchor (VIX trades every US market day).
This preserves dates where VIX exists but JGB/Nikkei don't (Japanese holidays).
Important because risk-off episodes can start on US trading days that are Japanese holidays.

All daily financial series merged into daily_fin dataframe.


================================================================================
STEP 7: COMPUTE YIELD SPREAD
================================================================================

Decision: Simple point-in-time subtraction.
spread = jgb10y - us10y (both in percentage points).

No lag, no smoothing - reflects the actual yield differential available to investors on that trading day.


================================================================================
STEP 8: LOG TRANSFORMATIONS
================================================================================

For financial variables: log_nikkei = log(nikkei225).
For macro variables: log_reer = log(reer), log_rgdp = log(rgdp).

Special case - WUI: Can be zero in early observations, which would produce -Inf.
Action: Guard condition - log_wui = log(wui) only if wui > 0, otherwise NA.


================================================================================
STEP 9: CAPITAL FLOW %GDP CONVERSION
================================================================================

This is the most complex calculation in the pipeline. We need to convert flows from
100M JPY to % of nominal GDP.

Sub-step 9a: Get end-of-month USD/JPY rates.
- Take the last trading day of each month from the daily USDJPY series.
- This matches how monthly GDP is reported (end of quarter).

Sub-step 9b: Expand nominal GDP to monthly frequency.
- GDP is quarterly (data points at March, June, September, December).
- Use complete() to generate a full monthly sequence.
- Use fill() with .direction = "down" to carry forward the quarterly value.
- This means January and February use the previous December's GDP, etc.

Sub-step 9c: Unit conversion.
- BOJ flows are in 100M JPY. Convert to USD billions:
    flow_usd_bn = (flow_100m_jpy * 0.1) / usdjpy_eom
  Why: 100M JPY = 0.1 billion JPY. Divide by USD/JPY rate = USD billions.
- GDP is in millions of JPY. Convert to USD billions:
    gdp_usd_bn = gdp_jpy_mn / (usdjpy_eom * 1000)
  Why: Divide by rate gets USD millions, divide by 1000 gets USD billions.

Sub-step 9d: Compute percentage.
    flow_pct_gdp = (flow_usd_bn / gdp_usd_bn) * 100

Done separately for debtsec_pct, equity_pct, other_pct, and direct_pct.

Output: Four monthly %GDP series.


================================================================================
STEP 10: EXPORT NATIVE-FREQUENCY DATA FOR QUADRATIC INTERPOLATION
================================================================================

Decision: The pipeline needs to convert monthly and quarterly series to daily frequency
to match the daily financial variables.

Why not linear interpolation? The paper (Beirne & Sugandi 2023) uses quadratic interpolation
(Section 4). We replicate their method exactly.

Why Python? R has no native quadratic spline function. pandas provides it as a one-liner
with proper boundary behavior (no extrapolation past anchor points).

Critical detail: We export unfiltered data (full available history, not START_DATE filtered).
The quadratic interpolation needs anchor points BEFORE 1999-01-14 to correctly fit the curve
at the start of the sample window. Without these pre-sample anchors, the interpolation
at January 1999 would be unreliable.

Files exported to data/tmp_quadratic/:
- log_reer_native.csv
- log_rgdp_native.csv
- log_wui_native.csv
- debtsec_native.csv
- equity_native.csv
- other_native.csv
- direct_native.csv

Each is a 2-column CSV (date, value) at native frequency (monthly or quarterly).

For capital flows, the native-frequency %GDP calculations are re-done on the unfiltered
full series here, using the same conversion logic as Step 9 but without the START_DATE filter.


================================================================================
STEP 11: PYTHON QUADRATIC INTERPOLATION
================================================================================

Action: system2 call to scripts/quadratic_interpolate.py (R runs Python externally).

What the Python script does:
1. Reads each native-frequency CSV from data/tmp_quadratic/.
2. Sets date as index.
3. Upsamples to daily frequency.
4. Applies pandas interpolate(method='quadratic').
5. Does NOT extrapolate - only fills dates between existing anchor points.
6. Writes output as _daily.csv files.

The no-extrapolation constraint is critical: it means we never invent data
beyond the actual observed date range of each series.


================================================================================
STEP 12: IMPORT INTERPOLATED DATA BACK TO R
================================================================================

Reads the _daily.csv files from data/tmp_quadratic/ back into R dataframes:
log_reer_daily, log_rgdp_daily, log_wui_daily, debtsec_daily, equity_daily,
other_daily, direct_daily.

All are now at daily frequency.


================================================================================
STEP 13: WORKING DAYS FILTER
================================================================================

Decision: After interpolation, remove weekends. Keep only Monday (wday = 2) through
Friday (wday = 6).

Why after interpolation, not before? The quadratic interpolation needs a continuous
date sequence to fit the spline. If we removed weekends first, the interpolation
would be fitting to irregular spacing.

All 10 variables (3 financial + 7 macro/interpolated) are filtered to working days.

This is the first point where risk_off, spread, and log_nikkei are also filtered
to working days (they were on the full US-trading-day calendar until now).


================================================================================
STEP 14: MERGE ALL VARIABLES INTO FINAL DATASET
================================================================================

All 10 variables joined on date using full_joins.

Variable order: risk_off, log_wui, spread, log_rgdp, log_reer, log_nikkei,
debtsec_pct, equity_pct, other_pct, direct_pct.

Period assignment:
- date <= 2021-03-31 -> "1999-2021" (paper period).
- date > 2021-03-31 -> "2021-2026" (extended period).

Output: final_dataset with 7171 rows x 11 columns (date + 10 variables + period).


================================================================================
STEP 15: EXPORT FINAL DATASET
================================================================================

Written to data/processed/final_dataset.csv.


================================================================================
STEP 16: DESCRIPTIVE STATISTICS
================================================================================

Compute N, Mean, SD, Min, Max for each variable, grouped by period.
Also compute full-sample statistics.
Output formatted as an HTML table and written to data/processed/descriptive_stats.csv.


================================================================================
STEP 17: F-TEST FOR EQUALITY OF VARIANCES
================================================================================

Test 5 key variables: log_reer, log_nikkei, spread, debtsec_pct, log_rgdp.

Purpose: Test whether the variance differences between periods are statistically significant.
Reports F-statistic, p-value, and which period has higher variance.

All five significant at p < 0.0001. log_rgdp has F = 31.14 (paper period dominates).
debtsec_pct inverts (F = 0.50, extended period more volatile).


================================================================================
STEP 18: ROLLING VOLATILITY PLOTS
================================================================================

260-day (1 trading year) rolling standard deviation for log_reer, log_nikkei, spread.
Faceted plot with 2021-03-31 vertical line.
Diagnostic: shows how volatility evolves through time rather than just period averages.


================================================================================
STEP 19: VISUALIZATION SUITE
================================================================================

Four figure sets:

a) Overlaid densities by period for all variables - shows distributional shifts after 2021.
b) Full-sample densities (single period, all data pooled) - overall shape reference.
c) Time-series plots with period color-coding and 2022 yen depreciation highlight.
d) Correlation matrix (full-sample, pairwise complete observations) - cross-variable diagnostics.

================================================================================
STEP 20: LaTeX TABLE EXPORT
================================================================================

Runs scripts/generate_descriptive_table.R which reads descriptive_stats.csv,
formats it as a booktabs longtable LaTeX file, and writes to drafts/.
Used for LaTeX paper compilation.


================================================================================
SUMMARY OF KEY DECISIONS
================================================================================

1. START_DATE = 1999-01-14: First date with complete financial data across all series.
2. Japanese era parsing: Manually handled because standard parsers crash on CP932 encoding.
3. BOJ data split at 2014: Pre-2014 from 6pi-1 CSV, post-2014 from cleaner BOJ API.
4. Debt securities = long-term + short-term: Per BOJ D-04 statistical definition.
5. risk_off follows Beirne & Sugandi (2023): VIX >= 60MA + 10, left_join preserves US-only trading days.
6. Quadratic interpolation via Python: R lacks native quadratic spline; pandas provides exact method.
7. Pre-sample anchors exported: Without anchor points before Jan 1999, interpolation at sample start is unreliable.
8. Weekends removed AFTER interpolation: Spline needs continuous dates; irregular spacing would break it.
9. %GDP conversion uses end-of-month FX rates: Matches monthly GDP reporting convention.
10. GDP carried forward monthly: January-February use December value; avoids NA gaps between quarterly observations.
