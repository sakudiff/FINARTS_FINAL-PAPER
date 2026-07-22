#!/usr/bin/env python3
"""
Compare IRF numeric values across restricted (fixed) and unrestricted VARs.
"""
import numpy as np, pandas as pd, warnings, sys
warnings.filterwarnings("ignore")
sys.path.insert(0, "scripts")

from statsmodels.tsa.api import VAR
from svar_lag_test import run_restricted_var, build_exog

PAPER_END = pd.Timestamp("2021-03-31")
IRF_HORIZON = 125
VAR_ORDER = [
    "risk_off","log_wui","spread","log_rgdp","log_reer",
    "log_nikkei","debtsec_pct","equity_pct","other_pct","direct_pct",
]

df = pd.read_csv("data/processed/final_dataset.csv", parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)
mask = df["date"] <= PAPER_END
df_p1 = df[mask].copy()
data_p1 = df_p1[VAR_ORDER].copy().dropna()
exog_p1 = build_exog(df_p1.loc[data_p1.index])

# -------------------------
# 1. Restricted VAR via fixed code, lag=6
# -------------------------
res_rest = run_restricted_var(data_p1, exog_p1, k_ar=6)
irf_rest = res_rest.irf(periods=IRF_HORIZON)
irf_r = irf_rest.irfs  # (periods, K, K), Cholesky-orthogonalized

# -------------------------
# 2. Unrestricted VAR via statsmodels, lag=6
# -------------------------
model = VAR(endog=data_p1, exog=exog_p1)
res_unr = model.fit(maxlags=6, ic="aic", trend="n")
irf_u_obj = res_unr.irf(periods=IRF_HORIZON)
orth_u = irf_u_obj.orth_irfs  # (periods+1, K, K)

# Also get non-orthogonalized for comparison
irf_u_nonorth = irf_u_obj.irfs

# -------------------------
# 3. Restricted via OLS - also compare prediction coefficients
# -------------------------

key_vars = [("WUI",1),("SPREAD",2),("RGDP",3),("REER",4),
            ("NIKKEI",5),("DEBT",6),("EQUITY",7),("OTHER",8),("DIRECT",9)]

horizons = [0, 1, 5, 10, 25, 50, 75, 100, 125]

print("=== Restricted VAR (FIXED, lag=6) ===")
print("  Response to one-SD risk-off shock")
print("")
for name, idx in key_vars:
    h_idx = [min(h, irf_r.shape[0]-1) for h in horizons]
    vals = [irf_r[h, 0, idx] for h in h_idx]
    print("{:8s}: ".format(name) + ", ".join(["{:.6f}".format(v) for v in vals]))

print("")
print("=== Unrestricted VAR (statsmodels, lag=6) ===")
print("")
for name, idx in key_vars:
    h_idx = [min(h, orth_u.shape[0]-1) for h in horizons]
    vals = [orth_u[h, 0, idx] for h in h_idx]
    print("{:8s}: ".format(name) + ", ".join(["{:.6f}".format(v) for v in vals]))

# Compare coefficient matrices
print("")
print("=== Coef comparison at lag 1 (risk_off equation) ===")
print("Risk-off equation, Lag 1 coefficients:")
print("Our restricted coefs[0,0,:]:", res_rest.coefs[0,0,:])
print("Unrestricted coefs[0,0,:]:", res_unr.coefs[0,0,:])
print("")
print("Risk-off equation, Lag 1, only risk_off coef:")
print("  Our restricted: {:.6f}".format(res_rest.coefs[0,0,0]))
print("  Unrestricted:   {:.6f}".format(res_unr.coefs[0,0,0]))

print("")
print("RGDP equation, Lag 1 risk_off coef:")
print("  Our restricted: {:.6f}".format(res_rest.coefs[0,3,0]))
print("  Unrestricted:   {:.6f}".format(res_unr.coefs[0,3,0]))

print("")
print("Sigma_u diagonal (residual variances):")
for i, v in enumerate(VAR_ORDER):
    print("  {:15s}: restricted={:.8f}  unrestricted={:.8f}".format(
        v, res_rest.sigma_u[i,i], res_unr.sigma_u[i,i]))

print("")
print("Cholesky diagonal (shock SDs):")
chol_r = np.linalg.cholesky(res_rest.sigma_u)
chol_u = np.linalg.cholesky(res_unr.sigma_u)
for i, v in enumerate(VAR_ORDER):
    print("  {:15s}: restricted={:.8f}  unrestricted={:.8f}".format(
        v, chol_r[i,i], chol_u[i,i]))
