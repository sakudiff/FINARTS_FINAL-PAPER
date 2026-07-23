"""
Unified SVAR replication script for Beirne & Sugandi (2023).

Usage:
  uv run python scripts/replicate_svar.py                           # full pipeline
  uv run python scripts/replicate_svar.py --interpolate-v1          # v1 daily only
  uv run python scripts/replicate_svar.py --with-daily-ci --repl 1000  # with CIs
  uv run python scripts/replicate_svar.py --verify                  # compare outputs
"""

import os
import sys
import time
import argparse
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)


VAR_ORDER = [
    "risk_off", "log_wui", "spread", "log_rgdp", "log_reer",
    "log_nikkei", "debtsec_pct", "equity_pct", "other_pct", "direct_pct",
]

REPO_ROOT = Path(__file__).resolve().parent.parent
PAPER_END = pd.Timestamp("2021-03-31")
EXTENDED_END = pd.Timestamp("2026-06-30")
IRF_H_DAILY = 125
IRF_H_MONTHLY = 40
MAX_LAG_DAILY = 20
MAX_LAG_MONTHLY = 12
ALPHA = 0.05
MC_REPL_DEFAULT = 1000
RNG_SEED = 42

FIG_DIR = Path("data/processed/var_results/figures")
PAPER_COLOR = "#2E45B8"
EXT_COLOR = "#F97A1F"
ZERO_COLOR = "#595959"

TMP_DIR = Path("data/tmp_quadratic")
V2_DIR = TMP_DIR / "v2"
OUT_DIR = Path("data/processed/var_results")
TWOTIER_DIR = OUT_DIR / "twotier"

FLOW_VARS = ["debtsec_pct", "equity_pct", "other_pct", "direct_pct"]
FLOW_HORIZONS = [1, 3, 6, 12, 24]
COMPARE_HORIZONS_M = [0, 1, 3, 6, 12, 24, 40]
COMPARE_HORIZONS_D = [0, 1, 3, 6, 12, 24, 125]

START_DATE_V1 = pd.Timestamp("1999-01-01")
END_DATE_V1 = pd.Timestamp("2026-06-30")

V1_SERIES = [
    ("log_reer_native.csv", "log_reer"),
    ("debtsec_native.csv", "debtsec_pct"),
    ("equity_native.csv", "equity_pct"),
    ("other_native.csv", "other_pct"),
    ("direct_native.csv", "direct_pct"),
    ("log_rgdp_native.csv", "log_rgdp"),
    ("log_wui_native.csv", "log_wui"),
]

# qdmatch series: (native_stem, value_col, freq)
QDMATCH_SERIES = [
    ("log_reer", "log_reer", "M"),
    ("debtsec", "debtsec_pct", "M"),
    ("equity", "equity_pct", "M"),
    ("other", "other_pct", "M"),
    ("direct", "direct_pct", "M"),
    ("log_rgdp", "log_rgdp", "Q"),
    ("log_wui", "log_wui", "Q"),
]


def _v1_interpolate_series(in_path, value_col, out_path):
    """Read native CSV, quadratic-interpolate to daily grid, write."""
    all_dates = pd.date_range(START_DATE_V1, END_DATE_V1, freq="D")
    df = pd.read_csv(in_path, parse_dates=["date"])
    df = df.set_index("date")
    df = df.reindex(all_dates)
    df[value_col] = df[value_col].interpolate(method="quadratic")
    df = df.reset_index().rename(columns={"index": "date"})
    df.to_csv(out_path, index=False)


def run_interpolate_v1():
    """Regenerate data/tmp_quadratic/*_daily.csv from natives (v1 method)."""
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    for native_name, value_col in V1_SERIES:
        stem = native_name.replace("_native.csv", "")
        in_path = TMP_DIR / native_name
        out_path = TMP_DIR / f"{stem}_daily.csv"
        print(f"  V1 interpolate: {native_name} -> {out_path.name}")
        _v1_interpolate_series(str(in_path), value_col, str(out_path))
    print("  Done.")


def _month_key(d):
    return (d.year, d.month)

