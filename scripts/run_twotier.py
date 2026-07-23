"""
Two-tier SVAR estimation for Beirne & Sugandi (2023) replication + extension.

Usage:
  uv run python scripts/run_twotier.py
  uv run python scripts/run_twotier.py --with-daily-ci --repl 1000

Outputs: data/processed/var_results/twotier/
"""

import os
import sys
import time
import argparse
import warnings
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

from statsmodels.tsa.api import VAR
from scripts.var_analysis import run_var, build_exog, _delta_irf_ci
from scripts.quadratic_match import quadratic_match_average

VAR_ORDER = [
    "risk_off", "log_wui", "spread", "log_rgdp", "log_reer",
    "log_nikkei", "debtsec_pct", "equity_pct", "other_pct", "direct_pct",
]

PAPER_END = pd.Timestamp("2021-03-31")
EXTENDED_END = pd.Timestamp("2026-06-30")
IRF_H_DAILY = 125
IRF_H_MONTHLY = 40
MAX_LAG_DAILY = 20
MAX_LAG_MONTHLY = 12
ALPHA = 0.05
MC_REPL_DEFAULT = 1000
RNG_SEED = 42

OUT_DIR = Path("data/processed/var_results/twotier")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FLOW_VARS = ["debtsec_pct", "equity_pct", "other_pct", "direct_pct"]
FLOW_HORIZONS = [1, 3, 6, 12, 24]
COMPARE_HORIZONS_M = [0, 1, 3, 6, 12, 24, 40]
COMPARE_HORIZONS_D = [0, 1, 3, 6, 12, 24, 125]


def _select_lag_aic(data, exog, maxlags):
    model = VAR(endog=data, exog=exog)
    order = model.select_order(maxlags=maxlags, trend="n")
    return int(order.selected_orders["aic"])


def _select_lag_bic(data, exog, maxlags):
    model = VAR(endog=data, exog=exog)
    order = model.select_order(maxlags=maxlags, trend="n")
    return int(order.selected_orders["bic"])


def _agg_monthly(df, end_date):
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


def _load_qdmatch(stem, col_name):
    path = f"data/tmp_quadratic/v2/{stem}_qdmatch.csv"
    qd = pd.read_csv(path, parse_dates=["date"])
    return qd[["date", col_name]]


def _build_daily_paper(df_daily):
    """Paper-period daily dataset with vintage RGDP + vintage REER interpolated."""
    daily = df_daily[["date", "risk_off", "spread", "log_nikkei"]].copy()
    daily = daily[daily["date"] <= PAPER_END].copy()
    qd_files = [("log_wui", "log_wui"), ("debtsec", "debtsec_pct"),
                ("equity", "equity_pct"), ("other", "other_pct"),
                ("direct", "direct_pct")]
    for stem, col in qd_files:
        qd = _load_qdmatch(stem, col)
        daily = daily.merge(qd, on="date", how="left")
    # Vintage RGDP: log of levels, quadratic-match interpolated
    vint_rgdp = pd.read_csv(
        "data/raw/vintage/JPNRGDPEXP_vintage_2021-06-01.csv", parse_dates=["date"])
    vint_rgdp["log_rgdp_v"] = np.log(vint_rgdp["rgdp"].values)
    daily["log_rgdp"] = quadratic_match_average(
        vint_rgdp["date"].values, vint_rgdp["log_rgdp_v"].values,
        daily["date"].values, freq="Q")
    # Vintage REER: log of levels, quadratic-match interpolated
    vint_reer = pd.read_csv(
        "data/raw/vintage/REER_JPN_BIS_vintage.csv", parse_dates=["date"])
    vint_reer["log_reer_v"] = np.log(vint_reer["reer"].values)
    daily["log_reer"] = quadratic_match_average(
        vint_reer["date"].values, vint_reer["log_reer_v"].values,
        daily["date"].values, freq="M")
    daily = daily.dropna().reset_index(drop=True)
    return daily


