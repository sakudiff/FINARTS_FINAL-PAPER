#!/usr/bin/env python3
"""
Diagnose why monthly restricted VAR flips RGDP sign while unrestricted doesn't.
Compares coefficients, residuals, Cholesky factors, and traces the IRF source.
"""
import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
from statsmodels.tsa.api import VAR

PAPER_END = pd.Timestamp("2021-03-31")
VAR_ORDER = [
    "risk_off","log_wui","spread","log_rgdp","log_reer",
    "log_nikkei","debtsec_pct","equity_pct","other_pct","direct_pct",
]

df = pd.read_csv("data/processed/final_dataset.csv", parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)
mask = df["date"] <= PAPER_END
df_p1 = df[mask].copy()

# Aggregate to monthly
df_p1["ym"] = df_p1["date"].dt.to_period("M")
monthly = df_p1.groupby("ym").agg({
    "risk_off": "sum", "log_wui": "last", "spread": "mean",
    "log_rgdp": "last", "log_reer": "last", "log_nikkei": "last",
    "debtsec_pct": "last", "equity_pct": "last",
    "other_pct": "last", "direct_pct": "last",
}).reset_index()
monthly["date"] = monthly["ym"].apply(lambda x: x.to_timestamp())
monthly = monthly.drop(columns=["ym"]).dropna()

data_m = monthly[VAR_ORDER].copy()

def build_exog(df):
    month = df["date"].dt.month
    month_dummies = pd.get_dummies(month, prefix="M", drop_first=True).astype(np.float64)
    month_dummies.index = df.index
    time_trend = np.arange(len(df)).astype(np.float64).reshape(-1, 1)
    return np.column_stack([time_trend, month_dummies.values])

exog_m = build_exog(monthly.loc[data_m.index])
K = len(VAR_ORDER)
T = len(data_m)
k_ar = 3  # BIC-selected

# === 1. UNRESTRICTED VAR ===
model = VAR(endog=data_m, exog=exog_m)
res_u = model.fit(maxlags=k_ar, ic="aic", trend="n")
coefs_u = res_u.coefs  # (k_ar, K, K): [lag, eq, var]
sigma_u = res_u.sigma_u
chol_u = np.linalg.cholesky(sigma_u)
resid_u = res_u.resid

# Unrestricted risk_off equation (equation 0) coefficients
print("=== UNRESTRICTED VAR ===")
print("Risk-off equation coefficients (all lags):")
for lag in range(k_ar):
    for var in range(K):
        print("  L{}.{}: {:.6f}".format(lag+1, VAR_ORDER[var], coefs_u[lag, 0, var]))
resid_u_arr = resid_u.values if hasattr(resid_u, 'values') else resid_u
print("Risk-off residual std: {:.6f}".format(np.std(resid_u_arr[:, 0])))
sigma_u_val = sigma_u.iloc[0, 0] if hasattr(sigma_u, 'iloc') else sigma_u[0, 0]
print("Sigma_u[0,0]: {:.8f}".format(sigma_u_val))
print("Cholesky P[0,0]: {:.6f}".format(chol_u[0, 0]))
print()

# Which variables significantly predict risk_off?
from statsmodels.regression.linear_model import OLS
y_roff = data_m[VAR_ORDER[0]].values[k_ar:]
lagged = np.column_stack([data_m[VAR_ORDER].values[k_ar - lag - 1:T - lag - 1, :] for lag in range(k_ar)])
X_u = np.column_stack([lagged, exog_m[k_ar:]])
ols_u = OLS(y_roff, X_u).fit()
print("Unrestricted risk_off equation F-test for each variable block (do lags predict risk_off?):")
for var in range(1, K):
    col_indices = [var + lag*K for lag in range(k_ar)]
    r = ols_u.f_test(np.eye(k_ar), None, col_indices)
    print("  {:15s}: F={:6.3f}, p={:.4f}".format(VAR_ORDER[var], r.statistic, r.pvalue))
print()

# === 2. RESTRICTED VAR ===
# Build restricted coefficients manually
coeffs_r = np.zeros((K, k_ar * K + exog_m.shape[1]))
resid_r = np.zeros((T - k_ar, K))
from statsmodels.regression.linear_model import OLS
for eq in range(K):
    if eq == 0:  # risk_off: only own lags
        own_cols = [0 + lag * K for lag in range(k_ar)]
        X_r = np.column_stack([lagged[:, own_cols], exog_m[k_ar:]])
    else:
        X_r = np.column_stack([lagged, exog_m[k_ar:]])
    ols_r = OLS(data_m[VAR_ORDER].values[k_ar:, eq], X_r).fit()
    coeffs_r[eq, :X_r.shape[1]] = ols_r.params
    resid_r[:, eq] = ols_r.resid

