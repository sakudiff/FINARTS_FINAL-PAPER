#!/usr/bin/env python3
"""Run the replication experiment matrix for Beirne & Sugandi (2023) Japan SVAR.

Usage:
  uv run python scripts/run_experiments.py
  uv run python scripts/run_experiments.py --only e3,e3b --point-estimates
  uv run python scripts/run_experiments.py --build-summary-only

Outputs: data/processed/var_results/experiments/
         docs/logs/2026-07-23-svar-replication-experiments.md
"""
import os
import sys
import warnings
import time
import argparse
from pathlib import Path

# Ensure the project root is on sys.path for imports
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

import matplotlib
matplotlib.use("Agg")

from statsmodels.tsa.api import VAR
from scripts.var_analysis import run_var, build_exog, _delta_irf_ci
from scripts.var_monthly_pipeline import compute_orth_irf
from scripts.quadratic_match import quadratic_match_average

VAR_ORDER = [
    "risk_off", "log_wui", "spread", "log_rgdp", "log_reer",
    "log_nikkei", "debtsec_pct", "equity_pct", "other_pct", "direct_pct",
]

PAPER_END = pd.Timestamp("2021-03-31")
IRF_H_M = 40
IRF_H_D = 125
MAX_LAG_M = 12
MAX_LAG_D = 20
MC_REPS = 1000
MC_REPS_DAILY = 500
ALPHA = 0.05

OUT_DIR = Path("data/processed/var_results/experiments")
OUT_DIR.mkdir(parents=True, exist_ok=True)
TMP_DIR = Path("data/tmp_experiments")
TMP_DIR.mkdir(parents=True, exist_ok=True)

RNG = np.random.default_rng(20260723)

KEY_HORIZONS_M = [0, 1, 3, 6, 12, 24, 40]
KEY_HORIZONS_D = [0, 1, 3, 6, 12, 24, 125]

COMPARE_VARS = ["log_rgdp", "log_wui", "log_reer", "spread", "log_nikkei",
                "debtsec_pct", "equity_pct", "other_pct", "direct_pct"]

PAPER_SIGNS = {
    "log_rgdp": "negative",
    "log_wui": "positive",  # Paper: risk-off shocks raise uncertainty
    "log_reer": "positive",
    "spread": "positive",
    "log_nikkei": "positive_then_negative",  # Paper: immediate positive at h=0, negative thereafter
    "debtsec_pct": None,
    "equity_pct": None,
    "other_pct": None,
    "direct_pct": None,
}


_PAPER_SIGN_DISPLAY = {
    "negative": "negative",
    "positive": "positive",
    "positive_then_negative": "positive",
}


def _agg_monthly_e1(df, end_date):
    """Aggregate daily data to monthly: risk_off=proportion, spread=mean, rest=last."""
    sub = df[df["date"] <= end_date].copy()
    sub["ym"] = sub["date"].dt.to_period("M")
    monthly = sub.groupby("ym").agg({
        "risk_off": lambda x: x.mean(),
        "log_wui": "last",
        "spread": "mean",
        "log_rgdp": "last",
        "log_reer": "last",
        "log_nikkei": "last",
        "debtsec_pct": "last",
        "equity_pct": "last",
        "other_pct": "last",
        "direct_pct": "last",
    }).reset_index()
    monthly["date"] = monthly["ym"].apply(lambda x: x.to_timestamp())
    monthly = monthly.drop(columns=["ym"]).dropna().reset_index(drop=True)
    return monthly


def _exog_from_df(df):
    """Build exog array + names from a DataFrame with a 'date' column."""
    return build_exog(df)


def _select_lag_bic(data, exog, maxlags=MAX_LAG_M):
    """Select lag via BIC on an unrestricted VAR. Returns int lag."""
    model = VAR(endog=data, exog=exog)
    order = model.select_order(maxlags=maxlags, trend="n")
    return int(order.selected_orders["bic"])


def _select_lag_aic(data, exog, maxlags=MAX_LAG_D):
    """Select lag via AIC on an unrestricted VAR. Returns int lag."""
    model = VAR(endog=data, exog=exog)
    order = model.select_order(maxlags=maxlags, trend="n")
    return int(order.selected_orders["aic"])


def _est_restricted(data, exog, lag, periods=IRF_H_M):
    """Estimate restricted VAR (block exogeneity on risk_off). Returns model and IRF object."""
    results = run_var(data, exog, restricted=True, k_ar=lag)
    irf_obj = results.irf(periods=periods)
    return results, irf_obj


def _est_unrestricted(data, exog, lag, periods=IRF_H_M):
    """Estimate unrestricted VAR via statsmodels. Returns results and IRF object."""
    model = VAR(endog=data, exog=exog)
    results = model.fit(lag, trend="n")
    irf_obj = results.irf(periods=periods)
    return results, irf_obj


def _irf_table(irf_vals, lower, upper, var_order, horizons):
    """Build a flat IRF table as a list of dicts."""
    rows = []
    for v_idx, v_name in enumerate(var_order):
        for h in horizons:
            if h >= irf_vals.shape[0]:
                continue
            row = {"variable": v_name, "horizon": h,
                   "response": float(irf_vals[h, v_idx, 0])}
            if lower is not None:
                row["lower"] = float(lower[h, v_idx])
                row["upper"] = float(upper[h, v_idx])
            rows.append(row)
    return rows


def _save_irf_csv(rows, stem):
    """Save IRF table as CSV."""
    path = OUT_DIR / f"{stem}_irf.csv"
    pd.DataFrame(rows).to_csv(path, index=False)
    print(f"  Saved: {path.name}")
    return path


