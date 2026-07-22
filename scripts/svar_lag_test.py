#!/usr/bin/env python3
"""
SVAR lag grid test — runs AIC across maxlags bounds, estimates restricted VAR
at each candidate lag, produces IRF plots for visual comparison.
Focus: original paper period 1999-2021.
"""
import os, sys, warnings
from pathlib import Path
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from statsmodels.tsa.api import VAR
warnings.filterwarnings("ignore", category=FutureWarning)

OUT = Path("data/processed/var_results/lag_test")
OUT.mkdir(parents=True, exist_ok=True)

DPI = 150
PAPER_END = pd.Timestamp("2021-03-31")
IRF_HORIZON = 125
VAR_ORDER = [
    "risk_off", "log_wui", "spread", "log_rgdp", "log_reer",
    "log_nikkei", "debtsec_pct", "equity_pct", "other_pct", "direct_pct",
]

KEY_VARS = ["log_wui", "log_rgdp", "log_reer", "spread", "log_nikkei",
            "debtsec_pct", "equity_pct", "other_pct", "direct_pct"]

COLORS = {
    "paper": "#2E45B8", "ci_fill": "#D6DBF5", "zero": "#595959",
    "bg": "#F5F4EF", "grid": "#D9D9D9", "text": "#0D0D0D", "muted": "#595959",
}

def set_style():
    plt.rcParams.update({
        "axes.grid": True, "grid.color": COLORS["grid"], "grid.linewidth": 0.3,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.spines.left": False, "axes.spines.bottom": True,
        "axes.titleweight": "bold", "axes.titlesize": 10, "axes.labelsize": 8,
        "axes.labelcolor": COLORS["muted"], "xtick.major.size": 0,
        "ytick.major.size": 0, "xtick.color": COLORS["muted"],
        "ytick.color": COLORS["muted"], "legend.fontsize": 7,
        "legend.frameon": False, "text.color": COLORS["text"],
        "figure.facecolor": COLORS["bg"], "axes.facecolor": COLORS["bg"],
    })

def build_exog(df):
    month = df["date"].dt.month
    month_dummies = pd.get_dummies(month, prefix="M", drop_first=True).astype(np.float64)
    month_dummies.index = df.index
    time_trend = np.arange(len(df)).astype(np.float64).reshape(-1, 1)
    return np.column_stack([time_trend, month_dummies.values])

def run_restricted_var(data, exog, k_ar):
    endog = data.values
    T, K = endog.shape
    exog_a = exog if exog is not None else np.empty((T, 0))
    exog_k = exog_a.shape[1]
    rest_idx = data.columns.get_loc("risk_off")
    y = endog[k_ar:]
    lagged = np.column_stack([endog[k_ar - lag - 1:T - lag - 1, :] for lag in range(k_ar)])
    exog_eff = exog_a[k_ar:]
    K_all_lags = K * k_ar
    coeffs = np.zeros((K, K_all_lags + exog_k))
    resid = np.zeros((T - k_ar, K))
    from statsmodels.regression.linear_model import OLS
    for eq in range(K):
        if eq == rest_idx:
            own_cols = [rest_idx + lag * K for lag in range(k_ar)]
            X = np.column_stack([lagged[:, own_cols], exog_eff])
        else:
            X = np.column_stack([lagged, exog_eff])
        ols_res = OLS(y[:, eq], X).fit()
        coeffs[eq, :X.shape[1]] = ols_res.params
        resid[:, eq] = ols_res.resid
    df_resid = T - k_ar - (K_all_lags + exog_k)
    sigma_u = resid.T @ resid / df_resid
    class ResVAR:
        def __init__(self):
            self.coefs = coeffs[:, :K_all_lags].reshape(K, k_ar, K).transpose(1, 0, 2)
            self.params = coeffs; self.resid = resid; self.sigma_u = sigma_u
            self.k_ar = k_ar; self.k_trend = 0; self.k_exog = exog_k; self.k_ma = 0
            self.n_totobs = T; self.nobs = T - k_ar; self.df_resid = df_resid
            self.df_model = K_all_lags + exog_k; self.names = data.columns.tolist()
            self.endog = endog; self.exog = exog_eff; self.llf = 0.0
            self.params_exog = coeffs[:, K_all_lags:] if exog_k > 0 else np.empty((K, 0))
        def irf(self, periods=125):
            return _compute_irf(self, periods)
    return ResVAR()

def _compute_irf(results, periods=125):
    K = results.coefs.shape[1]; k_ar = results.k_ar
    irfs = np.zeros((periods + 1, K, K)); irfs[0] = np.eye(K)
    for i in range(1, periods + 1):
        for j in range(1, min(i, k_ar) + 1):
            irfs[i] += irfs[i - j] @ results.coefs[j - 1]
    chol = np.linalg.cholesky(results.sigma_u)
    for i in range(periods + 1):
        irfs[i] = irfs[i] @ chol
    class IRF:
        def __init__(self):
            self.irfs = irfs[1:]; self.periods = periods
            self.model = results; self.names = results.names
    return IRF()