sigma_r = resid_r.T @ resid_r / (T - k_ar - X_r.shape[1])
chol_r = np.linalg.cholesky(sigma_r)

print("=== RESTRICTED VAR ===")
print("Risk-off equation coefficients (own lags only):")
for lag in range(k_ar):
    print("  L{}.{}: {:.6f}".format(lag+1, VAR_ORDER[0], coeffs_r[0, 0 + lag*K]))
print("Risk-off residual std: {:.6f}".format(np.std(resid_r[:, 0])))
print("Sigma_u[0,0]: {:.8f}".format(sigma_r[0, 0]))
print("Cholesky P[0,0]: {:.6f}".format(chol_r[0, 0]))
print()

# === 3. COMPARE IRF STEP BY STEP ===
def compute_irf(coefs_arr, chol, periods=24):
    Kk = coefs_arr.shape[1]
    pk = coefs_arr.shape[0]
    irfs = np.zeros((periods + 1, Kk, Kk)); irfs[0] = np.eye(Kk)
    for i in range(1, periods + 1):
        for j in range(1, min(i, pk) + 1):
            irfs[i] += irfs[i - j] @ coefs_arr[j - 1]
    for i in range(periods + 1):
        irfs[i] = irfs[i] @ chol
    return irfs[1:]  # (periods, K, K)

coefs_u_arr = np.asarray(res_u.coefs)
coefs_r_arr = np.asarray(coeffs_r[:, :k_ar*K].reshape(K, k_ar, K).transpose(1, 0, 2))

irf_u = compute_irf(coefs_u_arr, chol_u)
irf_r = compute_irf(coefs_r_arr, chol_r)

print("=== IRF COMPARISON: RGDP response to risk-off shock ===")
print("Horizon  Unrestricted  Restricted")
for h in range(12):
    print("  {:3d}     {:+.6f}    {:+.6f}".format(h, irf_u[h, 3, 0], irf_r[h, 3, 0]))

print()
print("=== IRF COMPARISON: REER response to risk-off shock ===")
print("Horizon  Unrestricted  Restricted")
for h in range(12):
    print("  {:3d}     {:+.6f}    {:+.6f}".format(h, irf_u[h, 4, 0], irf_r[h, 4, 0]))

# === 4. DECOMPOSE THE RESTRICTED IRF ===
# The IRF at horizon 1 is: A_1 @ chol
# Let's see what A_1 looks like for both
print()
print("=== LAG-1 COEFFICIENT MATRICES (risk_off column) ===")
print("Effect of risk_off[t-1] on each equation at t:")
for var in range(K):
    print("  {:15s}: unrestricted={:+.6f}, restricted={:+.6f}".format(
        VAR_ORDER[var], coefs_u_arr[0, var, 0], coefs_r_arr[0, var, 0]))

print()
print("=== LAG-1 COEFFICIENT MATRICES (RGDP column) ===")
print("Effect of log_rgdp[t-1] on each equation at t:")
for var in range(K):
    print("  {:15s}: unrestricted={:+.6f}, restricted={:+.6f}".format(
        VAR_ORDER[var], coefs_u_arr[0, var, 3], coefs_r_arr[0, var, 3]))

# === 5. UNDERSTAND THE CHAIN: shock -> risk_off equation -> IRF ===
print()
print("=== CHOLESKY FACTOR COMPARISON ===")
print(" P[0,0] (risk_off shock SD): unrestricted={:.6f}, restricted={:.6f}".format(
    chol_u[0, 0], chol_r[0, 0]))
print(" P[3,0] (contemporaneous RGDP from risk_off): unrestricted={:.6f}, restricted={:.6f}".format(
    chol_u[3, 0], chol_r[3, 0]))
print(" P[4,0] (contemporaneous REER from risk_off): unrestricted={:.6f}, restricted={:.6f}".format(
    chol_u[4, 0], chol_r[4, 0]))

# The contemporaneous impact (horizon 0) of risk_off shock on each variable
print()
print("Contemporaneous impact (horizon 0 = Cholesky column 0):")
for var in range(K):
    print("  {:15s}: unrestricted={:+.6f}, restricted={:+.6f}".format(
        VAR_ORDER[var], chol_u[var, 0], chol_r[var, 0]))

# === 6. CORRELATION BETWEEN RESTRICTED AND UNRESTRICTED RESIDUALS ===
print()
print("=== RESIDUAL COMPARISON ===")
resid_u_arr = resid_u.values if hasattr(resid_u, 'values') else resid_u
print("Correlation of risk_off residuals (restricted vs unrestricted): {:.4f}".format(
    np.corrcoef(resid_u_arr[:, 0], resid_r[:, 0])[0, 1]))
print("Risk_off residual variance ratio (restricted/unrestricted): {:.4f}".format(
    np.var(resid_r[:, 0]) / np.var(resid_u_arr[:, 0])))