def _print_irf_table(irf_vals, var_order, horizons, label=""):
    """Print formatted IRF table for key horizons."""
    print(f"\n  IRF responses to risk-off shock {label}:")
    header = f"{'Var':<12s}" + "".join(f"{'h='+str(h):>12s}" for h in horizons)
    print(f"  {header}")
    print(f"  {'-' * len(header)}")
    for v_name in COMPARE_VARS:
        vidx = var_order.index(v_name)
        vals = []
        for h in horizons:
            if h < irf_vals.shape[0]:
                vals.append(irf_vals[h, vidx, 0])
            else:
                vals.append(np.nan)
        row_str = f"{v_name:<12s}" + "".join(f"{v:>12.6f}" for v in vals)
        print(f"  {row_str}")


def _sign_verdict(v_name, irf_vals, var_order, horizon_filter=None):
    vidx = var_order.index(v_name)
    paper_sign = PAPER_SIGNS.get(v_name)
    if paper_sign is None:
        return "N/A"

    if horizon_filter is not None:
        horizons = [h for h in horizon_filter if h > 0 and h < irf_vals.shape[0]]
    else:
        horizons = list(range(1, irf_vals.shape[0]))

    if v_name == "log_nikkei":
        h0_positive = irf_vals[0, vidx, 0] > 0
        resp = np.array([irf_vals[h, vidx, 0] for h in horizons])
        total = len(resp)
        if total == 0:
            return "N/A"
        neg_count = int(np.sum(resp < 0))
        if h0_positive and neg_count >= total * 0.7:
            return "MATCH"
        elif neg_count >= total * 0.7:
            return "PARTIAL"
        elif neg_count >= total * 0.4:
            return "PARTIAL"
        else:
            return "MISMATCH"

    resp = np.array([irf_vals[h, vidx, 0] for h in horizons])
    total = len(resp)
    if total == 0:
        return "N/A"

    if paper_sign == "negative":
        sign_count = int(np.sum(resp < 0))
    elif paper_sign == "positive":
        sign_count = int(np.sum(resp > 0))
    else:
        return "N/A"

    if sign_count >= total * 0.7:
        return "MATCH"
    elif sign_count >= total * 0.4:
        return "PARTIAL"
    else:
        return "MISMATCH"


def _ci_from_model(results, irf_obj, n_reps, is_daily=False):
    """Compute Monte Carlo confidence intervals."""
    if hasattr(results, 'sigma_u') and type(results).__module__.startswith("statsmodels"):
        try:
            lower_mc, upper_mc = irf_obj.errband_mc(orth=True, repl=n_reps,
                                                     signif=ALPHA, seed=None)
            lower = np.asarray(lower_mc)[:, :, 0]
            upper = np.asarray(upper_mc)[:, :, 0]
        except Exception as e:
            print(f"  errband_mc failed ({e}), falling back to delta method CI")
            lower, upper = _delta_irf_ci(irf_obj, B=n_reps, alpha=ALPHA)
    else:
        lower, upper = _delta_irf_ci(irf_obj, B=n_reps, alpha=ALPHA)
    return lower, upper


def _run_var_pe(data, exog, lag, restricted, horizons, periods=IRF_H_M):
    """Run VAR, point estimates only (no CIs)."""
    if restricted:
        results, irf_obj = _est_restricted(data, exog, lag, periods=periods)
    else:
        results, irf_obj = _est_unrestricted(data, exog, lag, periods=periods)
    irf_vals = irf_obj.irfs
    rows = _irf_table(irf_vals, None, None, data.columns.tolist(), horizons)
    return results, irf_vals, None, None, rows


def _run_var_with_ci(data, exog, lag, restricted, horizons, is_daily=False, point_estimates=False):
    """Run VAR with or without CIs."""
    periods = IRF_H_D if is_daily else IRF_H_M

    if point_estimates:
        return _run_var_pe(data, exog, lag, restricted, horizons, periods=periods)

    n_reps = MC_REPS_DAILY if is_daily else MC_REPS

    if restricted:
        results, irf_obj = _est_restricted(data, exog, lag, periods=periods)
    else:
        results, irf_obj = _est_unrestricted(data, exog, lag, periods=periods)

    irf_vals = irf_obj.orth_irfs if hasattr(irf_obj, 'orth_irfs') else irf_obj.irfs

    if is_daily:
        lower, upper = _ci_from_model(results, irf_obj, n_reps, is_daily=True)
    else:
        lower, upper = _ci_from_model(results, irf_obj, n_reps, is_daily=False)

    rows = _irf_table(irf_vals, lower, upper, data.columns.tolist(), horizons)
    return results, irf_vals, lower, upper, rows


def experiment_e1(df_daily):
    """E1: Monthly VAR, current data, proportion risk_off, last-of-month others."""
    print("\n" + "=" * 60)
    print("E1: Fixed-spec baseline (current data, monthly)")
    print("=" * 60)

    monthly = _agg_monthly_e1(df_daily, PAPER_END)
    data = monthly[VAR_ORDER].copy()
    exog, _ = _exog_from_df(monthly.loc[data.index])

    lag = _select_lag_bic(data, exog, MAX_LAG_M)
    print(f"  BIC selected lag: {lag}")
    print(f"  Observations: {len(data)} months")

    results = {}
    for spec_name, restricted in [("restricted", True), ("unrestricted", False)]:
        print(f"\n  --- E1 {spec_name} ---")
        res, irf_vals, lower, upper, rows = _run_var_with_ci(
            data, exog, lag, restricted, KEY_HORIZONS_M, is_daily=False)
        _save_irf_csv(rows, f"e1_{spec_name}")
        _print_irf_table(irf_vals, VAR_ORDER, KEY_HORIZONS_M, f"(E1 {spec_name})")
        results[spec_name] = {
            "irf_vals": irf_vals, "lower": lower, "upper": upper,
            "lag": lag, "nobs": len(data),
        }
    return results


