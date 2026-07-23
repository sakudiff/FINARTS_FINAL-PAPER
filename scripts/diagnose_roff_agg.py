#!/usr/bin/env python3
"""Focused monthly VAR diagnostic - why does restricted flip RGDP sign?"""
import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
from statsmodels.tsa.api import VAR
from statsmodels.regression.linear_model import OLS

PAPER_END = pd.Timestamp("2021-03-31")
VAR_ORDER = ["risk_off","log_wui","spread","log_rgdp","log_reer","log_nikkei",
             "debtsec_pct","equity_pct","other_pct","direct_pct"]
K = len(VAR_ORDER)

# Load and aggregate
df = pd.read_csv("data/processed/final_dataset.csv", parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)
mask = df["date"] <= PAPER_END
df_p1 = df[mask].copy()
df_p1["ym"] = df_p1["date"].dt.to_period("M")

# Try different risk_off aggregations
for roff_method, roff_agg in [("sum", "sum"), ("binary_any", lambda x: 1 if x.sum() > 0 else 0), ("proportion", lambda x: x.mean())]:
    monthly = df_p1.groupby("ym").agg({
        "risk_off": roff_agg, "log_wui": "last", "spread": "mean",
        "log_rgdp": "last", "log_reer": "last", "log_nikkei": "last",
        "debtsec_pct": "last", "equity_pct": "last",
        "other_pct": "last", "direct_pct": "last",
    }).reset_index()
    monthly["date"] = monthly["ym"].apply(lambda x: x.to_timestamp())
    monthly = monthly.drop(columns=["ym"]).dropna()
    data_m = monthly[VAR_ORDER].copy()

    def build_exog(df):
        month = df["date"].dt.month
        md = pd.get_dummies(month, prefix="M", drop_first=True).astype(np.float64)
        md.index = df.index
        tt = np.arange(len(df)).astype(np.float64).reshape(-1, 1)
        return np.column_stack([tt, md.values])

    exog_m = build_exog(monthly.loc[data_m.index])
    T = len(data_m)
    k_ar = 3
    lagged = np.column_stack([data_m[VAR_ORDER].values[k_ar - lag - 1:T - lag - 1, :] for lag in range(k_ar)])

    # UNRESTRICTED - risk_off equation
    y_roff = data_m["risk_off"].values[k_ar:]
    X_u = np.column_stack([lagged, exog_m[k_ar:]])
    ols_u = OLS(y_roff, X_u).fit()
    
    # RESTRICTED - risk_off equation (own lags only)
    own_cols = [0 + lag*K for lag in range(k_ar)]
    X_r = np.column_stack([lagged[:, own_cols], exog_m[k_ar:]])
    ols_r = OLS(y_roff, X_r).fit()

    print("=== risk_off = {} (range: {:.2f}-{:.2f}) ===".format(roff_method, data_m["risk_off"].min(), data_m["risk_off"].max()))
    print("  Unrestricted R²: {:.4f}, Restricted R²: {:.4f}".format(ols_u.rsquared, ols_r.rsquared))
    print("  Unrestricted residual SD: {:.4f}, Restricted residual SD: {:.4f}".format(
        np.std(ols_u.resid), np.std(ols_r.resid)))
    print("  Restricted/unrestricted residual SD ratio: {:.2f}".format(
        np.std(ols_r.resid) / np.std(ols_u.resid)))
    print()

    # Full unrestricted VAR
    model = VAR(endog=data_m, exog=exog_m)
    res_u = model.fit(maxlags=k_ar, ic="aic", trend="n")
    irf_u = res_u.irf(periods=24)
    orth_u = irf_u.orth_irfs

    # Full restricted VAR
    coeffs_r = np.zeros((K, k_ar*K + exog_m.shape[1]))
    resid_r = np.zeros((T - k_ar, K))
    for eq in range(K):
        if eq == 0:
            X_r2 = np.column_stack([lagged[:, own_cols], exog_m[k_ar:]])
        else:
            X_r2 = np.column_stack([lagged, exog_m[k_ar:]])
        o = OLS(data_m[VAR_ORDER].values[k_ar:, eq], X_r2).fit()
        coeffs_r[eq, :X_r2.shape[1]] = o.params
        resid_r[:, eq] = o.resid
    df_r = T - k_ar - X_r2.shape[1]
    sigma_r = resid_r.T @ resid_r / df_r
    chol_r = np.linalg.cholesky(sigma_r)
    coefs_r_arr = coeffs_r[:, :k_ar*K].reshape(K, k_ar, K).transpose(1, 0, 2)

    def comp_irf(coefs, chol, pers=24):
        KK = coefs.shape[1]; pk = coefs.shape[0]
        ir = np.zeros((pers+1, KK, KK)); ir[0] = np.eye(KK)
        for i in range(1, pers+1):
            for j in range(1, min(i, pk)+1):
                ir[i] += ir[i-j] @ coefs[j-1]
        for i in range(pers+1): ir[i] = ir[i] @ chol
        return ir[1:]
    irf_r = comp_irf(coefs_r_arr, chol_r)

    print("  RGDP response to risk-off shock:")
    for h in range(12):
        print("    h={:2d}: unrestricted={:+.6f}, restricted={:+.6f}".format(h, orth_u[h, 3, 0], irf_r[h, 3, 0]))
    print()
