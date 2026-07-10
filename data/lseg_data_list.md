# LSEG Workspace Data Pull List

> For replicating Beirne & Sugandi (2023) — Japan-focused model
> Period: January 1999 – June 30, 2026
> Frequency: Daily (interpolate quarterly/monthly series within the VAR)

---

## How to Use This in LSEG Workspace

1. Open **LSEG Workspace** (formerly Refinitiv Eikon)
2. Use the **Search** bar or **Datastream** add-in
3. For each RIC code below, add to a list and download as **CSV** or **XLSX**
4. Set date range: **1 Jan 1999 – 30 Jun 2026**

---

## I. Financial Market Data (Daily, Direct RICs)

These are the core daily series. Pull every trading day.

| # | Variable | RIC / Code | Description | Notes |
|---|----------|-----------|-------------|-------|
| 1 | **VIX** | `.VIX` | CBOE Volatility Index | Used to construct the binary **Risk-off** indicator |
| 2 | **JP 10Y Bond Yield** | `JP10YT=RR` | Japan 10-year government bond yield (%) | For **Spread** = JP10YT − US10YT |
| 3 | **US 10Y Treasury Yield** | `US10YT=RR` | US 10-year Treasury note yield (%) | For **Spread** |
| 4 | **Nikkei 225** | `.N225` | Nikkei 225 Stock Average (index) | Japan equity market → log transform |
| 5 | **S&P 500** | `.SPX` | S&P 500 Index (index) | US equity market → log transform |
| 6 | **USD/JPY** | `JPY=` | USD/JPY spot exchange rate | For JPY/USD return = Δlog(JPY=) × 100 |
| 7 | **Japan 2Y Bond Yield** (optional) | `JP2YT=RR` | Japan 2-year government bond yield (%) | Alternative spread measure |

**Total: 6–7 series from LSEG Markets**

---

## II. Macroeconomic Data (Lower Frequency)

These need to be pulled from LSEG's **Datastream** macroeconomic database within Workspace. 
Search by the **Datastream mnemonic** or the descriptive name.

| # | Variable | Datastream Mnemonic | Description | Native Frequency | Notes |
|---|----------|-------------------|-------------|------------------|-------|
| 8 | **Japan Real GDP** | `JPGDP...D` or search "Japan Gross Domestic Product Constant Prices" | Real GDP, constant prices (JPY bn) | Quarterly | Interpolate to daily via quadratic |
| 9 | **Japan Nominal GDP** | `JPGDP...C` or search "Japan Gross Domestic Product Current Prices" | Nominal GDP, current prices (JPY bn) | Quarterly | Used to compute Debtsec/Equity/Other/Direct as % of GDP |
| 10 | **JP REER** (Broad) | Search "Japan Real Effective Exchange Rate BIS" or use `..JP..REER` | BIS real effective exchange rate, broad index (2010=100) | Monthly | If not found, use trade-weighted USD/JPY variant from LSEG |
| 11 | **Japan Net Portfolio Debt Inflows** | Search "Japan Portfolio Investment Liabilities Debt Securities" | Net inflows to debt securities (USD bn) | Quarterly | Match IMF BOPS series code in LSEG |
| 12 | **Japan Net Portfolio Equity Inflows** | Search "Japan Portfolio Investment Liabilities Equity" | Net inflows to equity securities (USD bn) | Quarterly | Match IMF BOPS series |
| 13 | **Japan Net Other Investment Inflows** | Search "Japan Other Investment Liabilities" | Net other investment inflows (USD bn) | Quarterly | Match IMF BOPS series |
| 14 | **Japan Net FDI Inflows** | Search "Japan Direct Investment Liabilities" | Net direct investment inflows (USD bn) | Quarterly | Match IMF BOPS series |

**Search strategy for macro data in LSEG Workspace:**
- Go to the **Datastream** tab (or use the search bar with "Datastream" filter)
- Search by keyword e.g. "Japan Real GDP constant"
- Add the series to your list
- Set frequency to match the native frequency (quarterly/monthly)
- LSEG will handle the data export

---

## III. Alternative: Simplified 6-Variable Model (Recommended)

Skip the capital flow variables (11–14) and use just these 7 series from LSEG:

| Pos | Variable | LSEG Code | Native Freq | Role in VAR |
|-----|----------|-----------|-------------|-------------|
| 1 | **VIX** | `.VIX` | Daily | Raw material for Risk-off binary |
| 2 | **JP 10Y Yield** | `JP10YT=RR` | Daily | Compute Spread = JP10YT − US10YT |
| 3 | **US 10Y Yield** | `US10YT=RR` | Daily | Compute Spread |
| 4 | **Nikkei 225** | `.N225` | Daily | Log(Stock Index) |
| 5 | **S&P 500** | `.SPX` | Daily | Log(Stock Index) — alternative |
| 6 | **Japan Real GDP** | Datastream search | Quarterly → interpolated | Log(RGDP) |
| 7 | **JP REER** | Datastream search | Monthly → interpolated | Log(REER) |
| 8 | **USD/JPY** | `JPY=` | Daily | ΔLog(JPY/) × 100 |

---

## IV. Risk-off Indicator Construction (No LSEG needed — compute in Python/R)

After you have `.VIX` from LSEG:

```python
import pandas as pd
import numpy as np

vix = pd.read_csv('vix.csv', parse_dates=['Date'])
vix['MA60'] = vix['Close'].rolling(window=60).mean()
vix['Risk-off'] = (vix['Close'] >= vix['MA60'] + 10).astype(int)
# First 60 days will be NaN — drop or backfill
```

This matches the De Bock & De Carvalho Filho (2013) method used by Beirne & Sugandi.

---

## V. Quick Pull Checklist

### Must Have (core model — all from LSEG)

- [ ] `.VIX` — VIX Index
- [ ] `JP10YT=RR` — Japan 10Y bond yield 
- [ ] `US10YT=RR` — US 10Y Treasury yield
- [ ] `.N225` — Nikkei 225 Index
- [ ] `JPY=` — USD/JPY spot rate
- [ ] **Japan Real GDP** (Datastream search) — quarterly
- [ ] **Japan REER** (Datastream search) — monthly
- [ ] **Japan Nominal GDP** (Datastream search) — quarterly (for %GDP ratios if doing capital flows)

### Nice to Have (for the full model with capital flows)

- [ ] **Japan net portfolio debt inflows** (Datastream)
- [ ] **Japan net portfolio equity inflows** (Datastream)
- [ ] **Japan net other investment inflows** (Datastream)
- [ ] **Japan net FDI inflows** (Datastream)

### Alternative for WUI (not on LSEG)

The World Uncertainty Index is an academic dataset not available on LSEG. Options:
1. Use VIX as a continuous risk measure alongside the binary Risk-off indicator
2. Download WUI from worlduncertaintyindex.com

---

## VI. Delivery Format

For each series, export from LSEG as:
- **Format:** CSV (.csv) or XLSX
- **Date range:** 1 Jan 1999 to 30 Jun 2026
- **Columns:** Date | Value (or Open/High/Low/Close for market data)
- **Frequency:** As native (daily, monthly, quarterly) — we'll align in code