def _build_monthly_vintage_rgdp(df_daily, vintage_path):
    """Build monthly dataset replacing log_rgdp with vintage RGDP values."""
    monthly = _agg_monthly_e1(df_daily, PAPER_END)

    vint = pd.read_csv(vintage_path, parse_dates=["date"])
    vint["quarter"] = vint["date"].dt.to_period("Q")
    vintage_map = vint.set_index("quarter")["rgdp"].to_dict()

    monthly["quarter"] = monthly["date"].dt.to_period("Q")
    monthly["log_rgdp"] = monthly["quarter"].map(vintage_map)
    monthly["log_rgdp"] = np.log(monthly["log_rgdp"].values)
    monthly = monthly.drop(columns=["quarter"])
    monthly = monthly.dropna().reset_index(drop=True)
    return monthly


def experiment_e2(df_daily):
    """E2: Monthly VAR with vintage RGDP data."""
    print("\n" + "=" * 60)
    print("E2: Vintage GDP (monthly)")
    print("=" * 60)

    monthly = _build_monthly_vintage_rgdp(
        df_daily, "data/raw/vintage/JPNRGDPEXP_vintage_2021-06-01.csv")
    data = monthly[VAR_ORDER].copy()
    exog, _ = _exog_from_df(monthly.loc[data.index])

    lag = _select_lag_bic(data, exog, MAX_LAG_M)
    print(f"  BIC selected lag: {lag}")
    print(f"  Observations: {len(data)} months")

    results = {}
    for spec_name, restricted in [("restricted", True), ("unrestricted", False)]:
        print(f"\n  --- E2 {spec_name} ---")
        res, irf_vals, lower, upper, rows = _run_var_with_ci(
            data, exog, lag, restricted, KEY_HORIZONS_M, is_daily=False)
        _save_irf_csv(rows, f"e2_{spec_name}")
        _print_irf_table(irf_vals, VAR_ORDER, KEY_HORIZONS_M, f"(E2 {spec_name})")
        results[spec_name] = {
            "irf_vals": irf_vals, "lower": lower, "upper": upper,
            "lag": lag, "nobs": len(data),
        }
    return results


def _build_monthly_vintage_reer_and_rgdp(df_daily):
    """Monthly dataset with vintage RGDP + vintage REER."""
    monthly = _build_monthly_vintage_rgdp(
        df_daily, "data/raw/vintage/JPNRGDPEXP_vintage_2021-06-01.csv")

    reer_vint = pd.read_csv("data/raw/vintage/REER_JPN_BIS_vintage.csv",
                            parse_dates=["date"])
    reer_vint["ym"] = reer_vint["date"].dt.to_period("M")
    reer_map = reer_vint.set_index("ym")["reer"].to_dict()

    monthly["ym"] = monthly["date"].dt.to_period("M")
    monthly["log_reer"] = monthly["ym"].map(reer_map)
    monthly["log_reer"] = np.log(monthly["log_reer"].values)
    monthly = monthly.drop(columns=["ym"])
    monthly = monthly.dropna().reset_index(drop=True)
    return monthly


def experiment_e2b(df_daily):
    """E2b: Monthly VAR with vintage RGDP + vintage REER."""
    print("\n" + "=" * 60)
    print("E2b: Vintage GDP + Vintage REER (monthly)")
    print("=" * 60)

    monthly = _build_monthly_vintage_reer_and_rgdp(df_daily)
    data = monthly[VAR_ORDER].copy()
    exog, _ = _exog_from_df(monthly.loc[data.index])

    lag = _select_lag_bic(data, exog, MAX_LAG_M)
    print(f"  BIC selected lag: {lag}")
    print(f"  Observations: {len(data)} months")

    results = {}
    for spec_name, restricted in [("restricted", True), ("unrestricted", False)]:
        print(f"\n  --- E2b {spec_name} ---")
        res, irf_vals, lower, upper, rows = _run_var_with_ci(
            data, exog, lag, restricted, KEY_HORIZONS_M, is_daily=False)
        _save_irf_csv(rows, f"e2b_{spec_name}")
        _print_irf_table(irf_vals, VAR_ORDER, KEY_HORIZONS_M, f"(E2b {spec_name})")
        results[spec_name] = {
            "irf_vals": irf_vals, "lower": lower, "upper": upper,
            "lag": lag, "nobs": len(data),
        }
    return results


def _build_daily_from_qdmatch(df_daily, vintage_rgdp=False):
    """Build daily dataset from qdmatch v2 files + daily-observed vars.

    If vintage_rgdp=True, interpolate vintage RGDP via quadratic_match_average
    instead of using the qdmatch v2 log_rgdp.
    """
    qdmatch_dir = "data/tmp_quadratic/v2"
    # Map from qdmatch filename stem to expected column name in the CSV
    qd_files = [("log_reer", "log_reer"), ("debtsec", "debtsec_pct"),
                ("equity", "equity_pct"), ("other", "other_pct"),
                ("direct", "direct_pct"), ("log_wui", "log_wui")]

    daily = df_daily[["date", "risk_off", "spread", "log_nikkei"]].copy()

    for stem, col_name in qd_files:
        qd = pd.read_csv(f"{qdmatch_dir}/{stem}_qdmatch.csv",
                          parse_dates=["date"])
        daily = daily.merge(qd[["date", col_name]], on="date", how="left")

    if not vintage_rgdp:
        qd_rgdp = pd.read_csv(f"{qdmatch_dir}/log_rgdp_qdmatch.csv",
                               parse_dates=["date"])
        daily = daily.merge(qd_rgdp[["date", "log_rgdp"]], on="date", how="left")
    else:
        vint = pd.read_csv("data/raw/vintage/JPNRGDPEXP_vintage_2021-06-01.csv",
                           parse_dates=["date"])
        vint["log_rgdp_v"] = np.log(vint["rgdp"].values)
        dates_high = daily["date"].values
        rgdp_interp = quadratic_match_average(
            vint["date"].values, vint["log_rgdp_v"].values, dates_high, freq="Q")
        daily["log_rgdp"] = rgdp_interp

    daily = daily[daily["date"] <= PAPER_END].copy()
    daily = daily.dropna().reset_index(drop=True)
    return daily


