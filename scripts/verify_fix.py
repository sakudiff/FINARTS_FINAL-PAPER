"""
Empirical verification of the restricted VAR coefficient-storage fix.

Builds a small monthly dataset, runs run_var restricted with k=3,
independently re-estimates the risk_off equation, and asserts:
  - coefs[lag, 0, 0] == OLS beta for each own lag (lag 0..k-1)
  - coefs[lag, 0, v] == 0 for v != 0 in equation 0 (cross-variable slots
    of the restricted equation are zero)
"""

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

_project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_project_root))

from scripts.var_analysis import run_var, build_exog
from statsmodels.regression.linear_model import OLS

VAR_ORDER = [
    "risk_off", "log_wui", "spread", "log_rgdp", "log_reer",
    "log_nikkei", "debtsec_pct", "equity_pct", "other_pct", "direct_pct",
]

PAPER_END = pd.Timestamp("2021-03-31")
K_LAGS = 3

print("=" * 70)
print("VERIFICATION: Restricted VAR coefficient storage fix")
print("=" * 70)

# Load data
df = pd.read_csv("data/processed/final_dataset.csv", parse_dates=["date"])
df = df[df["date"] <= PAPER_END].copy()

# Build monthly dataset
df["ym"] = df["date"].dt.to_period("M")
monthly = df.groupby("ym").agg({
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
print(f"\nMonthly data: {len(monthly)} rows, {monthly['date'].min()} to {monthly['date'].max()}")

data = monthly[VAR_ORDER].copy()
exog, exog_names = build_exog(monthly.loc[data.index])

# Run restricted VAR
print(f"\nRunning restricted VAR with k={K_LAGS}...")
results = run_var(data, exog, restricted=True, k_ar=K_LAGS)

coefs = results.coefs  # shape (k, K, K) -> (lag, eq, var)
print(f"coefs shape: {coefs.shape}")
K = len(VAR_ORDER)
k = K_LAGS
rest_idx = VAR_ORDER.index("risk_off")

# --- INDEPENDENT RE-ESTIMATION ---
endog = data.values
T = endog.shape[0]
exog_a = exog
exog_k = exog_a.shape[1]
exog_eff = exog_a[k:]

y = endog[k:]
lagged = np.column_stack([
    endog[k - lag - 1:T - lag - 1, :] for lag in range(k)
])

# Build hand-made regressors for the restricted (risk_off) equation
own_cols = [rest_idx + lag * K for lag in range(k)]
X_restricted = np.column_stack([lagged[:, own_cols], exog_eff])

# OLS re-estimation
ols_restricted = OLS(y[:, rest_idx], X_restricted).fit()
print(f"\nIndependent OLS re-estimation of risk_off equation:")
print(f"  Params (own lags + exog): {ols_restricted.params}")

# Now check: coefs[lag, 0, 0] should equal ols_restricted.params[lag]
all_ok = True
for lag in range(k):
    stored = coefs[lag, rest_idx, rest_idx]
    expected = ols_restricted.params[lag]
    match = abs(stored - expected) < 1e-10
    print(f"  coefs[lag={lag}, eq=0, var=0] = {stored:.10f}  "
          f"OLS own_lag_{lag+1} = {expected:.10f}  {'✓' if match else '✗ FAIL'}")
    if not match:
        all_ok = False

# Check cross-variable slots are zero
print(f"\nCross-variable slots (should all be zero):")
for lag in range(k):
    for v in range(K):
        if v == rest_idx:
            continue
        stored = coefs[lag, rest_idx, v]
        if abs(stored) > 1e-10:
            print(f"  coefs[lag={lag}, eq=0, var={v}] = {stored:.10f}  ✗ FAIL (should be 0)")
            all_ok = False
    # Print only non-zero cross entries for debugging (but none should be)
    cross = [coefs[lag, rest_idx, v] for v in range(K) if v != rest_idx]
    max_cross = max(abs(c) for c in cross) if cross else 0
    print(f"  lag={lag}: max |cross| = {max_cross:.2e}  {'✓' if max_cross < 1e-10 else '✗ FAIL'}")

# Also verify unrestricted equations are unchanged
print(f"\nVerifying unrestricted equations (eq != {rest_idx}):")
for eq in range(K):
    if eq == rest_idx:
        continue
    # Re-estimate unrestricted for this equation
    X_unrestricted = np.column_stack([lagged, exog_eff])
    ols_u = OLS(y[:, eq], X_unrestricted).fit()
    for lag in range(k):
        for v in range(K):
            stored = coefs[lag, eq, v]
            # Expected: stored at position lag*K + v in ols_u.params
            expected = ols_u.params[lag * K + v]
            if abs(stored - expected) > 1e-10:
                print(f"  coefs[lag={lag}, eq={eq}, var={v}] = {stored:.10f}  "
                      f"expected = {expected:.10f}  ✗ FAIL")
                all_ok = False

print(f"\n{'=' * 70}")
if all_ok:
    print("ALL ASSERTIONS PASSED ✓")
else:
    print("SOME ASSERTIONS FAILED ✗")

print(f"{'=' * 70}")
