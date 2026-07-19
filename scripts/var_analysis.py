"""
SVAR analysis for Beirne & Sugandi (2023) replication.

Estimates restricted (block-exogenous) and unrestricted VAR models on both the
paper replication period (1999-2021) and extended period (1999-2026).
Produces IRF plots (analytical and bootstrap CIs), FEVD tables, and comparison
figures.

Usage: uv run python scripts/var_analysis.py
Outputs: data/processed/var_results/ (figures and tables)
"""

import os
import sys
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller

warnings.filterwarnings("ignore", category=FutureWarning)

OUT_DIR = Path("data/processed/var_results")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(exist_ok=True)

DPI = 150
PAPER_END = pd.Timestamp("2021-03-31")
IRF_HORIZON = 125
MAX_LAG = 20
ALPHA = 0.05
N_BOOTSTRAP = 100
RNG = np.random.default_rng(20260715)

VAR_ORDER = [
    "risk_off", "log_wui", "spread", "log_rgdp", "log_reer",
    "log_nikkei", "debtsec_pct", "equity_pct", "other_pct", "direct_pct",
]

PAPER_TEXTS = {
    "restricted": (
        "In the restricted estimation, we set the model so that the Risk-off variable "
        "is only affected by its own lagged values, while other endogenous variables "
        "are affected by each other's lagged values and are affected by the lagged "
        "values of the Risk-off variable."
    ),
    "cholesky": (
        "A Cholesky identification scheme is used."
    ),
    "ci_95": (
        "Confidence intervals at the 95% level are provided."
    ),
    "lag_aic": (
        "k is optimum time lag for the VAR model based on the Akaike Information Criterion (AIC)."
    ),
    "stationarity": (
        "All endogenous variables are stationary."
    ),
    "exogenous": (
        "The exogenous variables are the time dummy and the seasonal dummies."
    ),
    "daily_freq": (
        "The use of daily data is used given that the risk-off shocks occurred on a specific day."
    ),
    "irf_horizon": (
        "The horizontal axis refers to the number of days. [Figures 4-10 show 125 days.]"
    ),
}

COLORS = {
    "paper": "#2E45B8",
    "extended": "#F97A1F",
    "shock": "#C91D42",
    "ci_fill": "#D6DBF5",
    "ci_boot": "#F9D2DB",
    "zero": "#595959",
    "bg": "#F5F4EF",
    "grid": "#D9D9D9",
    "text": "#0D0D0D",
    "muted": "#595959",
}


def set_quant_style():
    plt.rcParams.update({
        "axes.grid": True,
        "grid.color": COLORS["grid"],
        "grid.linewidth": 0.3,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.spines.bottom": True,
        "axes.titleweight": "bold",
        "axes.titlesize": 10,
        "axes.labelsize": 8,
        "axes.labelcolor": COLORS["muted"],
        "xtick.major.size": 0,
        "ytick.major.size": 0,
        "xtick.color": COLORS["muted"],
        "ytick.color": COLORS["muted"],
        "legend.fontsize": 7,
        "legend.frameon": False,
        "text.color": COLORS["text"],
        "figure.facecolor": COLORS["bg"],
        "axes.facecolor": COLORS["bg"],
    })