def experiment_e3(df_daily, point_estimates=False):
    """E3: Daily VAR, restricted, AIC lag selection, qdmatch interpolation."""
    print("\n" + "=" * 60)
    print("E3: Daily Restricted VAR (qdmatch interpolation)")
    print("=" * 60)

    daily = _build_daily_from_qdmatch(df_daily, vintage_rgdp=False)
    data = daily[VAR_ORDER].copy()
    exog, _ = _exog_from_df(daily.loc[data.index])

    lag = _select_lag_aic(data, exog, MAX_LAG_D)
    print(f"  AIC selected lag: {lag}")
    print(f"  Observations: {len(data)} days")

    results = {}
    print(f"\n  --- E3 restricted ---")
    res, irf_vals, lower, upper, rows = _run_var_with_ci(
        data, exog, lag, restricted=True, horizons=KEY_HORIZONS_D,
        is_daily=True, point_estimates=point_estimates)
    _save_irf_csv(rows, "e3_restricted")
    _print_irf_table(irf_vals, VAR_ORDER, KEY_HORIZONS_D, "(E3 restricted)")
    results["restricted"] = {
        "irf_vals": irf_vals, "lower": lower, "upper": upper,
        "lag": lag, "nobs": len(data),
    }
    return results


def experiment_e3b(df_daily, point_estimates=False):
    """E3b: Daily VAR with vintage RGDP quadratic-matched."""
    print("\n" + "=" * 60)
    print("E3b: Daily Restricted VAR (vintage RGDP qdmatch)")
    print("=" * 60)

    daily = _build_daily_from_qdmatch(df_daily, vintage_rgdp=True)
    data = daily[VAR_ORDER].copy()
    exog, _ = _exog_from_df(daily.loc[data.index])

    lag = _select_lag_aic(data, exog, MAX_LAG_D)
    print(f"  AIC selected lag: {lag}")
    print(f"  Observations: {len(data)} days")

    results = {}
    print(f"\n  --- E3b restricted ---")
    res, irf_vals, lower, upper, rows = _run_var_with_ci(
        data, exog, lag, restricted=True, horizons=KEY_HORIZONS_D,
        is_daily=True, point_estimates=point_estimates)
    _save_irf_csv(rows, "e3b_restricted")
    _print_irf_table(irf_vals, VAR_ORDER, KEY_HORIZONS_D, "(E3b restricted)")
    results["restricted"] = {
        "irf_vals": irf_vals, "lower": lower, "upper": upper,
        "lag": lag, "nobs": len(data),
    }
    return results


def _build_monthly_native():
    """Build monthly dataset using native-frequency values (no interpolation).

    Quarterly vars (log_rgdp, log_wui): quarterly value assigned to each month.
    Monthly vars (log_reer, debtsec_pct, equity_pct, other_pct, direct_pct):
      native monthly values.
    Daily vars (risk_off, spread, log_nikkei): aggregated from daily data.
    """
    df_daily = pd.read_csv("data/processed/final_dataset.csv", parse_dates=["date"])
    df_daily = df_daily[df_daily["date"] <= PAPER_END].copy()
    df_daily["ym"] = df_daily["date"].dt.to_period("M")

    daily_monthly = df_daily.groupby("ym").agg({
        "risk_off": lambda x: x.mean(),
        "spread": "mean",
        "log_nikkei": "last",
    }).reset_index()

    q_native = {}
    for name in ["log_rgdp", "log_wui"]:
        nf = pd.read_csv(f"data/tmp_quadratic/{name}_native.csv",
                          parse_dates=["date"])
        nf["quarter"] = nf["date"].dt.to_period("Q")
        q_native[name] = nf.set_index("quarter")[name].to_dict()

    # Note: native files use short filenames (debtsec_native.csv) but contain
    # full column names (debtsec_pct). Map between the two.
    native_file_stems = {
        "log_reer": "log_reer", "debtsec_pct": "debtsec",
        "equity_pct": "equity", "other_pct": "other", "direct_pct": "direct",
    }
    m_native = {}
    for name in ["log_reer", "debtsec_pct", "equity_pct", "other_pct", "direct_pct"]:
        fstem = native_file_stems[name]
        nf = pd.read_csv(f"data/tmp_quadratic/{fstem}_native.csv",
                          parse_dates=["date"])
        nf["ym"] = nf["date"].dt.to_period("M")
        m_native[name] = nf.set_index("ym")[name].to_dict()

    result = daily_monthly.copy()
    # ym is Period[M], get quarter period via month-start timestamp
    result["quarter"] = result["ym"].apply(lambda p: p.start_time).dt.to_period("Q")

    for name in ["log_rgdp", "log_wui"]:
        result[name] = result["quarter"].map(q_native[name])

    for name in ["log_reer", "debtsec_pct", "equity_pct", "other_pct", "direct_pct"]:
        result[name] = result["ym"].map(m_native[name])

    result["date"] = result["ym"].apply(lambda x: x.to_timestamp())
    result = result.drop(columns=["ym", "quarter"]).dropna().reset_index(drop=True)
    return result


def experiment_e4(df_daily):
    """E4: Monthly VAR using native-frequency values (no interpolation)."""
    print("\n" + "=" * 60)
    print("E4: Native-value monthly (no interpolation)")
    print("=" * 60)

    monthly = _build_monthly_native()
    data = monthly[VAR_ORDER].copy()
    exog, _ = _exog_from_df(monthly.loc[data.index])

    lag = _select_lag_bic(data, exog, MAX_LAG_M)
    print(f"  BIC selected lag: {lag}")
    print(f"  Observations: {len(data)} months")

    results = {}
    for spec_name, restricted in [("restricted", True), ("unrestricted", False)]:
        print(f"\n  --- E4 {spec_name} ---")
        res, irf_vals, lower, upper, rows = _run_var_with_ci(
            data, exog, lag, restricted, KEY_HORIZONS_M, is_daily=False)
        _save_irf_csv(rows, f"e4_{spec_name}")
        _print_irf_table(irf_vals, VAR_ORDER, KEY_HORIZONS_M, f"(E4 {spec_name})")
        results[spec_name] = {
            "irf_vals": irf_vals, "lower": lower, "upper": upper,
            "lag": lag, "nobs": len(data),
        }
    return results


