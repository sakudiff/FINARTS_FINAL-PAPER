# Data: Sources, Construction, and Transformations

> Working draft — Aaron Status: In progress

## Variables

### Risk-off (binary)

Constructed from VIX daily close using the De Bock & De Carvalho Filho (2013) method: - Compute 60-day backward-looking moving average of VIX - Risk-off = 1 when VIX \>= (60-day MA + 10 percentage points), else 0 - Source: data/raw/VIX.csv (LSEG .VIX, 1999-2026)

Implementation notes: - First 60 days will be NaN; backfill or drop as needed - Paper uses this exact threshold for Japan, Switzerland, and US

### Spread

Japan 10Y government bond yield minus US 10Y Treasury yield. - Japan: data/raw/JAPAN10Y.csv (FRED IRLTLT01JPM156N, monthly, interpolate to daily) - US: data/raw/US10Y.csv (LSEG US10YT=RR, daily) - Spread = JAPAN10Y_interpolated - US10Y

### JPY/USD Return

Log difference of daily USD/JPY spot rate, multiplied by 100. - Source: data/raw/USDJPY.csv (LSEG JPY=, daily) - Return_t = (ln(JPY_t) - ln(JPY\_{t-1})) \* 100

### Log(RGDP)

Natural log of Japan's real GDP at constant prices. - Source: data/raw/JAPAN_RGDP.csv (FRED JPNRGDPEXP, quarterly) - Interpolate to daily via quadratic method before taking log

### Log(REER)

Natural log of the BIS real effective exchange rate (broad index). - Source: data/raw/REER.xlsx (LSEG Datastream aJPIRECE/C, monthly) - Interpolate to daily

### Log(Nikkei 225)

Natural log of the Nikkei 225 stock index. - Source: data/raw/NIKKEI225.csv (LSEG .N225, daily) - No interpolation needed

### Log(WUI)

Natural log of the World Uncertainty Index (Japan). - Source: data/raw/WUI_JPN.csv (worlduncertaintyindex.com, quarterly) - Interpolate to daily

### Capital Flow Variables (% of GDP)

Each = (Net liability inflows in USD bn / Nominal GDP in USD bn) \* 100

Data sources: - Direct: data/raw/BOJ_BPBP6JYNFL13.csv (BOJ API, 1996-2026) - Other: data/raw/BOJ_BPBP6JYNFL3.csv (BOJ API, 1996-2026) - Debtsec: data/raw/BOJ_BPPI6E3N5.csv + BPPI6E4N5.csv + BOJ_6pi-1 merge (2014+/pre-2014) - Equity: data/raw/BOJ_BPPI6E2N5.csv + BOJ_6pi-1 merge (2014+/pre-2014)

Unit conversions: - BOJ data is in 100 million JPY - Convert to USD bn using USD/JPY rate - Nominal GDP from data/raw/JAPAN_NOMINAL_GDP.csv (FRED, quarterly)

## Frequency Alignment

| Native Freq | Variables | Method |
|-----------------------------|-------------------------|-------------------|
| Daily | VIX, Nikkei, SP500, US10Y, JPY/USD | No transform |
| Monthly | Japan 10Y, REER | Quadratic interpolation |
| Quarterly | RGDP, Nominal GDP, all capital flows, WUI | Quadratic interpolation |

## Cholesky Ordering Justification

1.  Risk-off (most exogenous) — external financial shock, not affected by domestic variables
2.  WUI — global uncertainty rises during risk-off but responds slowly
3.  Spread (10Y JGB - 10Y US) — bond market responds to risk and uncertainty
4.  RGDP — real economy responds with lag
5.  REER — exchange rate responds to macro-financial conditions
6.  Nikkei 225 — equity market responds to risk and macro variables 7-10. Debtsec, Equity, Other, Direct (most endogenous) — capital flows respond last