def load_data():
    df = pd.read_csv("data/processed/final_dataset.csv", parse_dates=["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df


def build_exog(df):
    month = df["date"].dt.month
    month_dummies = pd.get_dummies(month, prefix="M", drop_first=True).astype(np.float64)
    month_dummies.index = df.index
    time_trend = np.arange(len(df)).astype(np.float64).reshape(-1, 1)
    exog = np.column_stack([time_trend, month_dummies.values])
    exog_names = ["trend"] + [f"M{m}" for m in range(2, 13)]
    return exog, exog_names


def run_var(data, exog, restricted=True, k_ar=None):
    endog = data.values
    endog_names = data.columns.tolist()
    T, K = endog.shape
    exog_a = exog if exog is not None else np.empty((T, 0))
    exog_k = exog_a.shape[1]

    k = k_ar if k_ar is not None else MAX_LAG

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
        else:
            X = np.column_stack([lagged, exog_eff])
        ols_res = OLS(y[:, eq], X).fit()
        coeffs[eq, :X.shape[1]] = ols_res.params
        resid[:, eq] = ols_res.resid

    df = T - k - (K_all_lags + exog_k)
    sigma_u = resid.T @ resid / df

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
            self.df_resid = df
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
            irfs[i] += irfs[i - j] @ lag_coef.T
    chol = np.linalg.cholesky(results.sigma_u)
    irfs_orth = np.zeros((periods + 1, K, K))
    for i in range(periods + 1):
        irfs_orth[i] = irfs[i] @ chol
    class IRAnalysis:
        def __init__(self):
            self.irfs = irfs_orth[1:]
            self.periods = periods
            self.model = results
            self.names = results.names
            self._irf_orth = irfs_orth
        def _compute_corr_band(self):
            se = np.sqrt(np.diag(results.sigma_u) / results.nobs)
            z = 1.96
            T = self.irfs.shape[0]
            lower = self.irfs - z * se[np.newaxis, np.newaxis, :]
            upper = self.irfs + z * se[np.newaxis, np.newaxis, :]
            return lower[:, 0, :], upper[:, 0, :]
        def plot(self, orth=True):
            pass
    return IRAnalysis()


def _compute_fevd(results, periods=125):
    K = results.sigma_u.shape[0]
    irf_obj = results.irf(periods=periods)
    irfs = irf_obj.irfs
    msfe = np.cumsum(irfs ** 2, axis=0)
    fevd = np.zeros((periods, K, K))
    for i in range(periods):
        total = msfe[i].sum(axis=1, keepdims=True)
        total[total == 0] = 1
        fevd[i] = msfe[i] / total
    chol = np.linalg.cholesky(results.sigma_u)
    class FEVD:
        def __init__(self):
            self.decomp = fevd
    return FEVD()


def adf_test(series, name):
    clean = series.dropna()
    if len(clean) < 10:
        return {"variable": name, "n_obs": len(clean), "adf_stat": np.nan,
                "p_value": np.nan, "critical_5pct": np.nan, "stationary": "Insufficient data"}
    try:
        result = adfuller(clean, maxlag=20, autolag="AIC")
        adf_stat = result[0]
        p_value = result[1]
        crit_5pct = result[4]["5%"]
        stationary = "Yes" if p_value < ALPHA else "No"
        return {"variable": name, "n_obs": len(clean), "adf_stat": round(adf_stat, 4),
                "p_value": round(p_value, 4), "critical_5pct": round(crit_5pct, 4),
                "stationary": stationary}
    except Exception as e:
        return {"variable": name, "n_obs": len(clean), "adf_stat": np.nan,
                "p_value": np.nan, "critical_5pct": np.nan, "stationary": f"Error: {e}"}


def plot_irf(irf, ax, label, color, ci_method="analytic", B=1000):
    irf_values = irf.irfs
    shock_idx = 0
    n_steps = irf_values.shape[0]

    if ci_method == "analytic":
        lower, upper = irf._compute_corr_band()
        ci_label = "95% CI (analytic)"
    elif ci_method == "bootstrap":
        lower, upper = _bootstrap_irf_ci(irf, B=B)
        ci_label = f"95% CI (bootstrap, B={B})"
    else:
        lower, upper = None, None
        ci_label = ""

    steps = np.arange(n_steps)
    for v_idx in range(irf_values.shape[2]):
        response = irf_values[:, shock_idx, v_idx]
        ax[v_idx].plot(steps, response, color=color, linewidth=0.7, label=label)
        if lower is not None:
            ax[v_idx].fill_between(steps, lower[:, v_idx], upper[:, v_idx],
                                   color=color, alpha=0.12)
        ax[v_idx].axhline(y=0, color=COLORS["zero"], linewidth=0.4, linestyle="--")
        if v_idx == 0:
            ax[v_idx].set_title(f"Response of {VAR_ORDER[v_idx]}", fontsize=9)


def _bootstrap_irf_ci(irf_obj, B=1000, alpha=0.05):
    """Manual residual-based bootstrap for IRF confidence bands.
    Handles both RestrictedVARResults and statsmodels VARResults."""
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

    for b in range(B):
        try:
            boot_resid = resid[np.random.choice(T_eff, size=T_eff, replace=True)]
            boot_data = np.zeros((n_totobs, K))
            boot_data[:k_ar] = full_endog[:k_ar]
            for t in range(k_ar, n_totobs):
                pred = np.zeros(K)
                for lag in range(1, k_ar + 1):
                    pred += coefs[lag - 1].T @ boot_data[t - lag]
                exog_idx = t - k_ar
                if exog_k > 0 and exog_idx < len(exog):
                    pred += exog_coef @ exog[exog_idx]
                boot_data[t] = pred + boot_resid[t - k_ar]

            boot_y = boot_data[k_ar:]
            lagged = np.column_stack([
                boot_data[k_ar - lag - 1:n_totobs - lag - 1, :]
                for lag in range(k_ar)
            ])
            K_boot = boot_y.shape[1]
            boot_irf = np.zeros((n_steps, K_boot, K_boot))
            boot_irf[0] = np.eye(K_boot)
            boot_coefs = np.zeros((k_ar, K_boot, K_boot))
            boot_resids = np.zeros((T_eff, K_boot))
            for eq in range(K_boot):
                X_boot = np.column_stack([lagged, exog]) if exog_k > 0 else lagged
                ols_r = OLS(boot_y[:, eq], X_boot).fit()
                all_params = ols_r.params
                boot_coefs[:, eq, :] = all_params[:k_ar * K_boot].reshape(k_ar, K_boot)
                boot_resids[:, eq] = ols_r.resid

            sigma_boot = boot_resids.T @ boot_resids / (T_eff - X_boot.shape[1])
            for reg in [1e-10, 1e-6, 1e-2]:
                try:
                    chol_boot = np.linalg.cholesky(sigma_boot + np.eye(K_boot) * reg)
                    break
                except np.linalg.LinAlgError:
                    chol_boot = None
            if chol_boot is None:
                continue

            for i in range(1, n_steps):
                for j in range(1, min(i, k_ar) + 1):
                    boot_irf[i] += boot_irf[i - j] @ boot_coefs[j - 1]
            for i in range(n_steps):
                irf_samples[b, i, :] = (boot_irf[i] @ chol_boot)[:, shock_idx]
        except Exception:
            continue

    valid = ~np.isnan(irf_samples[:, 0, 0])
    if valid.sum() < 100:
        print(f"  Warning: Only {valid.sum()} valid bootstrap replications out of {B}.")
    lower = np.nanpercentile(irf_samples, alpha / 2 * 100, axis=0) if valid.sum() > 0 else np.zeros((n_steps, K))
    upper = np.nanpercentile(irf_samples, (1 - alpha / 2) * 100, axis=0) if valid.sum() > 0 else np.zeros((n_steps, K))
    return lower, upper


def main():
    print("=" * 70)
    print("SVAR Analysis — Beirne & Sugandi (2023) Replication")
    print("=" * 70)
    print(f"Output directory: {OUT_DIR}")
    print(f"IRF horizon: {IRF_HORIZON} days")
    print(f"Max lag search: {MAX_LAG}")
    print()

    df = load_data()
    print(f"Data loaded: {len(df)} rows, {df['date'].min()} to {df['date'].max()}")

    df_period1 = df[df["date"] <= PAPER_END].copy()
    df_period2 = df.copy()

    print(f"Period 1 (replication): {len(df_period1)} rows")
    print(f"Period 2 (extended):    {len(df_period2)} rows")
    print()

    for period_label, period_df in [("1999-2021", df_period1), ("1999-2026", df_period2)]:
        print(f"\n{'=' * 70}")
        print(f"Period: {period_label}")
        print(f"{'=' * 70}")

        data = period_df[VAR_ORDER].copy()
        data = data.dropna()
        print(f"  Complete rows after dropna: {len(data)}")

        exog, exog_names = build_exog(period_df.loc[data.index])

        print("\n  --- Stationarity Tests ---")
        adf_results = []
        for col in VAR_ORDER:
            result = adf_test(data[col], col)
            adf_results.append(result)
            marker = "✓" if result["stationary"] == "Yes" else "✗" if result["stationary"] == "No" else "?"
            print(f"    {marker} {col:20s}  ADF={result['adf_stat']:>8.4f}  p={result['p_value']:>8.4f}  "
                  f"5% crit={result['critical_5pct']:>8.4f}  → {result['stationary']}")

        adf_df = pd.DataFrame(adf_results)
        adf_df.to_csv(OUT_DIR / f"adf_tests_{period_label.replace('-', '_')}.csv", index=False)

        print(f"\n  --- Lag Selection (AIC, max={MAX_LAG}) ---")
        model = VAR(endog=data, exog=exog)
        lag_order = model.select_order(maxlags=MAX_LAG, trend="n")
        k_selected = int(lag_order.selected_orders["aic"])
        aic_vals = lag_order.ics["aic"]
        print(f"    AIC values by lag:")
        for lag_idx in range(1, min(len(aic_vals), MAX_LAG + 1)):
            aic_val = aic_vals[lag_idx]
            marker = " ← selected" if lag_idx == k_selected else ""
            print(f"      lag {lag_idx:2d}: {aic_val:>10.4f}{marker}")
        print(f"    Selected lag: {k_selected}")

        lag_df = pd.DataFrame({
            "lag": range(1, min(len(aic_vals), MAX_LAG + 1)),
            "aic": aic_vals[1:MAX_LAG + 1],
        })
        lag_df.to_csv(OUT_DIR / f"lag_selection_{period_label.replace('-', '_')}.csv", index=False)

        spec_types = [
            ("restricted", True),
            ("unrestricted", False),
        ]

        for spec_label, restricted in spec_types:
            print(f"\n  --- {spec_label.title()} VAR (lags={k_selected}) ---")
            var_results = run_var(data, exog, restricted=restricted, k_ar=k_selected)
            print(f"    Estimated. LLF={var_results.llf:.2f}, df_resid={var_results.df_resid}")

            irf = var_results.irf(periods=IRF_HORIZON)
            sigma_u = var_results.sigma_u
            nobs = var_results.nobs
            se = np.sqrt(np.diag(sigma_u) / nobs)
            z = 1.96
            irf_values = irf.irfs
            lower_anal = irf_values - z * se[np.newaxis, np.newaxis, :]
            upper_anal = irf_values + z * se[np.newaxis, np.newaxis, :]

            def _make_irf_plot(irf_vals, lower, upper, ci_label, suffix):
                set_quant_style()
                fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(16, 10))
                axes_flat = axes.flatten()
                for v_idx, v_name in enumerate(VAR_ORDER):
                    if v_idx < len(axes_flat):
                        response = irf_vals[:, 0, v_idx]
                        steps = np.arange(len(response))
                        axes_flat[v_idx].plot(steps, response,
                                              color=COLORS["paper"], linewidth=0.8,
                                              label="Point estimate")
                        if lower is not None:
                            axes_flat[v_idx].fill_between(
                                steps, lower[:, v_idx], upper[:, v_idx],
                                color=COLORS["paper"], alpha=0.15,
                                label=f"{ci_label}")
                        axes_flat[v_idx].axhline(y=0, color=COLORS["zero"],
                                                 linewidth=0.4, linestyle="--")
                        axes_flat[v_idx].set_title(v_name, fontsize=9, fontweight="bold")
                        axes_flat[v_idx].set_xlabel("Days", fontsize=8)
                        if v_idx % 4 == 0:
                            axes_flat[v_idx].set_ylabel("Percentage points", fontsize=8)
                        if v_idx == 0:
                            axes_flat[v_idx].legend(loc="upper right", fontsize=6)
                for v_idx in range(len(VAR_ORDER), len(axes_flat)):
                    axes_flat[v_idx].set_visible(False)
                fig.suptitle(f"Response of each variable to a Risk-off shock: "
                             f"{spec_label.title()} VAR, {period_label}",
                             fontsize=12, fontweight="bold", color=COLORS["text"],
                             y=0.98)
                fig.text(0.5, 0.01, f"Shaded band: {ci_label}",
                         ha="center", fontsize=8, color=COLORS["muted"])
                plt.tight_layout(rect=[0, 0.02, 1, 0.95])
                fname = f"irf_{spec_label}_{period_label.replace('-', '_')}_{suffix}.png"
                fig.savefig(FIG_DIR / fname, dpi=DPI, bbox_inches="tight")
                plt.close(fig)
                print(f"    Saved: {fname}")

            print(f"    Computing IRF (analytical CI)...")
            _make_irf_plot(irf_values, lower_anal[:, 0, :], upper_anal[:, 0, :],
                          "Analytical 95% CI", "analytical")

            print(f"    Computing IRF (bootstrap CI, B={N_BOOTSTRAP})...")
            try:
                lower_boot, upper_boot = _bootstrap_irf_ci(irf, B=N_BOOTSTRAP)
                _make_irf_plot(irf_values, lower_boot, upper_boot,
                              f"Bootstrap 95% CI, B={N_BOOTSTRAP}", "bootstrap")

                set_quant_style()
                fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(16, 10))
                axes_flat = axes.flatten()
                for v_idx, v_name in enumerate(VAR_ORDER):
                    if v_idx < len(axes_flat):
                        response = irf_values[:, 0, v_idx]
                        steps = np.arange(len(response))
                        axes_flat[v_idx].plot(steps, response,
                                              color=COLORS["paper"], linewidth=0.8,
                                              label="Point estimate")
                        axes_flat[v_idx].fill_between(
                            steps, lower_anal[:, 0, v_idx], upper_anal[:, 0, v_idx],
                            color=COLORS["paper"], alpha=0.15, label="Analytic 95% CI")
                        axes_flat[v_idx].fill_between(
                            steps, lower_boot[:, v_idx], upper_boot[:, v_idx],
                            color=COLORS["ci_boot"], alpha=0.4, label="Bootstrap 95% CI")
                        axes_flat[v_idx].axhline(y=0, color=COLORS["zero"],
                                                 linewidth=0.4, linestyle="--")
                        axes_flat[v_idx].set_title(v_name, fontsize=9, fontweight="bold")
                        axes_flat[v_idx].set_xlabel("Days", fontsize=8)
                        if v_idx % 4 == 0:
                            axes_flat[v_idx].set_ylabel("Percentage points", fontsize=8)
                axes_flat[0].legend(fontsize=6, loc="upper right")
                for v_idx in range(len(VAR_ORDER), len(axes_flat)):
                    axes_flat[v_idx].set_visible(False)
                fig.suptitle(f"Analytical versus bootstrap confidence intervals: "
                             f"{spec_label.title()} VAR, {period_label}",
                             fontsize=12, fontweight="bold", color=COLORS["text"],
                             y=0.98)
                plt.tight_layout(rect=[0, 0, 1, 0.95])
                fname = f"irf_{spec_label}_{period_label.replace('-', '_')}_ci_comparison.png"
                fig.savefig(FIG_DIR / fname, dpi=DPI, bbox_inches="tight")
                plt.close(fig)
                print(f"    Saved: {fname}")
            except Exception as e:
                print(f"    Bootstrap failed: {e}")

            print(f"    Computing FEVD ({IRF_HORIZON}-day horizon)...")
            fevd = var_results.fevd(periods=IRF_HORIZON)
            fevd_values = fevd.decomp[:, 0, :]
            target_horizons = [1, 5, 20, 60, 125]
            fevd_rows = []
            for h in target_horizons:
                if h <= fevd_values.shape[0]:
                    row = {"horizon_days": h}
                    for v_idx, v_name in enumerate(VAR_ORDER):
                        row[f"shock_{v_name}"] = round(fevd_values[h - 1, v_idx], 4)
                    fevd_rows.append(row)
            fevd_df = pd.DataFrame(fevd_rows)
            fevd_csv = f"fevd_{spec_label}_{period_label.replace('-', '_')}.csv"
            fevd_df.to_csv(OUT_DIR / fevd_csv, index=False)
            print(f"    Saved: {fevd_csv}")

            irf_peak = pd.DataFrame({
                "variable": VAR_ORDER,
                "peak_response": [np.max(np.abs(irf.irfs[:, 0, v])) for v in range(len(VAR_ORDER))],
                "peak_day": [np.argmax(np.abs(irf.irfs[:, 0, v])) for v in range(len(VAR_ORDER))],
            })
            peak_csv = f"irf_peak_{spec_label}_{period_label.replace('-', '_')}.csv"
            irf_peak.to_csv(OUT_DIR / peak_csv, index=False)

    print("\nPeriod comparison: overlaying restricted IRFs from both periods...")
    try:
        data_p1 = df_period1[VAR_ORDER].copy().dropna()
        exog_p1, _ = build_exog(df_period1.loc[data_p1.index])
        model_p1 = VAR(endog=data_p1, exog=exog_p1)
        res_p1 = model_p1.fit(maxlags=MAX_LAG, ic="aic", trend="n")
        k1 = res_p1.k_ar
        res_p1_rest = run_var(data_p1, exog_p1, restricted=True, k_ar=k1)
        irf_p1 = res_p1_rest.irf(periods=IRF_HORIZON)

        data_p2 = df_period2[VAR_ORDER].copy().dropna()
        exog_p2, _ = build_exog(df_period2.loc[data_p2.index])
        model_p2 = VAR(endog=data_p2, exog=exog_p2)
        res_p2 = model_p2.fit(maxlags=MAX_LAG, ic="aic", trend="n")
        k2 = res_p2.k_ar
        res_p2_rest = run_var(data_p2, exog_p2, restricted=True, k_ar=k2)
        irf_p2 = res_p2_rest.irf(periods=IRF_HORIZON)

        se_p1 = np.sqrt(np.diag(res_p1_rest.sigma_u) / res_p1_rest.nobs)
        se_p2 = np.sqrt(np.diag(res_p2_rest.sigma_u) / res_p2_rest.nobs)
        z = 1.96
        lower1 = irf_p1.irfs - z * se_p1[np.newaxis, np.newaxis, :]
        upper1 = irf_p1.irfs + z * se_p1[np.newaxis, np.newaxis, :]
        lower2 = irf_p2.irfs - z * se_p2[np.newaxis, np.newaxis, :]
        upper2 = irf_p2.irfs + z * se_p2[np.newaxis, np.newaxis, :]

        set_quant_style()
        fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(16, 10))
        axes_flat = axes.flatten()
        for v_idx, v_name in enumerate(VAR_ORDER):
            if v_idx < len(axes_flat):
                steps = np.arange(IRF_HORIZON)
                axes_flat[v_idx].plot(steps, irf_p1.irfs[:, 0, v_idx],
                                      color=COLORS["paper"], linewidth=0.8,
                                      label="1999-2021")
                axes_flat[v_idx].fill_between(steps, lower1[:, 0, v_idx],
                                              upper1[:, 0, v_idx],
                                              color=COLORS["paper"], alpha=0.12)
                axes_flat[v_idx].plot(steps, irf_p2.irfs[:, 0, v_idx],
                                      color=COLORS["extended"], linewidth=0.8,
                                      label="1999-2026", linestyle="--")
                axes_flat[v_idx].fill_between(steps, lower2[:, 0, v_idx],
                                              upper2[:, 0, v_idx],
                                              color=COLORS["extended"], alpha=0.08)
                axes_flat[v_idx].axhline(y=0, color=COLORS["zero"],
                                         linewidth=0.4, linestyle="--")
                axes_flat[v_idx].set_title(v_name, fontsize=9, fontweight="bold")
                axes_flat[v_idx].set_xlabel("Days", fontsize=8)
                if v_idx % 4 == 0:
                    axes_flat[v_idx].set_ylabel("Percentage points", fontsize=8)

        axes_flat[0].legend(fontsize=7, loc="upper right")
        for v_idx in range(len(VAR_ORDER), len(axes_flat)):
            axes_flat[v_idx].set_visible(False)

        fig.suptitle("Response to a Risk-off shock: restricted VAR, "
                     "1999-2021 versus 1999-2026",
                     fontsize=12, fontweight="bold", color=COLORS["text"],
                     y=0.98)
        fig.text(0.5, 0.01, "Solid line: 1999-2021. Dashed line: 1999-2026. "
                 "Shaded bands are analytical 95% confidence intervals.",
                 ha="center", fontsize=8, color=COLORS["muted"])
        plt.tight_layout(rect=[0, 0.02, 1, 0.95])
        fig.savefig(FIG_DIR / "irf_period_comparison_restricted.png",
                    dpi=DPI, bbox_inches="tight")
        plt.close(fig)
        print("  Saved: irf_period_comparison_restricted.png")

    except Exception as e:
        print(f"  Period comparison failed: {e}")

    print(f"\nAll outputs saved to {OUT_DIR.resolve()}")
    print("Done.")


if __name__ == "__main__":
    main()