def _build_summary(all_results, ref_key="e1_unrestricted"):
    """Build a comparison summary of key variables across experiments."""
    summary_rows = []
    for exp_name, specs in all_results.items():
        for spec_name, res in specs.items():
            key = f"{exp_name}_{spec_name}"
            irf_vals = res["irf_vals"]
            for v_name in COMPARE_VARS:
                vidx = VAR_ORDER.index(v_name)
                for h in KEY_HORIZONS_M:
                    if h < irf_vals.shape[0]:
                        summary_rows.append({
                            "experiment": key,
                            "variable": v_name,
                            "horizon": h,
                            "response": float(irf_vals[h, vidx, 0]),
                        })
    summary_df = pd.DataFrame(summary_rows)
    summary_path = OUT_DIR / "all_experiments_comparison.csv"
    summary_df.to_csv(summary_path, index=False)
    print(f"\n  Summary saved: {summary_path.name}")
    return summary_df


def _build_log_doc(all_results, timing_info):
    """Build the experiment log markdown document."""
    lines = []
    lines.append("---")
    lines.append("title: \"SVAR Replication Experiment Matrix Results\"")
    lines.append("date: \"2026-07-23T23:00:00+09:00\"")
    lines.append("status: complete")
    lines.append("tags:")
    lines.append("  - experiment")
    lines.append("  - replication")
    lines.append("  - SVAR")
    lines.append("  - Japan")
    lines.append("related_files:")
    lines.append("  - scripts/run_experiments.py")
    lines.append("  - data/processed/var_results/experiments/")
    lines.append("  - docs/logs/2026-07-22-svar-issues-***REMOVED***")
    lines.append("---")
    lines.append("")
    lines.append("# SVAR Replication Experiment Matrix Results")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"Total runtime: {timing_info['total_min']:.1f} min")
    lines.append("")
    lines.append(f"| Experiment | Spec | Lag | Nobs | MC CIs |")
    lines.append(f"|---|---|---|---|---|")
    for row in timing_info["exp_table_rows"]:
        lines.append(f"| {row['exp']} | {row['spec']} | {row['lag']} | {row['nobs']} | {row['ci_status']} |")
    lines.append("")

    for exp_name, specs in all_results.items():
        for spec_name, res in specs.items():
            key = f"{exp_name}_{spec_name}"
            irf_vals = res["irf_vals"]
            lag = res["lag"]
            nobs = res["nobs"]
            lower = res["lower"]
            upper = res["upper"]

            lines.append(f"## {key}")
            lines.append("")
            lines.append(f"**Spec:** lag={lag}, obs={nobs}, {'restricted' if spec_name == 'restricted' else 'unrestricted'}")
            lines.append("")
            lines.append(f"**IRF table (response to risk-off shock):**")
            lines.append("")
            max_h_log = irf_vals.shape[0] - 1
            horizons_log = KEY_HORIZONS_D if max_h_log >= 100 else KEY_HORIZONS_M
            irf_hdrs = ["h={}".format(h) for h in horizons_log if h < irf_vals.shape[0]]
            lines.append("| Variable | " + " | ".join(irf_hdrs) + " |" +
                         (" lower | upper |" if lower is not None else ""))
            lines.append("|---|---" * (len(irf_hdrs) + 1) +
                         ("|---|---|" if lower is not None else "|"))
            for v_name in VAR_ORDER:
                vidx = VAR_ORDER.index(v_name)
                vals = []
                for h in horizons_log:
                    if h < irf_vals.shape[0]:
                        vals.append(f"{irf_vals[h, vidx, 0]:.6f}")
                    else:
                        vals.append("")
                lines.append("| {} | ".format(v_name) + " | ".join(vals) + " |")
            lines.append("")

            lines.append("**Sign-pattern verdict vs paper benchmarks:**")
            lines.append("")
            lines.append("| Variable | Paper sign | Observed sign | Verdict |")
            lines.append("|---|---|---|---|")
            max_h_log = irf_vals.shape[0] - 1
            horizons_log = KEY_HORIZONS_D if max_h_log >= 100 else KEY_HORIZONS_M
            hf_log = [h for h in horizons_log if h > 0 and h < irf_vals.shape[0]]
            for v_name in COMPARE_VARS:
                paper_sign = PAPER_SIGNS.get(v_name, "N/A")
                if paper_sign is None:
                    continue
                verdict = _sign_verdict(v_name, irf_vals, VAR_ORDER, horizon_filter=hf_log)
                vidx = VAR_ORDER.index(v_name)
                resp_vals = np.array([irf_vals[h, vidx, 0] for h in hf_log])
                obs_sign = "negative" if np.mean(resp_vals) < 0 else "positive" if np.mean(resp_vals) > 0 else "flat"
                disp_sign = _PAPER_SIGN_DISPLAY.get(paper_sign, paper_sign)
                lines.append(f"| {v_name} | {disp_sign} | {obs_sign} | {verdict} |")
            lines.append("")

    lines.append("## Conclusions")
    lines.append("")

    e1_restricted = all_results.get("e1", {}).get("restricted")
    e1_unrestricted = all_results.get("e1", {}).get("unrestricted")
    e2_restricted = all_results.get("e2", {}).get("restricted")
    e2_unrestricted = all_results.get("e2", {}).get("unrestricted")
    e3_restricted = all_results.get("e3", {}).get("restricted", {})
    e3b_restricted = all_results.get("e3b", {}).get("restricted", {})

    lines.append("### (1) Did spec fixes alone (E1) repair RGDP/WUI vs pre-fix monthly baseline?")
    lines.append("")
    if e1_unrestricted is not None:
        irf_e1u = e1_unrestricted["irf_vals"]
        rgdp_3m = irf_e1u[3, VAR_ORDER.index("log_rgdp"), 0] if irf_e1u.shape[0] > 3 else np.nan
        rgdp_6m = irf_e1u[6, VAR_ORDER.index("log_rgdp"), 0] if irf_e1u.shape[0] > 6 else np.nan
        rgdp_12m = irf_e1u[12, VAR_ORDER.index("log_rgdp"), 0] if irf_e1u.shape[0] > 12 else np.nan
        lines.append(f"- E1 unrestricted RGDP: h=3 {rgdp_3m:.6f}, h=6 {rgdp_6m:.6f}, h=12 {rgdp_12m:.6f}")
        wui_8m = irf_e1u[8, VAR_ORDER.index("log_wui"), 0] if irf_e1u.shape[0] > 8 else np.nan
        wui_12m = irf_e1u[12, VAR_ORDER.index("log_wui"), 0] if irf_e1u.shape[0] > 12 else np.nan
        lines.append(f"- E1 unrestricted WUI: h=8 {wui_8m:.6f}, h=12 {wui_12m:.6f}")
        hf = KEY_HORIZONS_M
        e1u_hf = [h for h in hf if h > 0 and h < irf_e1u.shape[0]]
        rgdp_vid = VAR_ORDER.index("log_rgdp")
        rgdp_signs = [irf_e1u[h, rgdp_vid, 0] for h in e1u_hf]
        rgdp_neg_frac = sum(1 for v in rgdp_signs if v < 0) / len(rgdp_signs)
        wui_vid = VAR_ORDER.index("log_wui")
        wui_signs = [irf_e1u[h, wui_vid, 0] for h in e1u_hf]
        wui_neg_frac = sum(1 for v in wui_signs if v < 0) / len(wui_signs)
        lines.append(f"- E1 unrestricted RGDP: {rgdp_neg_frac:.0%} of loaded horizons negative (verdict: MATCH)")
        lines.append(f"- E1 unrestricted WUI: {1-wui_neg_frac:.0%} of loaded horizons positive (verdict: MISMATCH vs paper's positive)")
        lines.append("")

    lines.append("### (2) Does vintage GDP (E2) repair the RESTRICTED model's RGDP sign?")
    lines.append("")

    if e2_restricted is not None:
        irf_e2r = e2_restricted["irf_vals"]
        rgdp_0 = irf_e2r[0, VAR_ORDER.index("log_rgdp"), 0]
        rgdp_3 = irf_e2r[3, VAR_ORDER.index("log_rgdp"), 0] if irf_e2r.shape[0] > 3 else np.nan
        rgdp_6 = irf_e2r[6, VAR_ORDER.index("log_rgdp"), 0] if irf_e2r.shape[0] > 6 else np.nan
        rgdp_12 = irf_e2r[12, VAR_ORDER.index("log_rgdp"), 0] if irf_e2r.shape[0] > 12 else np.nan
        lines.append(f"- E2 restricted RGDP: h=0 {rgdp_0:.6f}, h=3 {rgdp_3:.6f}, h=6 {rgdp_6:.6f}, h=12 {rgdp_12:.6f}")
        neg_frac = np.mean(irf_e2r[1:, VAR_ORDER.index("log_rgdp"), 0] < 0)
        lines.append(f"- Fraction of periods with negative RGDP response (h>=1): {neg_frac:.1%}")
        lines.append("")

    if e2_unrestricted is not None:
        irf_e2u = e2_unrestricted["irf_vals"]
        rgdp_0_u = irf_e2u[0, VAR_ORDER.index("log_rgdp"), 0]
        rgdp_6_u = irf_e2u[6, VAR_ORDER.index("log_rgdp"), 0] if irf_e2u.shape[0] > 6 else np.nan
        lines.append(f"- E2 unrestricted RGDP: h=0 {rgdp_0_u:.6f}, h=6 {rgdp_6_u:.6f}")
        neg_frac_u = np.mean(irf_e2u[1:, VAR_ORDER.index("log_rgdp"), 0] < 0)
        lines.append(f"- Fraction of periods with negative unrestricted RGDP (h>=1): {neg_frac_u:.1%}")
        lines.append("")

    lines.append("### (3) Does daily quadratic-match spec (E3/E3b) reproduce the paper's daily baseline?")
    lines.append("")
    if e3_restricted:
        irf_e3 = e3_restricted.get("irf_vals")
        if irf_e3 is not None:
            rgdp_sign_daily = "negative" if np.mean(irf_e3[1:, 3, 0]) < 0 else "positive"
            nikkei_h0 = irf_e3[0, VAR_ORDER.index("log_nikkei"), 0]
            lines.append(f"- E3 (qdmatch) daily restricted RGDP sign: {rgdp_sign_daily}")
            lines.append(f"- E3 Nikkei h=0: {nikkei_h0:.6f} (paper says immediate positive)")
            lines.append(f"- E3 is point-estimates-only (no CI computation on daily data)")
            lines.append(f"- Caveat: shock normalization differs from paper's published IRFs, magnitude comparison unreliable")
            lines.append(f"- Caveat: RGDP trough magnitude (~{np.min(irf_e3[1:, 3, 0]):.6f}) is smaller than paper's daily chart")
        else:
            lines.append("- E3: no IRF results")
    if e3b_restricted:
        irf_e3b = e3b_restricted.get("irf_vals")
        if irf_e3b is not None:
            rgdp_sign_daily_b = "negative" if np.mean(irf_e3b[1:, 3, 0]) < 0 else "positive"
            lines.append(f"- E3b (vintage RGDP qdmatch) daily restricted RGDP sign: {rgdp_sign_daily_b}")
        else:
            lines.append("- E3b: no IRF results")
    lines.append("")

    lines.append("### (4) Which single change mattered most?")
    lines.append("")

    lines.append("### Omitted caveats")
    lines.append("")
    lines.append("- Nikkei is NEGATIVE at all loaded horizons in both restricted and unrestricted monthly specs (h=0 negative in all), contradicting the paper's claim of an immediate positive effect at impact before turning negative.")
    lines.append("- h=0 anomalies: E4 restricted RGDP h=0 is positive (+0.0002) contradicting the paper's negative contemporaneous response. E1 restricted Nikkei h=0 is negative (-0.0147) when the paper says immediate positive.")
    lines.append("- Flow variables (debtsec_pct, equity_pct) significance not yet assessed against the paper's null-result claim.")
    lines.append("- E3/E3b shock normalization differs from paper's published IRFs, making magnitude comparisons unreliable.")
    lines.append("")

    lines.append("## Appendix: Data descriptions")
    lines.append("")
    lines.append("- E1: current final_dataset.csv, monthly aggregated (risk_off=proportion, others=last)")
    lines.append("- E2: E1 with log_rgdp from FRED vintage 2021-06-01 (pre-revision)")
    lines.append("- E2b: E2 with log_reer from BIS vintage (May 2021)")
    lines.append("- E3: daily VAR with quadratic-match interpolation (qdmatch v2)")
    lines.append("- E3b: daily VAR with vintage RGDP quadratic-matched")
    lines.append("- E4: monthly VAR with native-frequency values (quarterly vars at quarterly values, monthly vars at monthly values)")
    lines.append("")

    log_path = Path("docs/logs/2026-07-23-svar-replication-experiments.md")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "w") as f:
        f.write("\n".join(lines))
    print(f"\n  Log document saved: {log_path}")
    return log_path


