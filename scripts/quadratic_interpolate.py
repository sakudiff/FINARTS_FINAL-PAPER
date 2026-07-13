import pandas as pd
import numpy as np
import sys
import os

TMP_DIR = "data/tmp_quadratic"
START = pd.Timestamp("1999-01-01")
END   = pd.Timestamp("2026-06-30")

all_dates = pd.date_range(START, END, freq="D")

def quadratic_to_daily(in_path, value_col, out_path):
    """Read native-frequency CSV, quadratic-interpolate to daily, write."""
    df = pd.read_csv(in_path, parse_dates=["date"])
    df = df.set_index("date")
    # Reindex to full daily calendar; NAs are filled by quadratic interpolation
    df = df.reindex(all_dates)
    # Quadratic interpolation fills interior NAs; leading/trailing NAs stay NA
    df[value_col] = df[value_col].interpolate(method="quadratic")
    df = df.reset_index().rename(columns={"index": "date"})
    df.to_csv(out_path, index=False)

# Monthly variables
quadratic_to_daily(f"{TMP_DIR}/log_reer_native.csv", "log_reer", f"{TMP_DIR}/log_reer_daily.csv")
quadratic_to_daily(f"{TMP_DIR}/debtsec_native.csv",  "debtsec_pct", f"{TMP_DIR}/debtsec_daily.csv")
quadratic_to_daily(f"{TMP_DIR}/equity_native.csv",   "equity_pct", f"{TMP_DIR}/equity_daily.csv")
quadratic_to_daily(f"{TMP_DIR}/other_native.csv",    "other_pct", f"{TMP_DIR}/other_daily.csv")
quadratic_to_daily(f"{TMP_DIR}/direct_native.csv",   "direct_pct", f"{TMP_DIR}/direct_daily.csv")

# Quarterly variables
quadratic_to_daily(f"{TMP_DIR}/log_rgdp_native.csv", "log_rgdp", f"{TMP_DIR}/log_rgdp_daily.csv")
quadratic_to_daily(f"{TMP_DIR}/log_wui_native.csv",  "log_wui", f"{TMP_DIR}/log_wui_daily.csv")
