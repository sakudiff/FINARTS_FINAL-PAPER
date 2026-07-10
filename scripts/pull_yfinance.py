"""Pull datasets from yfinance for Beirne & Sugandi (2023) replication.
Saves as CSV in data/yahoo/ with proper naming."""

import yfinance as yf
import pandas as pd
from pathlib import Path

OUT = Path("data/yahoo")
OUT.mkdir(parents=True, exist_ok=True)

START = "1999-01-01"
END = "2026-06-30"

tickers = {
    "VIX": "^VIX",
    "NIKKEI225": "^N225",
    "SP500": "^GSPC",
    "US10Y": "^TNX",
}

for name, ticker in tickers.items():
    print(f"Downloading {name} ({ticker})...")
    df = yf.download(ticker, start=START, end=END, auto_adjust=True, progress=False)
    if df.empty:
        print(f"  WARNING: No data for {ticker}")
        continue
    df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    out_path = OUT / f"{name}.csv"
    df.to_csv(out_path)
    print(f"  {len(df)} rows, {df.index[0].date()} → {df.index[-1].date()}  ->  {out_path}")

# Try Japan 10Y — may have limited history
print("Downloading Japan 10Y yield (JGB10)...")
try:
    jgb = yf.download("^JGB10", start=START, end=END, auto_adjust=True, progress=False)
    if not jgb.empty:
        jgb.columns = [c[0] if isinstance(c, tuple) else c for c in jgb.columns]
        jgb.to_csv(OUT / "JAPAN10Y.csv")
        print(f"  {len(jgb)} rows, {jgb.index[0].date()} → {jgb.index[-1].date()}")
    else:
        # Fallback: try the ETF proxy
        print("  ^JGB10 empty — trying IEF as proxy approach...")
except Exception as e:
    print(f"  Error: {e}")

print("\nDone.")