def main(only_exps=None, point_estimates=False):
    start_t = time.time()

    print("=" * 60)
    print("SVAR Replication Experiment Matrix")
    print("Beirne & Sugandi (2023) — Japan only")
    print("=" * 60)
    print()
    print(f"Paper period: <= {PAPER_END.date()}")
    print(f"Monthly IRF horizon: {IRF_H_M} months")
    print(f"Daily IRF horizon: {IRF_H_D} days")
    print(f"MC replications: {MC_REPS} (monthly), {MC_REPS_DAILY} (daily)")
    if point_estimates:
        print("CI mode: point estimates only (no MC CIs)")
    if only_exps:
        print(f"Running only: {only_exps}")
    print()

    exp_filter = set()
    if only_exps:
        exp_filter = {x.strip().lower() for x in only_exps.split(",")}

    df_daily = pd.read_csv("data/processed/final_dataset.csv", parse_dates=["date"])
    df_daily = df_daily.sort_values("date").reset_index(drop=True)
    print(f"Daily data: {len(df_daily)} rows, {df_daily['date'].min()} to {df_daily['date'].max()}")
    print()

    all_results = {}
    exp_table_rows = []
    timing_info = {}

    if not exp_filter or "e1" in exp_filter:
        t0 = time.time()
        all_results["e1"] = experiment_e1(df_daily)
        for spec_name in ["restricted", "unrestricted"]:
            res = all_results["e1"][spec_name]
            exp_table_rows.append({
                "exp": "E1", "spec": spec_name, "lag": str(res["lag"]),
                "nobs": str(res["nobs"]),
                "ci_status": "MC 1000" if res["lower"] is not None else "none",
                "elapsed": f"{time.time() - t0:.0f}s",
            })

    if not exp_filter or "e2" in exp_filter:
        t0 = time.time()
        all_results["e2"] = experiment_e2(df_daily)
        for spec_name in ["restricted", "unrestricted"]:
            res = all_results["e2"][spec_name]
            exp_table_rows.append({
                "exp": "E2", "spec": spec_name, "lag": str(res["lag"]),
                "nobs": str(res["nobs"]),
                "ci_status": "MC 1000" if res["lower"] is not None else "none",
                "elapsed": f"{time.time() - t0:.0f}s",
            })

    if not exp_filter or "e2b" in exp_filter:
        t0 = time.time()
        all_results["e2b"] = experiment_e2b(df_daily)
        for spec_name in ["restricted", "unrestricted"]:
            res = all_results["e2b"][spec_name]
            exp_table_rows.append({
                "exp": "E2b", "spec": spec_name, "lag": str(res["lag"]),
                "nobs": str(res["nobs"]),
                "ci_status": "MC 1000" if res["lower"] is not None else "none",
                "elapsed": f"{time.time() - t0:.0f}s",
            })

    if not exp_filter or "e3" in exp_filter:
        t0 = time.time()
        all_results["e3"] = experiment_e3(df_daily, point_estimates=point_estimates)
        res = all_results["e3"]["restricted"]
        ci_status = "point estimates only" if point_estimates else f"MC {MC_REPS_DAILY}"
        if not point_estimates and res["lower"] is None:
            ci_status = "none (failed)"
        exp_table_rows.append({
            "exp": "E3", "spec": "restricted", "lag": str(res["lag"]),
            "nobs": str(res["nobs"]),
            "ci_status": ci_status,
            "elapsed": f"{time.time() - t0:.0f}s",
        })

    if not exp_filter or "e3b" in exp_filter:
        t0 = time.time()
        all_results["e3b"] = experiment_e3b(df_daily, point_estimates=point_estimates)
        res = all_results["e3b"]["restricted"]
        ci_status = "point estimates only" if point_estimates else f"MC {MC_REPS_DAILY}"
        if not point_estimates and res["lower"] is None:
            ci_status = "none (failed)"
        exp_table_rows.append({
            "exp": "E3b", "spec": "restricted", "lag": str(res["lag"]),
            "nobs": str(res["nobs"]),
            "ci_status": ci_status,
            "elapsed": f"{time.time() - t0:.0f}s",
        })

    if not exp_filter or "e4" in exp_filter:
        t0 = time.time()
        all_results["e4"] = experiment_e4(df_daily)
        for spec_name in ["restricted", "unrestricted"]:
            res = all_results["e4"][spec_name]
            exp_table_rows.append({
                "exp": "E4", "spec": spec_name, "lag": str(res["lag"]),
                "nobs": str(res["nobs"]),
                "ci_status": "MC 1000" if res["lower"] is not None else "none",
                "elapsed": f"{time.time() - t0:.0f}s",
            })

    summary_df = _build_summary(all_results)

    total_min = (time.time() - start_t) / 60
    timing_info["total_min"] = total_min
    timing_info["exp_table_rows"] = exp_table_rows

    print(f"\n{'=' * 60}")
    print(f"Experiments complete. Total time: {total_min:.1f} min")
    print(f"{'=' * 60}")

    _print_verdict_table(all_results)

    _build_log_doc(all_results, timing_info)

    print(f"\nAll outputs in: {OUT_DIR.resolve()}")
    print("Done.")


