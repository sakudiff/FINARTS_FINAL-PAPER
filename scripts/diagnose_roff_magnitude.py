#!/usr/bin/env python3
"""Compare monthly risk_off aggregations: effect on IRF magnitude and smoothness."""
import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
from statsmodels.tsa.api import VAR
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PAPER_END = pd.Timestamp("2021-03-31")
VAR_ORDER = ["risk_off","log_wui","spread","log_rgdp","log_reer","log_nikkei",
             "debtsec_pct","equity_pct","other_pct","direct_pct"]
IRF_HORIZON = 41
KEY_VARS = ["log_rgdp", "log_reer"]

df = pd.read_csv("data/processed/final_dataset.csv", parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)
mask = df["date"] <= PAPER_END
df_p1 = df[mask].copy()
df_p1["ym"] = df_p1["date"].dt.to_period("M")

agg_methods = {
    "sum (our current)": lambda x: x.sum(),
    "binary (any=1)": lambda x: 1.0 if x.sum() > 0 else 0.0,
    "proportion 0-1": lambda x: x.mean(),
}

fig, axes = plt.subplots(len(KEY_VARS), 1, figsize=(10, 6))
colors = {"sum (our current)": "#C91D42", "binary (any=1)": "#2E45B8", "proportion 0-1": "#2E9E45"}

for agg_name, agg_func in agg_methods.items():
    monthly = df_p1.groupby("ym").agg({
        "risk_off": agg_func, "log_wui": "last", "spread": "mean",
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
    model = VAR(endog=data_m, exog=exog_m)

    # BIC=3 for all
    res = model.fit(maxlags=3, ic="aic", trend="n")
    irf = res.irf(periods=IRF_HORIZON)
    orth = irf.orth_irfs  # shape (IRF_HORIZON+1, K, K)

    print(f"\n=== {agg_name} ===")
    print(f"  risk_off range: {monthly['risk_off'].min():.2f}-{monthly['risk_off'].max():.2f}")
    print(f"  risk_off mean: {monthly['risk_off'].mean():.4f}, std: {monthly['risk_off'].std():.4f}")
    sigma = np.asarray(res.sigma_u)
    chol = np.linalg.cholesky(sigma)
    print(f"  Cholesky P[0,0] (shock SD): {chol[0,0]:.4f}")

    steps = np.arange(orth.shape[0])
    for idx, vname in enumerate([("RGDP",3), ("REER",4)]):
        ax = axes[idx]
        resp = orth[:, vname[1], 0]
        ax.plot(steps, resp, color=colors[agg_name], linewidth=0.8, label=agg_name)
        ax.axhline(y=0, color="#595959", linewidth=0.4, linestyle="--")
        ax.set_title(vname[0], fontweight="bold")
        ax.set_xlabel("Months")

axes[0].legend(fontsize=8)
plt.suptitle("Monthly Unrestricted VAR (BIC=3) — risk_off aggregation comparison", fontweight="bold")
plt.tight_layout()
plt.savefig("data/processed/var_results/monthly/figures/roff_agg_comparison.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nSaved: roff_agg_comparison.png")