def _build_daily_extended(df_daily):
    """Extended-period daily dataset with current-vintage qdmatch data."""
    daily = df_daily[["date", "risk_off", "spread", "log_nikkei"]].copy()
    qd_stems = [("log_reer", "log_reer"), ("debtsec", "debtsec_pct"),
                ("equity", "equity_pct"), ("other", "other_pct"),
                ("direct", "direct_pct"), ("log_wui", "log_wui"),
                ("log_rgdp", "log_rgdp")]
    for stem, col in qd_stems:
        qd = _load_qdmatch(stem, col)
        daily = daily.merge(qd, on="date", how="left")
    daily = daily.dropna().reset_index(drop=True)
    return daily


def _build_monthly_paper_vintage(df_daily):
    """Monthly paper-period dataset with vintage RGDP + vintage REER."""
    monthly = _agg_monthly(df_daily, PAPER_END)
    vint_rgdp = pd.read_csv(
        "data/raw/vintage/JPNRGDPEXP_vintage_2021-06-01.csv", parse_dates=["date"])
    vint_rgdp["quarter"] = vint_rgdp["date"].dt.to_period("Q")
    rgdp_map = vint_rgdp.set_index("quarter")["rgdp"].to_dict()
    monthly["quarter"] = monthly["date"].dt.to_period("Q")
    monthly["log_rgdp"] = monthly["quarter"].map(rgdp_map)
    monthly["log_rgdp"] = np.log(monthly["log_rgdp"].values)
    monthly = monthly.drop(columns=["quarter"])
    vint_reer = pd.read_csv(
        "data/raw/vintage/REER_JPN_BIS_vintage.csv", parse_dates=["date"])
    vint_reer["ym"] = vint_reer["date"].dt.to_period("M")
    reer_map = vint_reer.set_index("ym")["reer"].to_dict()
    monthly["ym"] = monthly["date"].dt.to_period("M")
    monthly["log_reer"] = monthly["ym"].map(reer_map)
    monthly["log_reer"] = np.log(monthly["log_reer"].values)
    monthly = monthly.drop(columns=["ym"])
    monthly = monthly.dropna().reset_index(drop=True)
    return monthly


def _build_monthly_extended(df_daily):
    """Monthly extended-period dataset with current data."""
    return _agg_monthly(df_daily, EXTENDED_END)


def _run_restricted_var(data, exog, lag, periods):
    results = run_var(data, exog, restricted=True, k_ar=lag)
    irf_obj = results.irf(periods=periods)
    irf_vals = irf_obj.irfs
    return results, irf_vals


def _run_unrestricted_var(data, exog, lag, periods):
    model = VAR(endog=data, exog=exog)
    results = model.fit(lag, trend="n")
    irf_obj = results.irf(periods=periods)
    irf_vals = np.asarray(irf_obj.orth_irfs)
    return results, irf_vals


def _ci_restricted(results, irf_vals, repl, seed=42):
    """Compute CIs for restricted VAR via Monte Carlo delta method."""
    np.random.seed(seed)
    dummy_irf = type("DummyIRF", (), {
        "irfs": irf_vals,
        "model": results,
        "periods": irf_vals.shape[0] - 1,
    })()
    lower, upper = _delta_irf_ci(dummy_irf, B=repl, alpha=ALPHA)
    return lower, upper


def _ci_unrestricted(results, irf_obj, repl, seed=42):
    """Compute CIs for unrestricted VAR via statsmodels errband_mc.
    Note: seed is set globally then passed as None to work around a
    statsmodels bug where integer seed makes bands degenerate."""
    try:
        np.random.seed(seed)
        lower_mc, upper_mc = irf_obj.errband_mc(
            orth=True, repl=repl, signif=ALPHA, seed=None)
        lower = np.asarray(lower_mc)[:, :, 0]
        upper = np.asarray(upper_mc)[:, :, 0]
    except Exception:
        lower, upper = _delta_irf_ci(irf_obj, B=repl, alpha=ALPHA)
    return lower, upper


def _irf_rows(irf_vals, lower, upper, var_order, horizons):
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


def _save_irf_csv(rows, filename):
    path = OUT_DIR / filename
    pd.DataFrame(rows).to_csv(path, index=False)
    print(f"  Saved: {path.name}")
    return path


