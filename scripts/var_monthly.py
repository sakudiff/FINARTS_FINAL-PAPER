#!/usr/bin/env python3
"""
Monthly-frequency SVAR to check if sign discrepancies resolve at lower frequency.
Aggregates daily data to monthly, estimates restricted VAR, computes IRFs.
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

OUT = Path("data/processed/var_results/monthly_test")
OUT.mkdir(parents=True, exist_ok=True)

DPI = 150
PAPER_END = pd.Timestamp("2021-03-31")
IRF_HORIZON = 60  # ~5 years at monthly frequency (60 months)
VAR_ORDER = [
    "risk_off","log_wui","spread","log_rgdp","log_reer",
    "log_nikkei","debtsec_pct","equity_pct","other_pct","direct_pct",
]

KEY_VARS = ["log_wui", "log_rgdp", "log_reer", "spread", "log_nikkei",
            "debtsec_pct", "equity_pct", "other_pct", "direct_pct"]

COLORS = {
    "paper": "#2E45B8", "zero": "#595959",
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
    ones = np.ones((len(df), 1))
    time_trend = np.arange(len(df)).astype(np.float64).reshape(-1, 1)
    return np.column_stack([ones, time_trend, month_dummies.values])

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
        def irf(self, periods=IRF_HORIZON):
            return _compute_irf(self, periods)
    return ResVAR()

def _compute_irf(results, periods=IRF_HORIZON):
    K = results.coefs.shape[1]; k_ar = results.k_ar
    irfs = np.zeros((periods + 1, K, K)); irfs[0] = np.eye(K)
    for i in range(1, periods + 1):
        for j in range(1, min(i, k_ar) + 1):
            irfs[i] += irfs[i - j] @ results.coefs[j - 1]
    chol = np.linalg.cholesky(results.sigma_u)
    for i in range(periods + 1): irfs[i] = irfs[i] @ chol
    class IRF:
        def __init__(self):
            self.irfs = irfs; self.periods = periods
            self.model = results; self.names = results.names
    return IRF()

# Load daily data
print("Loading and aggregating to monthly...")
df = pd.read_csv("data/processed/final_dataset.csv", parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)

# Filter to original period
mask = df["date"] <= PAPER_END
df_p1 = df[mask].copy()

# Aggregate to monthly (end-of-month values for stocks, averages for flows)
df_p1["yearmonth"] = df_p1["date"].dt.to_period("M")

# For each variable, pick appropriate aggregation:
# - risk_off: sum (number of risk-off days in month) - gives more granularity
# - log_wui, log_rgdp, log_reer, log_nikkei: last value of month (stock variables)
# - spread: average (yield spread, should be averaged)
# - debtsec_pct, equity_pct, other_pct, direct_pct: last value (monthly native)
monthly = df_p1.groupby("yearmonth").agg({
    "risk_off": "sum",
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

monthly["date"] = monthly["yearmonth"].apply(lambda x: x.to_timestamp())
monthly = monthly.drop(columns=["yearmonth"])
monthly = monthly.dropna()

print("Monthly data: {} rows, {} to {}".format(
    len(monthly), monthly["date"].min(), monthly["date"].max()))

# Build data for VAR
data_m = monthly[VAR_ORDER].copy()
exog_m = build_exog(monthly.loc[data_m.index])

# Run unrestricted VAR via statsmodels for reference
model = VAR(endog=data_m, exog=exog_m)
order = model.select_order(maxlags=12, trend="n")
print("\nMonthly AIC/BIC grid:")
for i in range(len(order.ics["aic"])):
    print("  Lag {:2d}: AIC={:6.2f}, BIC={:6.2f}".format(
        i+1, order.ics["aic"][i], order.ics["bic"][i]))
print("AIC selected: {}, BIC selected: {}".format(order.aic, order.bic))

# Run unrestricted at BIC-selected lag
use_lag = order.bic
print("\nUsing lag={} for estimation".format(use_lag))

res_unr = model.fit(maxlags=use_lag, ic="aic", trend="n")
irf_unr = res_unr.irf(periods=IRF_HORIZON)
orth_unr = irf_unr.orth_irfs

# Restricted VAR at same lag
res_rest = run_restricted_var(data_m, exog_m, k_ar=use_lag)
irf_rest = res_rest.irf(periods=IRF_HORIZON)
irf_r = irf_rest.irfs

# Print numeric results
shock_idx = 0  # risk_off
key_vars = [("WUI",1),("SPREAD",2),("RGDP",3),("REER",4),("NIKKEI",5),
            ("DEBT",6),("EQUITY",7),("OTHER",8),("DIRECT",9)]

horizons = list(range(0, min(IRF_HORIZON+1, 25)))
print("\n=== Monthly Restricted VAR (lag={}) ===".format(use_lag))
print("Horizons:", ", ".join(str(h) for h in horizons))
print()
for name, idx in key_vars:
    vals = [irf_r[h, idx, shock_idx] if h < irf_r.shape[0] else 0 for h in horizons]
    print("{:8s}: {}".format(name, ", ".join(["{:.6f}".format(v) for v in vals])))

print("\n=== Monthly Unrestricted VAR (lag={}) ===".format(use_lag))
for name, idx in key_vars:
    vals = [orth_unr[h, idx, shock_idx] if h < orth_unr.shape[0] else 0 for h in horizons]
    print("{:8s}: {}".format(name, ", ".join(["{:.6f}".format(v) for v in vals])))

# Plot the restricted IRFs for visual comparison
set_style()
key_indices = [VAR_ORDER.index(v) for v in KEY_VARS]
ncols = 3
nrows = int(np.ceil(len(KEY_VARS) / ncols))
fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10, 2.5*nrows),
                          sharex=False, sharey=False)
axes_flat = axes.flatten()
steps = np.arange(irf_r.shape[0])

# Delta-method CIs via bootstrap
from var_analysis import _delta_irf_ci
lower, upper = _delta_irf_ci(irf_rest, B=500)

for i, (vname, vidx) in enumerate(zip(KEY_VARS, key_indices)):
    ax = axes_flat[i]
    resp = irf_r[:, vidx, shock_idx]
    ax.plot(steps, resp, color=COLORS["paper"], linewidth=0.8)
    ax.fill_between(steps, lower[:, vidx], upper[:, vidx],
                    color=COLORS["paper"], alpha=0.15)
    ax.axhline(y=0, color=COLORS["zero"], linewidth=0.4, linestyle="--")
    ax.set_title(vname, fontsize=9, fontweight="bold")
    ax.set_xlabel("Months")
    if i % ncols == 0:
        ax.set_ylabel("Percentage points")
for j in range(len(KEY_VARS), len(axes_flat)):
    axes_flat[j].set_visible(False)
fig.suptitle("Monthly Restricted VAR (lag={}) — Response to Risk-off shock, 1999-2021".format(use_lag),
             fontsize=11, fontweight="bold", y=0.98)
plt.tight_layout(rect=[0, 0.02, 1, 0.95])
fname = "monthly_restricted_lag{}.png".format(use_lag)
fig.savefig(OUT / fname, dpi=DPI, bbox_inches="tight")
plt.close(fig)
print("\nSaved: {}".format(fname))

# Summary
lines = [
    "Monthly VAR Test Summary",
    "========================",
    "Original period: {} to {} ({} months)".format(
        monthly["date"].min(), monthly["date"].max(), len(monthly)),
    "",
    "AIC selected lag: {}".format(order.aic),
    "BIC selected lag: {}".format(order.bic),
    "Using lag: {}".format(use_lag),
    "",
]
(OUT / "monthly_test_summary.txt").write_text("\n".join(lines))
print("Done.")