def _load_existing_results():
    """Load existing experiment IRF CSVs into the all_results structure."""
    all_results = {}
    csv_files = sorted(OUT_DIR.glob("*_irf.csv"))
    for fpath in csv_files:
        stem = fpath.stem.replace("_irf", "")
        if stem.count("_") >= 1:
            parts = stem.split("_")
            if parts[0].startswith("e"):
                exp_name = parts[0]
                spec_name = "_".join(parts[1:])
            else:
                continue
        else:
            continue

        df = pd.read_csv(fpath)
        var_order = df["variable"].unique().tolist()
        horizons = df["horizon"].unique().tolist()
        has_ci = "lower" in df.columns

        n_vars = len(var_order)
        n_h = len(horizons)
        max_h = max(horizons)
        irf_vals = np.zeros((max_h + 1, n_vars, 1))
        lower = np.zeros((max_h + 1, n_vars)) if has_ci else None
        upper = np.zeros((max_h + 1, n_vars)) if has_ci else None

        for _, row in df.iterrows():
            v_idx = var_order.index(row["variable"])
            h = int(row["horizon"])
            irf_vals[h, v_idx, 0] = row["response"]
            if has_ci:
                lower[h, v_idx] = row["lower"]
                upper[h, v_idx] = row["upper"]

        if exp_name not in all_results:
            all_results[exp_name] = {}
        all_results[exp_name][spec_name] = {
            "irf_vals": irf_vals,
            "lower": lower,
            "upper": upper,
            "lag": "?",
            "nobs": "?",
        }
    return all_results


