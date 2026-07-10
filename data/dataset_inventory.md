# Dataset Inventory — Beirne & Sugandi (2023) Replication

Period: 1999-01-01 to 2026-06-30 (extended from paper's 1999–2021)

---

## Data Status

| # | Variable | Source | File | Freq | Period | Notes | Acquired |
|---|----------|--------|------|------|--------|-------|----------|
| 1 | VIX | LSEG `.VIX` | `data/raw/VIX.csv` | Daily | 1999–2026 | Used to construct Risk-off binary | [x] |
| 2 | Nikkei 225 | LSEG `.N225` | `data/raw/NIKKEI225.csv` | Daily | 1999–2026 | Log for Stock Index | [x] |
| 3 | S&P 500 | LSEG `.SPX` | `data/raw/SP500.csv` | Daily | 1999–2026 | Alternative Stock Index | [x] |
| 4 | US 10Y Yield | LSEG `US10YT=RR` | `data/raw/US10Y.csv` | Daily | 1999–2026 | For Spread = JPN10Y - US10Y | [x] |
| 5 | JPY/USD | LSEG `JPY=` | `data/raw/USDJPY.csv` | Daily | 1999–2026 | Log difference for exchange rate return | [x] |
| 6 | Japan 10Y Yield | FRED `IRLTLT01JPM156N` | `data/raw/JAPAN10Y.csv` | Monthly | 1989–2026 | Interpolate to daily | [x] |
| 7 | REER | LSEG Datastream `aJPIRECE/C` | `data/raw/REER.xlsx` | Monthly | 1996–2026 | BIS broad index, interpolate to daily | [x] |
| 8 | Japan RGDP | FRED `JPNRGDPEXP` | `data/raw/JAPAN_RGDP.csv` | Quarterly | 1994–2026 | Constant prices, interpolate to daily | [x] |
| 9 | WUI (Japan) | worlduncertaintyindex.com | `data/raw/WUI_JPN.csv` | Quarterly | 1952–2026 | Log transform | [x] |
| 10 | Debtsec | Bloomberg Terminal | `data/raw/DEBTSEC_BB.csv` | Quarterly | 1999–2026 | Portfolio debt inflows (% GDP) | [ ] |
| 11 | Equity | Bloomberg Terminal | `data/raw/EQUITY_BB.csv` | Quarterly | 1999–2026 | Portfolio equity inflows (% GDP) | [ ] |
| 12 | Other | Bloomberg Terminal | `data/raw/OTHER_BB.csv` | Quarterly | 1999–2026 | Other investment inflows (% GDP) | [ ] |
| 13 | Direct | Bloomberg Terminal | `data/raw/DIRECT_BB.csv` | Quarterly | 1999–2026 | FDI inflows (% GDP) | [ ] |
| 14 | Japan Nominal GDP | Bloomberg Terminal | `data/raw/JPN_NOMINAL_GDP_BB.csv` | Quarterly | 1999–2026 | Denominator for %GDP ratios | [ ] |

---

## Bloomberg Terminal Pull Guide

### Steps

1. Open Bloomberg terminal
2. Type `ECO` then press Go
3. Country: Japan
4. Function: Balance of Payments / National Accounts
5. Date range: 1Q 1999 to 2Q 2026
6. Export each series as CSV

### Variable Descriptions

Each capital flow variable is calculated as:
```
Variable = (Net inflow in USD bn) / (Nominal GDP in USD bn) x 100
```

### Bloomberg Search Paths

| Variable | ECO Navigation Path |
|----------|---------------------|
| Debtsec | Japan -> Balance of Payments -> Portfolio Investment Liabilities -> Debt Securities |
| Equity | Japan -> Balance of Payments -> Portfolio Investment Liabilities -> Equity |
| Other | Japan -> Balance of Payments -> Financial Account -> Other Investment |
| Direct | Japan -> Balance of Payments -> Direct Investment -> Liabilities |
| Nominal GDP | Japan -> National Accounts -> Nominal GDP |

### Alternative Tickers (for BDH function)

| Variable | Possible Ticker |
|----------|----------------|
| Japan Nominal GDP | `JGDPNIND Index` |
| Portfolio debt liabilities | `JNPPDEF Index` or search BOPS |
| Portfolio equity liabilities | `JNPPEQF Index` or search BOPS |
| Other investment liabilities | `JNPOTHF Index` or search BOPS |
| Direct investment liabilities | `JNPDIFF Index` or search BOPS |

---

## Constructed Variables (computed in code, not downloaded)

| Variable | Construction | Status |
|----------|-------------|--------|
| Risk-off (binary) | = 1 when VIX >= (60-day MA of VIX + 10pp), else 0 | Pending |
| Spread | = Japan 10Y yield - US 10Y yield | Pending |
| JPY/USD return | = delta log(JPY/USD) x 100 | Pending |

---

## Summary

| Status | Count | Variables |
|--------|-------|-----------|
| Acquired | 9 of 14 | VIX, Nikkei225, SP500, US10Y, JPY/USD, Japan10Y, REER, RGDP, WUI |
| Pending | 5 of 14 | Debtsec, Equity, Other, Direct, Japan Nominal GDP |