def _print_signs(label, irf_vals, var_order, horizons):
    print(f"\n  Sign check [{label}]:")
    check_vars = ["log_rgdp", "log_reer", "spread"]
    for v in check_vars:
        vi = var_order.index(v)
        vals = [irf_vals[h, vi, 0] for h in horizons if h < irf_vals.shape[0]]
        if vals:
            n = len(vals)
            h1 = f"{vals[0]:.6f}" if n > 0 else "NA"
            h6 = f"{vals[1]:.6f}" if n > 1 else "NA"
            h12 = f"{vals[2]:.6f}" if n > 2 else "NA"
            print(f"    {v}: h=1={h1}, h=6={h6}, h=12={h12}")


def _estimate_monthly(data, exog, label, repl, var_order=VAR_ORDER,
                      periods=IRF_H_MONTHLY, maxlags=MAX_LAG_MONTHLY):
    lag = _select_lag_bic(data, exog, maxlags)
    print(f"\n  {label} — BIC lag: {lag}, obs: {len(data)}")

    # Restricted
    print(f"  Estimating restricted VAR...")
    res_r, irf_r = _run_restricted_var(data, exog, lag, periods)
    print(f"  Computing restricted CIs (MC delta, B={repl})...")
    lower_r, upper_r = _ci_restricted(res_r, irf_r, repl)
    rows_r = _irf_rows(irf_r, lower_r, upper_r, var_order,
                       list(range(irf_r.shape[0])))

    # Unrestricted
    print(f"  Estimating unrestricted VAR...")
    res_u, irf_u = _run_unrestricted_var(data, exog, lag, periods)
    print(f"  Computing unrestricted CIs (errband_mc, B={repl})...")
    lower_u, upper_u = _ci_unrestricted(res_u, res_u.irf(periods=periods), repl)
    rows_u = _irf_rows(irf_u, lower_u, upper_u, var_order,
                       list(range(irf_u.shape[0])))

    _print_signs(label, irf_r, var_order, [1, 6, 12])
    _print_signs(label + " (unrestricted)", irf_u, var_order, [1, 6, 12])

    return {
        "restricted": {"irf": irf_r, "lower": lower_r, "upper": upper_r, "lag": lag},
        "unrestricted": {"irf": irf_u, "lower": lower_u, "upper": upper_u, "lag": lag},
        "rows_r": rows_r,
        "rows_u": rows_u,
    }


def _estimate_daily(data, exog, label, with_ci, repl,
                    var_order=VAR_ORDER, periods=IRF_H_DAILY, maxlags=MAX_LAG_DAILY):
    lag = _select_lag_aic(data, exog, maxlags)
    print(f"\n  {label} — AIC lag: {lag}, obs: {len(data)}")

    # Restricted only for daily
    print(f"  Estimating daily restricted VAR...")
    res_r, irf_r = _run_restricted_var(data, exog, lag, periods)

    lower_r, upper_r = None, None
    if with_ci:
        print(f"  Computing daily restricted CIs (MC delta, B={repl})...")
        lower_r, upper_r = _ci_restricted(res_r, irf_r, repl)

    rows_r = _irf_rows(irf_r, lower_r, upper_r, var_order,
                       list(range(irf_r.shape[0])))

    _print_signs(label, irf_r, var_order, [1, 6, 12])

    return {
        "restricted": {"irf": irf_r, "lower": lower_r, "upper": upper_r, "lag": lag},
        "rows_r": rows_r,
    }


def _build_comparison_table(all_runs):
    rows = []
    tier_key_map = {
        ("daily", "paper"): "daily_paper",
        ("daily", "extended"): "daily_extended",
        ("monthly", "paper"): "monthly_paper",
        ("monthly", "extended"): "monthly_extended",
    }
    for (tier, period), key in tier_key_map.items():
        run = all_runs.get(key)
        if run is None:
            continue
        for spec_name in ["restricted", "unrestricted"]:
            spec = run.get(spec_name)
            if spec is None:
                continue
            irf = spec["irf"]
            lo = spec.get("lower")
            hi = spec.get("upper")
            horizons = (COMPARE_HORIZONS_D if tier == "daily"
                        else COMPARE_HORIZONS_M)
            for v_idx, v_name in enumerate(VAR_ORDER):
                for h in horizons:
                    if h >= irf.shape[0]:
                        continue
                    row = {
                        "tier": tier,
                        "period": period,
                        "specification": spec_name,
                        "variable": v_name,
                        "horizon": h,
                        "response": float(irf[h, v_idx, 0]),
                    }
                    if lo is not None:
                        row["lower"] = float(lo[h, v_idx])
                        row["upper"] = float(hi[h, v_idx])
                    rows.append(row)
    return pd.DataFrame(rows)