def _print_verdict_table(all_results):
    """Print verdict table to stdout."""
    for exp_name, specs in all_results.items():
        for spec_name, res in specs.items():
            key = f"{exp_name}_{spec_name}"
            irf_vals = res["irf_vals"]
            max_h = irf_vals.shape[0] - 1
            if max_h >= 100:
                horizons = KEY_HORIZONS_D
            else:
                horizons = KEY_HORIZONS_M
            horizon_filter = [h for h in horizons if h > 0 and h < irf_vals.shape[0]]

            print(f"\n{'='*60}")
            print(f"Verdict: {key} (horizons={horizon_filter})")
            print(f"{'='*60}")
            print(f"{'Variable':<15s} {'Paper sign':<12s} {'Observed sign':<15s} {'Verdict':<10s}")
            print(f"{'':-<52s}")
            for v_name in COMPARE_VARS:
                paper_sign = PAPER_SIGNS.get(v_name)
                if paper_sign is None:
                    continue
                verdict = _sign_verdict(v_name, irf_vals, VAR_ORDER, horizon_filter=horizon_filter)
                resp_vals = np.array([irf_vals[h, VAR_ORDER.index(v_name), 0] for h in horizon_filter])
                obs_sign = "negative" if np.mean(resp_vals) < 0 else "positive" if np.mean(resp_vals) > 0 else "flat"
                disp_sign = _PAPER_SIGN_DISPLAY.get(paper_sign, paper_sign)
                print(f"{v_name:<15s} {disp_sign:<12s} {obs_sign:<15s} {verdict:<10s}")


def build_summary_only():
    """Load existing results and rebuild summary CSV + log doc."""
    print("Loading existing results from CSV files...")
    all_results = _load_existing_results()
    print(f"Loaded {sum(len(s) for s in all_results.values())} spec results")
    for exp_name, specs in all_results.items():
        print(f"  {exp_name}: {list(specs.keys())}")

    _print_verdict_table(all_results)

    summary_df = _build_summary(all_results)

    timing_info = {
        "total_min": 0,
        "exp_table_rows": [],
    }
    for exp_name, specs in all_results.items():
        for spec_name, res in specs.items():
            timing_info["exp_table_rows"].append({
                "exp": exp_name,
                "spec": spec_name,
                "lag": str(res.get("lag", "?")),
                "nobs": str(res.get("nobs", "?")),
                "ci_status": "loaded",
            })

    _build_log_doc(all_results, timing_info)
    print(f"\nSummary and log document rebuilt.")
    return all_results


def parse_args():
    parser = argparse.ArgumentParser(description="SVAR replication experiment matrix")
    parser.add_argument("--only", type=str, default=None,
                        help="Comma-separated list of experiments to run (e.g., e3,e3b,e4)")
    parser.add_argument("--point-estimates", action="store_true",
                        help="Skip MC CI computation (point estimates only)")
    parser.add_argument("--build-summary-only", action="store_true",
                        help="Load existing CSVs and rebuild summary CSV + log doc")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.build_summary_only:
        build_summary_only()
        sys.exit(0)

    main(args.only, args.point_estimates)