def _quarter_key(d):
    return (d.year, (d.month - 1) // 3 + 1)

def _freq_key_fn(freq):
    return _month_key if freq == "M" else _quarter_key

def _period_keys(dates, key_fn):
    dt = pd.DatetimeIndex(dates)
    if key_fn == _month_key:
        return list(zip(dt.year, dt.month))
    else:
        return list(zip(dt.year, ((dt.month - 1) // 3 + 1)))


def quadratic_match_average(dates_low, values_low, dates_high, freq):
    """EViews quadratic-match average interpolation with mean preservation."""
    dates_low = np.asarray(pd.to_datetime(dates_low))
    values_low = np.asarray(values_low, dtype=float)
    dates_high = np.asarray(pd.to_datetime(dates_high))

    key_fn = _freq_key_fn(freq)
    obs_periods = _period_keys(dates_low, key_fn)
    valid = ~np.isnan(values_low)
    obs_vals_arr = values_low[valid]
    obs_periods_list = [p for i, p in enumerate(obs_periods) if valid[i]]

    n_obs = len(obs_vals_arr)
    if n_obs < 3:
        raise ValueError("Need at least 3 valid source observations")

    period_to_seq = {}
    for idx, p in enumerate(obs_periods_list):
        period_to_seq[p] = idx

    hf_periods = _period_keys(dates_high, key_fn)
    hf_seq_idx = np.full(len(dates_high), -1, dtype=np.int64)
    for i, p in enumerate(hf_periods):
        if p in period_to_seq:
            hf_seq_idx[i] = period_to_seq[p]

    result = np.full(len(dates_high), np.nan)

    for k in range(n_obs):
        mask = hf_seq_idx == k
        n_hf = mask.sum()
        if n_hf == 0:
            continue

        y_t = obs_vals_arr[k]

        if k == 0:
            y_prev, y_curr, y_next = obs_vals_arr[0], obs_vals_arr[1], obs_vals_arr[2]
        elif k == n_obs - 1:
            y_prev, y_curr, y_next = obs_vals_arr[-3], obs_vals_arr[-2], obs_vals_arr[-1]
        else:
            y_prev, y_curr, y_next = (
                obs_vals_arr[k - 1],
                obs_vals_arr[k],
                obs_vals_arr[k + 1],
            )

        a_coef = (y_prev - 2 * y_curr + y_next) / 2.0
        b_coef = (y_next - y_prev) / 2.0
        c_coef = y_curr

        i = np.arange(n_hf, dtype=float)
        u = (i + 0.5) / n_hf - 0.5

        f_vals = a_coef * u**2 + b_coef * u + c_coef

        mean_f = np.mean(f_vals)
        result[mask] = f_vals + (y_t - mean_f)

    return result


def _qdmatch_one(native_stem, value_col, freq):
    """Interpolate a native series to trading-day grid using qdmatch."""
    native_path = TMP_DIR / f"{native_stem}_native.csv"
    out_path = V2_DIR / f"{native_stem}_qdmatch.csv"

    native = pd.read_csv(str(native_path), parse_dates=["date"])
    native = native[native["date"] >= "1998-01-01"].copy()
    native = native.dropna(subset=[value_col])

    final = pd.read_csv("data/processed/final_dataset.csv", parse_dates=["date"])
    dates_high = final["date"].values

    values = quadratic_match_average(
        native["date"].values,
        native[value_col].values,
        dates_high,
        freq=freq,
    )

    out = pd.DataFrame({"date": dates_high, value_col: values})
    out.to_csv(str(out_path), index=False)
    return out


def build_exog(df):
    month = df["date"].dt.month
    month_dummies = pd.get_dummies(month, prefix="M", drop_first=True).astype(np.float64)
    month_dummies.index = df.index
    ones = np.ones((len(df), 1))
    time_trend = np.arange(len(df)).astype(np.float64).reshape(-1, 1)
    exog = np.column_stack([ones, time_trend, month_dummies.values])
    exog_names = ["const", "trend"] + [f"M{m}" for m in range(2, 13)]
    return exog, exog_names


def run_var(data, exog, restricted=True, k_ar=None):
    """Estimate restricted (block-exogenous) or unrestricted VAR."""
    endog = data.values
    endog_names = data.columns.tolist()
    T, K = endog.shape
    exog_a = exog if exog is not None else np.empty((T, 0))
    exog_k = exog_a.shape[1]

    k = k_ar if k_ar is not None else MAX_LAG_DAILY

    if not restricted:
        model = VAR(endog=data, exog=exog)
        return model.fit(maxlags=k, ic=None, trend="n")

    rest_idx = endog_names.index("risk_off")
    y = endog[k:]
    lagged = np.column_stack([
        endog[k - lag - 1:T - lag - 1, :]
        for lag in range(k)
    ])
    exog_eff = exog_a[k:]

    K_all_lags = K * k
    coeffs = np.zeros((K, K_all_lags + exog_k))
    resid = np.zeros((T - k, K))

    from statsmodels.regression.linear_model import OLS

    for eq in range(K):
        if eq == rest_idx:
            own_cols = [rest_idx + lag * K for lag in range(k)]
            X = np.column_stack([lagged[:, own_cols], exog_eff])
            ols_res = OLS(y[:, eq], X).fit()
            coeffs[eq, own_cols] = ols_res.params[:k]
            coeffs[eq, K_all_lags:K_all_lags + exog_k] = ols_res.params[k:]
        else:
            X = np.column_stack([lagged, exog_eff])
            ols_res = OLS(y[:, eq], X).fit()
            coeffs[eq, :X.shape[1]] = ols_res.params
        resid[:, eq] = ols_res.resid

    n_params = np.full(K, K_all_lags + exog_k)
    n_params[rest_idx] = k + exog_k
    df_vec = T - k - n_params
    sigma_u = resid.T @ resid / np.sqrt(np.outer(df_vec, df_vec))
    df_unrestricted = T - k - (K_all_lags + exog_k)

    class RestrictedVARResults:
        def __init__(self):
            self.coefs = coeffs[:, :K_all_lags].reshape(K, k, K).transpose(1, 0, 2)
            self.params = coeffs
            self.resid = resid
            self.sigma_u = sigma_u
            self.k_ar = k
            self.k_trend = 0
            self.k_exog = exog_k
            self.k_ma = 0
            self.n_totobs = T
            self.nobs = T - k
            self.df_resid = df_unrestricted
            self.df_model = K_all_lags + exog_k
            self.names = endog_names
            self.endog = endog
            self.exog = exog_eff
            self.llf = 0.0
            self.params_exog = coeffs[:, K_all_lags:] if exog_k > 0 else np.empty((K, 0))
            self.params_endog = self.coefs

        def irf(self, periods=125):
            return _compute_irf(self, periods)

        def fevd(self, periods=125):
            return _compute_fevd(self, periods)

    return RestrictedVARResults()


def _compute_irf(results, periods=125):
    K = results.coefs.shape[1]
    k_ar = results.k_ar
    irfs = np.zeros((periods + 1, K, K))
    irfs[0] = np.eye(K)
    for i in range(1, periods + 1):
        for j in range(1, min(i, k_ar) + 1):
            lag_coef = results.coefs[j - 1]
            irfs[i] += irfs[i - j] @ lag_coef
    chol = np.linalg.cholesky(results.sigma_u)
    irfs_orth = np.zeros((periods + 1, K, K))
    for i in range(periods + 1):
        irfs_orth[i] = irfs[i] @ chol

    class IRAnalysis:
        def __init__(self):
            self.irfs = irfs_orth
            self.periods = periods
            self.model = results
            self.names = results.names
            self._irf_orth = irfs_orth

    return IRAnalysis()


def _compute_fevd(results, periods=125):
    K = results.sigma_u.shape[0]
    irf_obj = results.irf(periods=periods)
    irfs = irf_obj.irfs
    msfe = np.cumsum(irfs ** 2, axis=0)
    fevd = np.zeros((irfs.shape[0], K, K))
    for i in range(irfs.shape[0]):
        total = msfe[i].sum(axis=1, keepdims=True)
        total[total == 0] = 1
        fevd[i] = msfe[i] / total

    class FEVD:
        def __init__(self):
            self.decomp = fevd
    return FEVD()


def _delta_irf_ci(irf_obj, B=1000, alpha=0.05):
    """Monte Carlo delta method for IRF confidence bands via parametric bootstrap."""
    results = irf_obj.model
    resid = results.resid
    T_eff, K = resid.shape
    k_ar = results.k_ar
    coefs = results.coefs
    is_statsmodels = type(results).__module__.startswith("statsmodels")

    if is_statsmodels:
        full_endog = results.endog
        exog_full = results.exog
        exog_k = exog_full.shape[1] if exog_full is not None else 0
        n_totobs = full_endog.shape[0]
        exog = exog_full[k_ar:] if exog_k > 0 else np.empty((T_eff, 0))
        if exog_k > 0:
            params_t = results.params.T
            exog_coef = params_t[:, K * k_ar:]
        else:
            exog_coef = np.zeros((K, 0))
    else:
        exog_raw = results.exog
        exog_k = exog_raw.shape[1] if exog_raw is not None else 0
        n_totobs = results.n_totobs if hasattr(results, "n_totobs") else (T_eff + k_ar)
        exog = exog_raw if exog_k == 0 else exog_raw
        exog_coef = results.params_exog if hasattr(results, "params_exog") else np.zeros((K, exog_k))
        full_endog = results.endog

    n_steps = irf_obj.irfs.shape[0]
    shock_idx = 0
    irf_samples = np.full((B, n_steps, K), np.nan)
    from statsmodels.regression.linear_model import OLS
    chol_sigma = np.linalg.cholesky(results.sigma_u)

    for b in range(B):
        try:
            shocks = np.random.normal(0, 1, size=(n_totobs, K)) @ chol_sigma.T
            boot_data = np.zeros((n_totobs, K))
            boot_data[:k_ar] = full_endog[:k_ar]
            for t in range(k_ar, n_totobs):
                pred = np.zeros(K)
                for lag in range(1, k_ar + 1):
                    pred += coefs[lag - 1] @ boot_data[t - lag]
                exog_idx = t - k_ar
                if exog_k > 0 and exog_idx < len(exog):
                    pred += exog_coef @ exog[exog_idx]
                boot_data[t] = pred + shocks[t]

            boot_y = boot_data[k_ar:]
            lagged = np.column_stack([
                boot_data[k_ar - lag - 1:n_totobs - lag - 1, :]
                for lag in range(k_ar)
            ])
            K_boot = boot_y.shape[1]
            boot_irf = np.zeros((n_steps, K_boot, K_boot))
            boot_irf[0] = np.eye(K_boot)
            boot_coefs = np.zeros((k_ar, K_boot, K_boot))
            for eq in range(K_boot):
                X_boot = np.column_stack([lagged, exog]) if exog_k > 0 else lagged
                ols_r = OLS(boot_y[:, eq], X_boot).fit()
                all_params = ols_r.params
                boot_coefs[:, eq, :] = all_params[:k_ar * K_boot].reshape(k_ar, K_boot)

            for i in range(n_steps):
                for j in range(1, min(i, k_ar) + 1):
                    boot_irf[i] += boot_irf[i - j] @ boot_coefs[j - 1]
            chol_s = np.linalg.cholesky(results.sigma_u)
            for i in range(n_steps):
                irf_samples[b, i, :] = (boot_irf[i] @ chol_s)[:, shock_idx]
        except Exception:
            continue

    valid = ~np.isnan(irf_samples[:, 0, 0])
    if valid.sum() < 100:
        print(f"  Warning: Only {valid.sum()} valid MC replications out of {B}.")
    lower = np.nanpercentile(irf_samples, alpha / 2 * 100, axis=0) if valid.sum() > 0 else np.zeros((n_steps, K))
    upper = np.nanpercentile(irf_samples, (1 - alpha / 2) * 100, axis=0) if valid.sum() > 0 else np.zeros((n_steps, K))
    return lower, upper


def adf_test(series, name):
    clean = series.dropna()
    if len(clean) < 10:
        return {"variable": name, "n_obs": len(clean), "adf_stat": np.nan,
                "p_value": np.nan, "critical_5pct": np.nan, "stationary": "Insufficient data"}
    try:
        result = adfuller(clean, maxlag=20, autolag="AIC")
        return {
            "variable": name, "n_obs": len(clean),
            "adf_stat": round(result[0], 4),
            "p_value": round(result[1], 4),
            "critical_5pct": round(result[4]["5%"], 4),
            "stationary": "Yes" if result[1] < ALPHA else "No",
        }
    except Exception as e:
        return {"variable": name, "n_obs": len(clean), "adf_stat": np.nan,
                "p_value": np.nan, "critical_5pct": np.nan, "stationary": f"Error: {e}"}



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
    path = V2_DIR / f"{stem}_qdmatch.csv"
    qd = pd.read_csv(str(path), parse_dates=["date"])
    return qd[["date", col_name]]


def _build_daily_paper(df_daily):
    daily = df_daily[["date", "risk_off", "spread", "log_nikkei"]].copy()
    daily = daily[daily["date"] <= PAPER_END].copy()
    qd_files = [("log_wui", "log_wui"), ("debtsec", "debtsec_pct"),
                ("equity", "equity_pct"), ("other", "other_pct"),
                ("direct", "direct_pct")]
    for stem, col in qd_files:
        qd = _load_qdmatch(stem, col)
        daily = daily.merge(qd, on="date", how="left")
    vint_rgdp = pd.read_csv(
        "data/raw/vintage/JPNRGDPEXP_vintage_2021-06-01.csv", parse_dates=["date"])
    vint_rgdp["log_rgdp_v"] = np.log(vint_rgdp["rgdp"].values)
    daily["log_rgdp"] = quadratic_match_average(
        vint_rgdp["date"].values, vint_rgdp["log_rgdp_v"].values,
        daily["date"].values, freq="Q")
    vint_reer = pd.read_csv(
        "data/raw/vintage/REER_JPN_BIS_vintage.csv", parse_dates=["date"])
    vint_reer["log_reer_v"] = np.log(vint_reer["reer"].values)
    daily["log_reer"] = quadratic_match_average(
        vint_reer["date"].values, vint_reer["log_reer_v"].values,
        daily["date"].values, freq="M")
    daily = daily.dropna().reset_index(drop=True)
    return daily


def _build_daily_extended(df_daily):
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
    np.random.seed(seed)
    dummy_irf = type("DummyIRF", (), {
        "irfs": irf_vals,
        "model": results,
        "periods": irf_vals.shape[0] - 1,
    })()
    lower, upper = _delta_irf_ci(dummy_irf, B=repl, alpha=ALPHA)
    return lower, upper


def _ci_unrestricted(results, irf_obj, repl, seed=42):
    se = np.asarray(irf_obj.stderr(orth=True))
    orth = np.asarray(irf_obj.orth_irfs)
    z = 1.96
    lower = orth - z * se
    upper = orth + z * se
    return lower[:, :, 0], upper[:, :, 0]


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
    path = TWOTIER_DIR / filename
    pd.DataFrame(rows).to_csv(str(path), index=False)
    print(f"  Saved: {path.name}")
    return path


def _print_signs(label, irf_vals, var_order, horizons):
    print(f"\n  Sign check [{label}]:")
    check_vars = ["log_rgdp", "log_reer", "spread"]
    for v in check_vars:
        vi = var_order.index(v)
        vals = [irf_vals[h, vi, 0] for h in horizons if h < irf_vals.shape[0]]
        if vals:
            print(f"    {v}: h=1={vals[0]:.6f}" if len(vals) > 0 else "")
            if len(vals) > 1:
                print(f"          h=6={vals[1]:.6f}")
            if len(vals) > 2:
                print(f"          h=12={vals[2]:.6f}")


def _estimate_monthly(data, exog, label, repl, var_order=VAR_ORDER,
                      periods=IRF_H_MONTHLY, maxlags=MAX_LAG_MONTHLY):
    lag = _select_lag_bic(data, exog, maxlags)
    print(f"\n  {label} — BIC lag: {lag}, obs: {len(data)}")

    print(f"  Estimating restricted VAR...")
    res_r, irf_r = _run_restricted_var(data, exog, lag, periods)
    print(f"  Computing restricted CIs (MC delta, B={repl})...")
    lower_r, upper_r = _ci_restricted(res_r, irf_r, repl)
    rows_r = _irf_rows(irf_r, lower_r, upper_r, var_order,
                       list(range(irf_r.shape[0])))

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

    print(f"  Estimating daily restricted VAR...")
    res_r, irf_r = _run_restricted_var(data, exog, lag, periods)

    lower_r, upper_r = None, None
    if with_ci:
        print(f"  Computing daily restricted CIs (MC delta, B={repl})...")
        lower_r, upper_r = _ci_restricted(res_r, irf_r, repl)

    rows_r = _irf_rows(irf_r, lower_r, upper_r, var_order,
                       list(range(irf_r.shape[0])))

    print(f"  Estimating daily unrestricted VAR...")
    res_u, irf_u = _run_unrestricted_var(data, exog, lag, periods)

    lower_u, upper_u = None, None
    if with_ci:
        print(f"  Computing daily unrestricted CIs (asymptotic, B={repl})...")
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


def _run_adf_and_lag(df_daily):
    """Regenerate ADF test and lag selection CSVs for both periods."""
    periods_info = [
        ("1999_2021", df_daily[df_daily["date"] <= PAPER_END]),
        ("1999_2026", df_daily),
    ]
    for period_label, period_df in periods_info:
        data = period_df[VAR_ORDER].copy().dropna()
        exog, _ = build_exog(period_df.loc[data.index])

        print(f"\n  ADF tests — {period_label.replace('_', '-')}")
        adf_results = []
        for col in VAR_ORDER:
            result = adf_test(data[col], col)
            adf_results.append(result)
        adf_df = pd.DataFrame(adf_results)
        adf_path = OUT_DIR / f"adf_tests_{period_label}.csv"
        adf_df.to_csv(str(adf_path), index=False)
        print(f"  Saved: {adf_path.name}")

        print(f"  Lag selection — {period_label.replace('_', '-')}")
        model = VAR(endog=data, exog=exog)
        lag_order = model.select_order(maxlags=MAX_LAG_DAILY, trend="n")
        aic_vals = lag_order.ics["aic"]
        lag_df = pd.DataFrame({
            "lag": range(1, min(len(aic_vals), MAX_LAG_DAILY + 1)),
            "aic": aic_vals[1:MAX_LAG_DAILY + 1],
        })
        lag_path = OUT_DIR / f"lag_selection_{period_label}.csv"
        lag_df.to_csv(str(lag_path), index=False)
        print(f"  Saved: {lag_path.name}")


def _regenerate_qdmatch():
    """Regenerate v2 quadratic-match CSVs from natives."""
    V2_DIR.mkdir(parents=True, exist_ok=True)
    for stem, col, freq in QDMATCH_SERIES:
        print(f"  QDMatch: {stem}_native.csv -> v2/{stem}_qdmatch.csv")
        _qdmatch_one(stem, col, freq)



def _verify():
    """Run the pipeline in-place and compare outputs against git-HEAD references."""
    import subprocess
    import tempfile
    from io import StringIO

    def _load_git_ref(rel_path):
        result = subprocess.run(
            ["git", "show", f"HEAD:{rel_path}"],
            capture_output=True, text=True, cwd=REPO_ROOT)
        if result.returncode != 0:
            print(f"  WARNING: cannot read git HEAD for {rel_path} — skipping")
            return None
        return pd.read_csv(StringIO(result.stdout))

    print("=" * 60)
    print("VERIFICATION: Running pipeline and comparing against committed outputs")
    print("=" * 60)

    paper_end_saved = (PAPER_END,)
    extended_end_saved = (EXTENDED_END,)

    twotier_files = [
        "daily_paper_irf.csv",
        "daily_extended_irf.csv",
        "monthly_paper_restricted_irf.csv",
        "monthly_paper_unrestricted_irf.csv",
        "monthly_extended_restricted_irf.csv",
        "monthly_extended_unrestricted_irf.csv",
        "daily_paper_unrestricted_irf.csv",
        "daily_extended_unrestricted_irf.csv",
        "comparison_paper_vs_extended.csv",
        "flow_significance.csv",
    ]
    std_files = [
        "adf_tests_1999_2021.csv",
        "adf_tests_1999_2026.csv",
        "lag_selection_1999_2021.csv",
        "lag_selection_1999_2026.csv",
    ]

    # Load references from git HEAD
    print("\n  Loading reference outputs from git HEAD...")
    refs = {}
    for fname in twotier_files:
        ref = _load_git_ref(f"data/processed/var_results/twotier/{fname}")
        if ref is not None:
            refs[fname] = ref
    for fname in std_files:
        ref = _load_git_ref(f"data/processed/var_results/{fname}")
        if ref is not None:
            refs[fname] = ref

    n_refs = len(refs)
    print(f"    Loaded {n_refs}/14 reference files")
    if n_refs < 14:
        print(f"    WARNING: {14 - n_refs} references missing — verify will be incomplete")

    # Run the pipeline in-place
    print("\n  Running pipeline...")
    _run_pipeline(with_daily_ci=False, repl=MC_REPL_DEFAULT)

    # Restore CI-column files (pipeline without --with-daily-ci omits these)
    print("\n  Restoring CI-column files from git...")
    for fname in ["daily_paper_irf.csv", "daily_extended_irf.csv",
                  "comparison_paper_vs_extended.csv"]:
        path_str = f"data/processed/var_results/twotier/{fname}"
        subprocess.run(
            ["git", "checkout", "HEAD", "--", path_str],
            capture_output=True, cwd=REPO_ROOT)
    print("    Done")

    # Compare each output against its reference
    all_ok = True
    print("\n" + 60 * "-")
    print("COMPARISON RESULTS")
    print(60 * "-")
    for fname in twotier_files:
        path = TWOTIER_DIR / fname
        if not path.exists():
            print(f"  {fname}: FAIL (output missing)")
            all_ok = False
            continue
        ref = refs.get(fname)
        if ref is None:
            print(f"  {fname}:  SKIP (no git ref)")
            continue
        new = pd.read_csv(str(path))

        shared = [c for c in ref.columns if c in new.columns]
        num_cols = [c for c in shared if pd.api.types.is_numeric_dtype(ref[c])
                    and pd.api.types.is_numeric_dtype(new[c])]
        if not num_cols:
            print(f"  {fname}:  SKIP (no shared numeric columns)")
            continue

        mcols = [c for c in ["variable", "horizon", "tier", "period", "specification"]
                 if c in ref.columns and c in new.columns]
        if mcols:
            m = ref.merge(new, on=mcols, suffixes=("_ref", "_new"), how="inner")
            max_diffs = {}
            for c in num_cols:
                rc = f"{c}_ref" if c not in mcols else c
                nc = f"{c}_new" if c not in mcols else c
                if rc not in m.columns or nc not in m.columns:
                    continue
                d = np.abs(m[rc].values.astype(float) - m[nc].values.astype(float))
                d = d[~np.isnan(d)]
                max_diffs[c] = float(np.max(d)) if len(d) > 0 else 0.0
            rvals = [np.nan_to_num(ref[c].values.astype(float)) for c in num_cols]
            nvals = [np.nan_to_num(new[c].values.astype(float)) for c in num_cols]
            ok = all(np.allclose(r, n, rtol=1e-6, atol=1e-12)
                     for r, n in zip(rvals, nvals))
            label = "PASS" if ok else "FAIL"
            fmt = {k: f"{v:.2e}" for k, v in max_diffs.items()}
            print(f"  {fname}: {label} (max diffs: {fmt})")
            if not ok:
                all_ok = False
        else:
            rvals = [np.nan_to_num(ref[c].values.astype(float)) for c in num_cols]
            nvals = [np.nan_to_num(new[c].values.astype(float)) for c in num_cols]
            ok = all(np.allclose(r, n, rtol=1e-6, atol=1e-12)
                     for r, n in zip(rvals, nvals))
            print(f"  {fname}: {'PASS' if ok else 'FAIL'}")
            if not ok:
                all_ok = False

    for fname in std_files:
        path = OUT_DIR / fname
        if not path.exists():
            print(f"  {fname}: FAIL (output missing)")
            all_ok = False
            continue
        ref = refs.get(fname)
        if ref is None:
            print(f"  {fname}:  SKIP (no git ref)")
            continue
        new = pd.read_csv(str(path))
        num_cols = [c for c in ref.columns if c in new.columns
                    and pd.api.types.is_numeric_dtype(ref[c])
                    and pd.api.types.is_numeric_dtype(new[c])]
        if not num_cols:
            print(f"  {fname}:  SKIP (no shared numeric columns)")
            continue
        ok = all(np.allclose(
            np.nan_to_num(ref[c].values.astype(float)),
            np.nan_to_num(new[c].values.astype(float)),
            rtol=1e-6, atol=1e-12) for c in num_cols)
        print(f"  {fname}: {'PASS' if ok else 'FAIL'}")
        if not ok:
            all_ok = False



    print()
    if all_ok:
        print("VERDICT: ALL CHECKS PASSED")
    else:
        print("VERDICT: SOME CHECKS FAILED — investigate discrepancies above")
    return all_ok


# --- figure functions ---


VAR_LABELS = {
    "risk_off": "RISK", "log_wui": "LOG(WUI_JP)", "spread": "SPREAD_JP",
    "log_rgdp": "LOG(RGDP_JP)", "log_reer": "LOG(REER_JP)",
    "log_nikkei": "LOG(STOCK_IDX_JP)", "debtsec_pct": "DEBTSEC_JP",
    "equity_pct": "EQUITY_JP", "other_pct": "OTHER_JP", "direct_pct": "DIRECT_JP",
}


def _plot_panel(ax, df, variable, color, x_max):
    sub = df[df["variable"] == variable].sort_values("horizon")
    has_ci = "lower" in sub.columns and "upper" in sub.columns
    if has_ci:
        ax.fill_between(sub["horizon"], sub["lower"], sub["upper"],
                         color=color, alpha=0.15)
    ax.plot(sub["horizon"], sub["response"], color=color, linewidth=0.8)
    ax.axhline(0, color=ZERO_COLOR, linewidth=0.4, linestyle="--")
    ax.set_title(VAR_LABELS.get(variable, variable), fontsize=8)
    ax.set_xlim(0, x_max)
    ax.set_xlabel("")
    ax.tick_params(labelbottom=False)


def _grid(csv_path, out_name, title, color):
    df = pd.read_csv(csv_path)
    x_max = df["horizon"].max()
    x_ticks = list(range(0, int(x_max) + 1, 25)) if x_max > 60 else list(range(0, int(x_max) + 1, 5))
    last_ax_idx = None
    fig, axes = plt.subplots(5, 2, figsize=(10, 12))
    for idx, var in enumerate(VAR_ORDER):
        ax = axes.flat[idx]
        _plot_panel(ax, df, var, color, x_max)
        last_ax_idx = idx
    for idx in range(len(VAR_ORDER), 10):
        axes.flat[idx].set_visible(False)
    axes.flat[last_ax_idx].set_xlabel("Horizon")
    axes.flat[last_ax_idx].tick_params(labelbottom=True)
    axes.flat[last_ax_idx].set_xticks(x_ticks)
    axes.flat[last_ax_idx - 1].set_xlabel("Horizon")
    axes.flat[last_ax_idx - 1].tick_params(labelbottom=True)
    axes.flat[last_ax_idx - 1].set_xticks(x_ticks)
    fig.suptitle(title, fontsize=12, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(FIG_DIR / out_name, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_name}")


def run_figures():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({
        "axes.grid": True,
        "grid.color": "#F2F2F2",
        "grid.linewidth": 0.3,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.spines.bottom": True,
        "axes.titleweight": "bold",
        "axes.titlesize": 9,
        "axes.labelsize": 8,
        "axes.labelcolor": "#595959",
        "xtick.major.size": 0,
        "ytick.major.size": 0,
        "xtick.color": "#595959",
        "ytick.color": "#595959",
        "text.color": "#0D0D0D",
        "legend.fontsize": 7,
        "legend.frameon": False,
        "figure.facecolor": "#F5F4EF",
        "axes.facecolor": "#F5F4EF",
    })

    grids = [
        (TWOTIER_DIR / "daily_paper_irf.csv",
         "irf_grid_daily_restricted_paper.png",
         "Figure A3.1, Real and Financial Spillovers in Japan (Restricted), 1999-2021", PAPER_COLOR),
        (TWOTIER_DIR / "daily_paper_unrestricted_irf.csv",
         "irf_grid_daily_unrestricted_paper.png",
         "Figure A2.1, Real and Financial Spillovers in Japan (Unrestricted), 1999-2021", PAPER_COLOR),
        (TWOTIER_DIR / "monthly_paper_restricted_irf.csv",
         "irf_grid_monthly_restricted_paper.png",
         "Figure A4, Real and Financial Spillovers in Japan, Monthly (Restricted), 1999-2021", PAPER_COLOR),
        (TWOTIER_DIR / "monthly_paper_unrestricted_irf.csv",
         "irf_grid_monthly_unrestricted_paper.png",
         "Figure A4, Real and Financial Spillovers in Japan, Monthly (Unrestricted), 1999-2021", PAPER_COLOR),
        (TWOTIER_DIR / "daily_extended_irf.csv",
         "irf_grid_daily_restricted_extended.png",
         "Real and Financial Spillovers in Japan (Restricted), 1999-2026", EXT_COLOR),
        (TWOTIER_DIR / "daily_extended_unrestricted_irf.csv",
         "irf_grid_daily_unrestricted_extended.png",
         "Real and Financial Spillovers in Japan (Unrestricted), 1999-2026", EXT_COLOR),
        (TWOTIER_DIR / "monthly_extended_restricted_irf.csv",
         "irf_grid_monthly_restricted_extended.png",
         "Real and Financial Spillovers in Japan, Monthly (Restricted), 1999-2026", EXT_COLOR),
        (TWOTIER_DIR / "monthly_extended_unrestricted_irf.csv",
         "irf_grid_monthly_unrestricted_extended.png",
         "Real and Financial Spillovers in Japan, Monthly (Unrestricted), 1999-2026", EXT_COLOR),
    ]
    for csv_path, out_name, title, color in grids:
        _grid(csv_path, out_name, title, color)
def main():
    parser = argparse.ArgumentParser(description="Unified SVAR replication")
    parser.add_argument("--interpolate-v1", action="store_true",
                        help="Regenerate v1 daily CSVs from natives (pandas spline)")
    parser.add_argument("--with-daily-ci", action="store_true",
                        help="Compute daily restricted CIs")
    parser.add_argument("--repl", type=int, default=MC_REPL_DEFAULT,
                        help=f"MC bootstrap replications (default: {MC_REPL_DEFAULT})")
    parser.add_argument("--verify", action="store_true",
                        help="Compare outputs against committed reference CSVs")
    parser.add_argument("--figures", action="store_true",
                        help="Render IRF figures from committed CSVs")
    parser.add_argument("--fetch-vintage-gdp", action="store_true",
                        help="Download ALFRED JPNRGDPEXP vintage CSV if missing (requires internet)")
    parser.add_argument("--fetch-vintage-reer", action="store_true",
                        help="Download Wayback BIS REER vintage CSV if missing (requires internet)")
    args = parser.parse_args()

    if args.interpolate_v1:
        print(60 * "=")
        print("Mode: v1 daily interpolation only")
        print(60 * "=")
        run_interpolate_v1()
        return

    if args.verify:
        _verify()
        return

    if args.fetch_vintage_gdp:
        fetch_vintage_gdp()
        return

    if args.fetch_vintage_reer:
        fetch_vintage_reer()
        return

    if args.figures:
        run_figures()
        return

    print(60 * "=")
    print("Unified SVAR Replication")
    print(60 * "=")
    print(f"Paper period:  {PAPER_END.date()}")
    print(f"Extended end:  {EXTENDED_END.date()}")
    print(f"Daily IRF:     {IRF_H_DAILY} days (restricted)")
    print(f"Monthly IRF:   {IRF_H_MONTHLY} months (restricted + unrestricted)")
    print(f"MC repl:       {args.repl}")
    print(f"Daily CIs:     {'YES' if args.with_daily_ci else 'point estimates only'}")

    _run_pipeline(with_daily_ci=args.with_daily_ci, repl=args.repl)


# Vintage data fetch (inlined from fetch_alfred_vintage.py)

ALFRED_API_BASE = "https://fred.stlouisfed.org/graph/api"
ALFRED_SERIES_ID = "JPNRGDPEXP"
ALFRED_VINTAGES = ["2021-06-01"]
ALFRED_OUTPUT_DIR = REPO_ROOT / "data" / "raw" / "vintage"


def _alfred_filter_notes(obj):
    if isinstance(obj, dict):
        return {k: _alfred_filter_notes(v) for k, v in obj.items() if k != "notes"}
    if isinstance(obj, list):
        return [_alfred_filter_notes(v) for v in obj]
    return obj


def _alfred_decompress(data):
    if data[:2] == b"\x1f\x8b":
        return gzip.decompress(data)
    return data


def _alfred_fetch_payload(series_id, mode, vintage_date=None):
    url = f"{ALFRED_API_BASE}/series/?id={series_id}&width=800&mode={mode}"
    if vintage_date:
        url += f"&vintage_date={vintage_date}"
    req = urllib.request.Request(url, headers={
        "Accept-Encoding": "gzip, deflate",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        parsed = json.loads(_alfred_decompress(resp.read()))
    chart_state = {
        "chart": parsed["chart"],
        "seriesObjects": parsed["chart_series"],
    }
    return _alfred_filter_notes(chart_state)


def _alfred_fetch_observations(series_id, chart_state):
    body = json.dumps(chart_state, separators=(",", ":"))
    url = f"{ALFRED_API_BASE}/series/?obs=true&sid={series_id}"
    req = urllib.request.Request(
        url, data=body.encode("utf-8"), headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
        }, method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        parsed = json.loads(_alfred_decompress(resp.read()))
    obs_groups = parsed.get("observations", [])
    if not obs_groups:
        return {}
    result = {}
    for ts_ms, val in obs_groups[0]:
        dt = datetime.datetime.fromtimestamp(ts_ms / 1000, datetime.UTC)
        result[dt.strftime("%Y-%m-%d")] = val
    return result


def _alfred_fetch_vintage(series_id, vintage_date):
    state = _alfred_fetch_payload(series_id, "alfred", vintage_date)
    return _alfred_fetch_observations(series_id, state)


def _alfred_save_csv(filepath, observations):
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "rgdp"])
        for d in sorted(observations.keys()):
            writer.writerow([d, observations[d]])


def fetch_vintage_gdp():
    """Fetch ALFRED vintage JPNRGDPEXP if the CSV does not exist."""
    for vintage in ALFRED_VINTAGES:
        out_path = ALFRED_OUTPUT_DIR / f"{ALFRED_SERIES_ID}_vintage_{vintage}.csv"
        if out_path.exists():
            print(f"  {out_path.name} already exists — skipping")
            continue
        print(f"  Fetching {ALFRED_SERIES_ID} as of {vintage} ...", end=" ", flush=True)
        try:
            obs = _alfred_fetch_vintage(ALFRED_SERIES_ID, vintage)
            if not obs:
                print("FAILED: no observations returned")
                continue
            _alfred_save_csv(str(out_path), obs)
            dates = sorted(obs.keys())
            print(f"OK — {len(obs)} obs, {dates[0]} to {dates[-1]}")
        except urllib.error.HTTPError as e:
            print(f"HTTP {e.code}: {e.reason}")
            print(f"  Manual download: https://alfred.stlouisfed.org/series?seid={ALFRED_SERIES_ID}")
        except Exception as e:
            print(f"ERROR: {e}")


# BIS REER vintage fetch (inlined from fetch_reer_vintage.py)

REER_SNAPSHOT_URL = (
    "https://web.archive.org/web/20210524235626id_/"
    "https://www.bis.org/statistics/eer/broad.xlsx"
)
REER_JAPAN_COL = 31
REER_OUTPUT_DIR = REPO_ROOT / "data" / "raw" / "vintage"
REER_OUTPUT_FILE = REER_OUTPUT_DIR / "REER_JPN_BIS_vintage.csv"


def _reer_fetch_broad_xlsx(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def _reer_extract_japan(data):
    tmp = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
    try:
        tmp.write(data)
        tmp.close()
        df = pd.read_excel(tmp.name, sheet_name="Real", header=None)
    finally:
        os.unlink(tmp.name)
    dates_raw = df.iloc[5:, 0].values
    rbjp_raw = df.iloc[5:, REER_JAPAN_COL].values
    dates = pd.to_datetime([str(d)[:10] for d in dates_raw])
    vals = pd.to_numeric(rbjp_raw, errors="coerce")
    dates = dates.to_period("M").to_timestamp()
    result = pd.DataFrame({"date": dates, "reer": vals})
    result = result.dropna(subset=["reer"]).reset_index(drop=True)
    result["date"] = result["date"].dt.strftime("%Y-%m-%d")
    return result


def _reer_verify(result, source_data):
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
    if source_data is not None:
        vintage_s = result.set_index("date")["reer"]
        cur_s = source_data.set_index("date")["reer"]
        both = pd.DataFrame({"v": vintage_s, "c": cur_s}).dropna()
        both = both.loc["2015-01-01":"2021-03-01"]
        pct = np.abs(both["v"].astype(float) - both["c"].astype(float)) / both["c"].astype(float) * 100
        info["mean_abs_pct_diff_vs_current"] = round(pct.mean(), 4)
        info["max_abs_pct_diff_vs_current"] = round(pct.max(), 4)
    return info


def fetch_vintage_reer():
    """Fetch 2021-vintage BIS REER from Wayback Machine if the CSV does not exist."""
    if REER_OUTPUT_FILE.exists():
        print(f"  {REER_OUTPUT_FILE.name} already exists — skipping")
        return
    print(f"  Fetching from Wayback Machine...", end=" ", flush=True)
    try:
        xlsx_data = _reer_fetch_broad_xlsx(REER_SNAPSHOT_URL)
        print(f"downloaded {len(xlsx_data)} bytes")
        result = _reer_extract_japan(xlsx_data)
        print(f"  Extracted {len(result)} months of Japan real broad REER")

        current = None
        current_path = REPO_ROOT / "data" / "raw" / "REER.xlsx"
        if current_path.exists():
            try:
                cur = pd.read_excel(current_path, sheet_name="Table Data")
                cur["date"] = pd.to_datetime(cur["Date"]).dt.strftime("%Y-%m-%d")
                cur["reer"] = pd.to_numeric(cur.iloc[:, 1], errors="coerce")
                current = cur[["date", "reer"]].dropna()
            except Exception:
                pass

        info = _reer_verify(result, current)
        print(f"  Provenance:")
        print(f"    Source: {REER_SNAPSHOT_URL}")
        print(f"    Base year: {info['base_year']} (2010 mean = {info['2010_mean']})")
        print(f"    Coverage: {info['date_min']} to {info['date_max']} ({info['n_obs']} months)")
        if "mean_abs_pct_diff_vs_current" in info:
            print(f"    Mean abs % diff vs REER.xlsx (2015-2021): {info['mean_abs_pct_diff_vs_current']}%")

        REER_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        result.to_csv(REER_OUTPUT_FILE, index=False)
        print(f"  Wrote {REER_OUTPUT_FILE}")
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}")
        print(f"  Manual download: https://www.bis.org/statistics/eer/broad.xlsx")
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