def _build_flow_significance(run_key, all_runs):
    run = all_runs.get(run_key)
    if run is None:
        return None
    rows = []
    for spec_name in ["restricted", "unrestricted"]:
        spec = run.get(spec_name)
        if spec is None:
            continue
        irf = spec["irf"]
        lo = spec.get("lower")
        hi = spec.get("upper")
        if lo is None or hi is None:
            continue
        for v_name in FLOW_VARS:
            v_idx = VAR_ORDER.index(v_name)
            for h in FLOW_HORIZONS:
                if h >= irf.shape[0]:
                    continue
                resp = float(irf[h, v_idx, 0])
                l = float(lo[h, v_idx])
                u = float(hi[h, v_idx])
                rows.append({
                    "specification": spec_name,
                    "variable": v_name,
                    "horizon": h,
                    "response": resp,
                    "lower": l,
                    "upper": u,
                    "significant_95": (l > 0) or (u < 0),
                })
    return pd.DataFrame(rows)


def print_flow_verdict(flow_df):
    if flow_df is None or len(flow_df) == 0:
        print("  (no flow significance data)")
        return
    sig = flow_df[flow_df["significant_95"] == True]
    if len(sig) == 0:
        print("  FLOW SIGNIFICANCE: ALL FLOWS INSIGNIFICANT at 95% (matches paper)")
    else:
        print(f"  FLOW SIGNIFICANCE: {len(sig)} significant entries found:")
        for _, r in sig.iterrows():
            print(f"    {r['variable']} h={r['horizon']} ({r['specification']}): "
                  f"resp={r['response']:.6f} [{r['lower']:.6f}, {r['upper']:.6f}]")


