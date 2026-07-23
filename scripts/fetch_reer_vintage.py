"""Fetch 2021-vintage BIS broad real effective exchange rate for Japan from Wayback Machine."""

import urllib.request
import tempfile
import os
import sys

import pandas as pd
import numpy as np

# Wayback Machine snapshot of bis.org/statistics/eer/broad.xlsx from May 2021.
# BIS retroactively revised the series (2023 rebasing to 2020=100), so current
# downloads differ from what the paper authors would have seen in 2021.
SNAPSHOT_URL = (
    "https://web.archive.org/web/20210524235626id_/"
    "https://www.bis.org/statistics/eer/broad.xlsx"
)

# Identify Japan's real broad REER column in the "Real" sheet header layout.
# Row 3: country names (col 31 = "Japan")
# Row 4: BIS tickers (col 31 = "RBJP")
JAPAN_COL = 31

OUTPUT_DIR = "data/raw/vintage"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "REER_JPN_BIS_vintage.csv")


def fetch_broad_xlsx(url: str) -> bytes:
    """Download broad.xlsx from the Wayback Machine."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def extract_japan_reer(data: bytes) -> pd.DataFrame:
    """Extract Japan real broad REER from the xlsx bytes.

    Returns a DataFrame with columns ['date', 'reer'] at month-start frequency.
    """
    tmp = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
    try:
        tmp.write(data)
        tmp.close()
        df = pd.read_excel(tmp.name, sheet_name="Real", header=None)
    finally:
        os.unlink(tmp.name)

    # Data rows: row 5 onward (rows 0-4 are headers)
    dates_raw = df.iloc[5:, 0].values
    rbjp_raw = df.iloc[5:, JAPAN_COL].values

    dates = pd.to_datetime([str(d)[:10] for d in dates_raw])
    vals = pd.to_numeric(rbjp_raw, errors="coerce")

    # Convert end-of-month dates to month-start (ISO 8601 month-start date)
    dates = dates.to_period("M").to_timestamp()

    result = pd.DataFrame({"date": dates, "reer": vals})
    result = result.dropna(subset=["reer"]).reset_index(drop=True)
    result["date"] = result["date"].dt.strftime("%Y-%m-%d")
    return result


def verify(result: pd.DataFrame, source_data: pd.DataFrame) -> dict:
    """Run diagnostics on the extracted series."""
    vals = pd.to_numeric(result["reer"], errors="coerce")
    dates = pd.to_datetime(result["date"])
    info = {}

    mask_2010 = (dates >= "2010-01-01") & (dates <= "2010-12-01")
    mask_2020 = (dates >= "2020-01-01") & (dates <= "2020-12-01")
    info["base_year"] = "2010" if abs(vals[mask_2010].mean() - 100) < 5 else "unknown"
    info["2010_mean"] = round(vals[mask_2010].mean(), 4)
    info["2020_mean"] = round(vals[mask_2020].mean(), 4)
    info["date_min"] = dates.min().strftime("%Y-%m-%d")
    info["date_max"] = dates.max().strftime("%Y-%m-%d")
    info["n_obs"] = len(result)

    # Mean abs pct diff vs current data over 2015-2021
    if source_data is not None:
        vintage_s = result.set_index("date")["reer"]
        cur_s = source_data.set_index("date")["reer"]
        both = pd.DataFrame({"v": vintage_s, "c": cur_s}).dropna()
        both = both.loc["2015-01-01":"2021-03-01"]
        pct_diff = np.abs(both["v"].astype(float) - both["c"].astype(float)) / both["c"].astype(float) * 100
        info["mean_abs_pct_diff_vs_current"] = round(pct_diff.mean(), 4)
        info["max_abs_pct_diff_vs_current"] = round(pct_diff.max(), 4)

    return info


def main():
    print(f"Fetching 2021-vintage BIS broad.xlsx from Wayback Machine...")
    xlsx_data = fetch_broad_xlsx(SNAPSHOT_URL)
    print(f"Downloaded {len(xlsx_data)} bytes")

    result = extract_japan_reer(xlsx_data)
    print(f"Extracted {len(result)} months of Japan real broad REER")

    # Optionally compare against current REER.xlsx
    current = None
    current_path = "data/raw/REER.xlsx"
    if os.path.exists(current_path):
        try:
            cur = pd.read_excel(current_path, sheet_name="Table Data")
            cur["date"] = pd.to_datetime(cur["Date"]).dt.strftime("%Y-%m-%d")
            cur["reer"] = pd.to_numeric(cur.iloc[:, 1], errors="coerce")
            current = cur[["date", "reer"]].dropna()
        except Exception:
            pass

    info = verify(result, current)
    print(f"\nProvenance:")
    print(f"  Source: {SNAPSHOT_URL}")
    print(f"  Snapshot date: 2021-05-24")
    print(f"  Base year: {info['base_year']} (2010 mean = {info['2010_mean']})")
    print(f"  Coverage: {info['date_min']} to {info['date_max']} ({info['n_obs']} months)")
    if "mean_abs_pct_diff_vs_current" in info:
        print(f"  Mean abs % diff vs REER.xlsx (2015-2021): {info['mean_abs_pct_diff_vs_current']}%")
        print(f"  Max abs % diff vs REER.xlsx (2015-2021): {info['max_abs_pct_diff_vs_current']}%")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False)
    print(f"\nWrote {OUTPUT_FILE}")
    return result


if __name__ == "__main__":
    main()