print("Loading data...")
df = pd.read_csv("data/processed/final_dataset.csv", parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)

# Original paper period
mask = df["date"] <= PAPER_END
df_p1 = df[mask].copy()
print("Original period: {} to {}, {} rows".format(
    df_p1["date"].min(), df_p1["date"].max(), len(df_p1)))

data_p1 = df_p1[VAR_ORDER].copy().dropna()
exog_p1 = build_exog(df_p1.loc[data_p1.index])
print("After dropna: {} rows".format(len(data_p1)))

# --- PART 1: AIC / BIC grid ---
print("\n=== AIC/BIC Grid Search (maxlags=1..20) ===")
model = VAR(endog=data_p1, exog=exog_p1)
order = model.select_order(maxlags=20, trend="n")
aic_vals = order.ics["aic"]
bic_vals = order.ics["bic"]

aic_selected = order.aic
bic_selected = order.bic

print("Lag  AIC        BIC")
for i in range(len(aic_vals)):
    lag = i + 1
    print("{:3d}  {:8.2f}  {:8.2f}".format(lag, aic_vals[i], bic_vals[i]))
print("")
print("AIC selected lag: {}".format(aic_selected))
print("BIC selected lag: {}".format(bic_selected))

# Also check what AIC gives with different maxlags caps
print("\n=== AIC with varying maxlags caps ===")
for cap in [5, 6, 7, 8, 10, 12, 15]:
    m = VAR(endog=data_p1, exog=exog_p1)
    r = m.fit(maxlags=cap, ic="aic", trend="n")
    selected = r.k_ar
    boundary = " (at boundary)" if selected == cap else ""
    print("  maxlags={:2d} -> AIC selects lag={}{}".format(cap, selected, boundary))

# --- PART 2: IRF plots for each candidate lag ---
test_lags = sorted(set([5, 6, 7, 8, 10, 12, 15, aic_selected]))

print("\n=== Generating IRF plots for lags: {} ===".format(test_lags))
for lag in test_lags:
    print("\n--- Lag {} ---".format(lag))
    res = run_restricted_var(data_p1, exog_p1, k_ar=lag)
    irf = res.irf(periods=IRF_HORIZON)
    irf_vals = irf.irfs

    # Analytical CIs — IRF is [horizon, response_var, shock_var]
    # Shock is risk_off = variable 0
    shock_idx = 0
    z = 1.96
    se = np.sqrt(np.diag(res.sigma_u) / res.nobs)
    lower = irf_vals[:, :, shock_idx] - z * se[np.newaxis, :]
    upper = irf_vals[:, :, shock_idx] + z * se[np.newaxis, :]

    set_style()
    key_indices = [VAR_ORDER.index(v) for v in KEY_VARS]
    ncols = 3
    nrows = int(np.ceil(len(KEY_VARS) / ncols))
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10, 2.5*nrows),
                              sharex=False, sharey=False)
    axes_flat = axes.flatten()
    steps = np.arange(IRF_HORIZON)
    for i, (vname, vidx) in enumerate(zip(KEY_VARS, key_indices)):
        ax = axes_flat[i]
        resp = irf_vals[:, vidx, shock_idx]
        ax.plot(steps, resp, color=COLORS["paper"], linewidth=0.8)
        ax.fill_between(steps, lower[:, vidx], upper[:, vidx],
                        color=COLORS["paper"], alpha=0.15)
        ax.axhline(y=0, color=COLORS["zero"], linewidth=0.4, linestyle="--")
        ax.set_title(vname, fontsize=9, fontweight="bold")
        ax.set_xlabel("Days")
        if i % ncols == 0:
            ax.set_ylabel("Percentage points")
    for j in range(len(KEY_VARS), len(axes_flat)):
        axes_flat[j].set_visible(False)
    fig.suptitle("Response to Risk-off shock — Restricted VAR, Lag={}, 1999-2021".format(lag),
                 fontsize=11, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0.02, 1, 0.95])
    fname = "lag_{}_original_period.png".format(lag)
    fig.savefig(OUT / fname, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print("  Saved: {}".format(fname))

# Summary
lines = ["SVAR Lag Test Summary", "====================", ""]
lines.append("Dataset: final_dataset.csv")
lines.append("Original period: {} to {} ({} rows)".format(
    df_p1["date"].min(), df_p1["date"].max(), len(df_p1)))
lines.append("After dropna: {} rows".format(len(data_p1)))
lines.append("")
lines.append("AIC selected lag (maxlags=20): {}".format(aic_selected))
lines.append("BIC selected lag (maxlags=20): {}".format(bic_selected))
lines.append("")
lines.append("Lag  AIC      BIC")
for i in range(len(aic_vals)):
    lines.append("  {:2d}  {:8.2f}  {:8.2f}".format(i+1, aic_vals[i], bic_vals[i]))
lines.append("")
lines.append("Generated IRF plots for lags: {}".format(test_lags))
(OUT / "lag_test_summary.txt").write_text("\n".join(lines))
print("\nSummary saved to {}".format(OUT / "lag_test_summary.txt"))
print("Done.")