def main():
    parser = argparse.ArgumentParser(description="Two-tier SVAR estimation runner")
    parser.add_argument("--with-daily-ci", action="store_true",
                        help="Compute daily restricted CIs (slow, use on fast machine)")
    parser.add_argument("--repl", type=int, default=MC_REPL_DEFAULT,
                        help=f"MC bootstrap replications (default: {MC_REPL_DEFAULT})")
    args = parser.parse_args()

    print("=" * 60)
    print("Two-Tier SVAR — Beirne & Sugandi (2023) Replication + Extension")
    print("=" * 60)
    print(f"Paper period:  {PAPER_END.date()}")
    print(f"Extended end:  {EXTENDED_END.date()}")
    print(f"Daily IRF:     {IRF_H_DAILY} days (restricted)")
    print(f"Monthly IRF:   {IRF_H_MONTHLY} months (restricted + unrestricted)")
    print(f"MC repl:       {args.repl}")
    print(f"Daily CIs:     {'YES' if args.with_daily_ci else 'point estimates only (fast)'}")
    print()

    t_start = time.time()

    df_daily = pd.read_csv("data/processed/final_dataset.csv", parse_dates=["date"])
    df_daily = df_daily.sort_values("date").reset_index(drop=True)
    print(f"Daily data: {len(df_daily)} rows, {df_daily['date'].min()} to {df_daily['date'].max()}")
    print()

    all_runs = {}

    # TIER 1: Daily restricted
    print("-" * 60)
    print("TIER 1: DAILY RESTRICTED VAR")
    print("-" * 60)

    # Daily paper (vintage RGDP + REER)
    print("\nBuilding daily paper-period dataset (vintage RGDP + REER)...")
    daily_paper = _build_daily_paper(df_daily)
    exog_p, _ = build_exog(daily_paper.loc[daily_paper[VAR_ORDER].dropna().index])
    data_p = daily_paper[VAR_ORDER].dropna()
    res_daily_paper = _estimate_daily(
        data_p, exog_p, "Daily paper (restricted)",
        with_ci=args.with_daily_ci, repl=args.repl)
    _save_irf_csv(res_daily_paper["rows_r"], "daily_paper_irf.csv")
    all_runs["daily_paper"] = res_daily_paper

    # Daily extended (current data)
    print("\nBuilding daily extended-period dataset...")
    daily_ext = _build_daily_extended(df_daily)
    exog_e, _ = build_exog(daily_ext.loc[daily_ext[VAR_ORDER].dropna().index])
    data_e = daily_ext[VAR_ORDER].dropna()
    res_daily_ext = _estimate_daily(
        data_e, exog_e, "Daily extended (restricted)",
        with_ci=args.with_daily_ci, repl=args.repl)
    _save_irf_csv(res_daily_ext["rows_r"], "daily_extended_irf.csv")
    all_runs["daily_extended"] = res_daily_ext

    # TIER 2: Monthly restricted + unrestricted
    print("\n" + "-" * 60)
    print("TIER 2: MONTHLY RESTRICTED + UNRESTRICTED VAR")
    print("-" * 60)

    # Monthly paper (vintage RGDP + REER)
    print("\nBuilding monthly paper-period dataset (vintage RGDP + REER)...")
    monthly_paper = _build_monthly_paper_vintage(df_daily)
    exog_mp, _ = build_exog(monthly_paper.loc[monthly_paper[VAR_ORDER].dropna().index])
    data_mp = monthly_paper[VAR_ORDER].dropna()
    res_monthly_paper = _estimate_monthly(
        data_mp, exog_mp, "Monthly paper (vintage)",
        repl=args.repl)
    _save_irf_csv(res_monthly_paper["rows_r"], "monthly_paper_restricted_irf.csv")
    _save_irf_csv(res_monthly_paper["rows_u"], "monthly_paper_unrestricted_irf.csv")
    all_runs["monthly_paper"] = res_monthly_paper

    # Monthly extended (current data)
    print("\nBuilding monthly extended-period dataset...")
    monthly_ext = _build_monthly_extended(df_daily)
    exog_me, _ = build_exog(monthly_ext.loc[monthly_ext[VAR_ORDER].dropna().index])
    data_me = monthly_ext[VAR_ORDER].dropna()
    res_monthly_ext = _estimate_monthly(
        data_me, exog_me, "Monthly extended",
        repl=args.repl)
    _save_irf_csv(res_monthly_ext["rows_r"], "monthly_extended_restricted_irf.csv")
    _save_irf_csv(res_monthly_ext["rows_u"], "monthly_extended_unrestricted_irf.csv")
    all_runs["monthly_extended"] = res_monthly_ext

    # COMPARISON TABLE
    print("\n" + "-" * 60)
    print("BUILDING COMPARISON AND FLOW SIGNIFICANCE TABLES")
    print("-" * 60)
    comp_df = _build_comparison_table(all_runs)
    comp_df.to_csv(OUT_DIR / "comparison_paper_vs_extended.csv", index=False)
    print(f"  Saved: comparison_paper_vs_extended.csv ({len(comp_df)} rows)")

    # FLOW SIGNIFICANCE (from monthly paper results — matches paper's monthly VAR)
    flow_df = _build_flow_significance("monthly_paper", all_runs)
    if flow_df is not None:
        flow_df.to_csv(OUT_DIR / "flow_significance.csv", index=False)
        print(f"  Saved: flow_significance.csv ({len(flow_df)} rows)")
    else:
        print("  (flow_significance not available — monthly paper CIs missing)")

    # Print verdict
    print("\n" + "=" * 60)
    print("FLOW SIGNIFICANCE VERDICT (monthly paper)")
    print("=" * 60)
    print_flow_verdict(flow_df)

    elapsed = time.time() - t_start
    print(f"\nTotal time: {elapsed:.1f}s ({elapsed/60:.1f} min)")
    print(f"All outputs in: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
