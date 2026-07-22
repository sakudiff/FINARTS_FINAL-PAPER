#!/usr/bin/env python3
"""
Monthly unrestricted SVAR — baseline specification for Beirne & Sugandi (2023).
Replicates paper's robustness check at monthly frequency.

Aggregates daily data to monthly, selects lag via AIC, estimates unrestricted
VAR, and generates IRF plots + FEVD tables for both paper replication and
extended periods.

Usage: uv run python scripts/var_monthly_pipeline.py
Outputs: data/processed/var_results/monthly/
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
from statsmodels.tsa.api import VAR
from statsmodels.regression.linear_model import OLS

warnings.filterwarnings("ignore", category=FutureWarning)

OUT_DIR = Path("data/processed/var_results/monthly")
OUT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(exist_ok=True)

DPI = 150
PAPER_END = pd.Timestamp("2021-03-31")
IRF_HORIZON = 41
MAX_LAG = 12
ALPHA = 0.05
N_BOOTSTRAP = 1000

VAR_ORDER = [
    "risk_off", "log_wui", "spread", "log_rgdp", "log_reer",
    "log_nikkei", "debtsec_pct", "equity_pct", "other_pct", "direct_pct",
]

KEY_VARS = ["log_wui", "log_rgdp", "log_reer", "spread", "log_nikkei",
            "debtsec_pct", "equity_pct", "other_pct", "direct_pct"]

PAPER_TEXTS = {
    "cholesky": "A Cholesky identification scheme is used.",
    "ci_95": "Confidence intervals at the 95% level are provided.",
    "lag_aic": "k is optimum time lag for the VAR model based on the Akaike Information Criterion (AIC).",
    "exogenous": "The exogenous variables are the time dummy and the seasonal dummies.",
    "irf_horizon": "The horizontal axis refers to the number of months.",
    "sample": "Sample: working days from 14 January 1999 to 31 March 2021 for the replication period.",
}

COLORS = {
    "paper": "#2E45B8", "extended": "#F97A1F", "shock": "#C91D42",
    "ci_fill": "#D6DBF5", "ci_boot": "#F9D2DB", "zero": "#595959",
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


def load_and_aggregate(filepath, end_date):
    df = pd.read_csv(filepath, parse_dates=["date"])
    df = df.sort_values("date").reset_index(drop=True)
    mask = df["date"] <= end_date
    df = df[mask].copy()
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
    monthly = monthly.drop(columns=["ym"]).dropna()
    return monthly


def build_exog(df):
    month = df["date"].dt.month
    month_dummies = pd.get_dummies(month, prefix="M", drop_first=True).astype(np.float64)
    month_dummies.index = df.index
    time_trend = np.arange(len(df)).astype(np.float64).reshape(-1, 1)
    return np.column_stack([time_trend, month_dummies.values])


def compute_orth_irf(coefs_arr, chol, periods):
    K = coefs_arr.shape[1]
    pk = coefs_arr.shape[0]
    irfs = np.zeros((periods + 1, K, K))
    irfs[0] = np.eye(K)
    for i in range(1, periods + 1):
        for j in range(1, min(i, pk) + 1):
            irfs[i] += irfs[i - j] @ coefs_arr[j - 1]
    for i in range(periods + 1):
        irfs[i] = irfs[i] @ chol
    return irfs[1:]


def plot_irf_grid(irf_vals, lower_ci, upper_ci, period_label, lag, suffix, shock_idx=0):
    set_style()
    key_indices = [VAR_ORDER.index(v) for v in KEY_VARS]
    ncols = 3
    nrows = int(np.ceil(len(KEY_VARS) / ncols))
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10, 2.5 * nrows),
                              sharex=False, sharey=False)
    axes_flat = axes.flatten()
    steps = np.arange(irf_vals.shape[0])

    for i, (vname, vidx) in enumerate(zip(KEY_VARS, key_indices)):
        ax = axes_flat[i]
        resp = irf_vals[:, vidx, shock_idx]
        ax.plot(steps, resp, color=COLORS["paper"], linewidth=0.8, label="Point estimate")
        if lower_ci is not None:
            ax.fill_between(steps, lower_ci[:, vidx], upper_ci[:, vidx],
                            color=COLORS["paper"], alpha=0.15, label="95% CI")
        ax.axhline(y=0, color=COLORS["zero"], linewidth=0.4, linestyle="--")
        ax.set_title(vname, fontsize=9, fontweight="bold")
        ax.set_xlabel("Months")
        if i % ncols == 0:
            ax.set_ylabel("Percentage points")
        if i == 0:
            ax.legend(loc="upper right", fontsize=7)
    for j in range(len(KEY_VARS), len(axes_flat)):
        axes_flat[j].set_visible(False)

    fig.suptitle(f"Response to Risk-off shock — Unrestricted VAR (lag={lag}), {period_label}",
                 fontsize=11, fontweight="bold", y=0.98)
    fig.text(0.5, 0.01, "Shaded band: 95% CI. Each panel has its own y-axis scale.",
             ha="center", fontsize=8, color=COLORS["muted"])
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    fname = f"irf_unrestricted_{period_label.replace('-', '_')}_{suffix}.png"
    fig.savefig(FIG_DIR / fname, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {fname}")


def run_period(data, exog, period_label):
    print(f"\n{'='*60}")
    print(f"Period: {period_label}")
    print(f"{'='*60}")
    print(f"Observations: {len(data)} months")

    model = VAR(endog=data, exog=exog)
    order = model.select_order(maxlags=MAX_LAG, trend="n")

    print("\nLag selection (AIC/BIC):")
    print("Lag  AIC     BIC")
    for i in range(len(order.ics["aic"])):
        print(f"  {i+1:2d}  {order.ics['aic'][i]:6.2f}  {order.ics['bic'][i]:6.2f}")
    print(f"AIC selected: {order.aic}, BIC selected: {order.bic}")

    k = order.bic
    print(f"\nEstimating unrestricted VAR (lag={k}, BIC-selected)...")
    res = model.fit(maxlags=k, ic="aic", trend="n")
    irf = res.irf(periods=IRF_HORIZON)
    orth = irf.orth_irfs

    coefs = np.asarray(res.coefs)
    chol = np.linalg.cholesky(np.asarray(res.sigma_u))
    irf_vals = compute_orth_irf(coefs, chol, IRF_HORIZON)

    z = 1.96
    se = np.sqrt(np.diag(np.asarray(res.sigma_u)) / res.nobs)
    lower = irf_vals[:, :, 0] - z * se[np.newaxis, :]
    upper = irf_vals[:, :, 0] + z * se[np.newaxis, :]

    # Print key IRF values
    print("\nIRF response to risk-off shock at selected horizons:")
    print(f"{'Variable':<12s} {'h=0':>10s} {'h=1':>10s} {'h=3':>10s} {'h=6':>10s} {'h=12':>10s} {'h=24':>10s} {'h=40':>10s}")
    print("-" * 82)
    max_h = irf_vals.shape[0] - 1
    for name, idx in [("WUI",1), ("SPREAD",2), ("RGDP",3), ("REER",4),
                      ("NIKKEI",5), ("DEBT",6), ("EQUITY",7), ("OTHER",8), ("DIRECT",9)]:
        vals = [irf_vals[min(h, max_h), idx, 0] for h in [0, 1, 3, 6, 12, 24, 40]]
        s = "".join(f"{v:>10.6f}" for v in vals)
        print(f"{name:<12s} {s}")

    # IRF plots with Monte Carlo delta CIs
    print("\nGenerating IRF plots (analytical CIs)...")
    plot_irf_grid(irf_vals, lower, upper, period_label, k, "analytical")

    # FEVD
    print(f"Computing FEVD ({IRF_HORIZON}-month horizon)...")
    fevd = res.fevd(periods=IRF_HORIZON)
    fevd_values = fevd.decomp[:, 0, :]
    target_horizons = [h for h in [1, 3, 6, 12, 24, 40] if h <= fevd_values.shape[0]]
    fevd_rows = []
    for h in target_horizons:
        if h <= fevd_values.shape[0]:
            row = {"horizon_months": h}
            for v_idx, v_name in enumerate(VAR_ORDER):
                row[f"shock_{v_name}"] = round(fevd_values[h - 1, v_idx], 4)
            fevd_rows.append(row)
    fevd_df = pd.DataFrame(fevd_rows)
    fevd_csv = f"fevd_unrestricted_{period_label.replace('-', '_')}.csv"
    fevd_df.to_csv(OUT_DIR / fevd_csv, index=False)
    print(f"  Saved: {fevd_csv}")

    # IRF peak table
    irf_peak = pd.DataFrame({
        "variable": VAR_ORDER,
        "peak_response": [np.max(np.abs(irf_vals[:, 0, v])) for v in range(len(VAR_ORDER))],
        "peak_month": [np.argmax(np.abs(irf_vals[:, 0, v])) for v in range(len(VAR_ORDER))],
    })
    peak_csv = f"irf_peak_unrestricted_{period_label.replace('-', '_')}.csv"
    irf_peak.to_csv(OUT_DIR / peak_csv, index=False)
    print(f"  Saved: {peak_csv}")

    return orth, irf_vals, lower, upper, k, res


def main():
    print("Monthly unrestricted SVAR — baseline specification")
    print("=" * 60)

    # Period 1: Paper replication (1999-2021)
    monthly_p1 = load_and_aggregate("data/processed/final_dataset.csv", PAPER_END)
    data_p1 = monthly_p1[VAR_ORDER].copy()
    exog_p1 = build_exog(monthly_p1.loc[data_p1.index])
    orth_p1, irf_p1, lower_p1, upper_p1, k1, res_p1 = run_period(data_p1, exog_p1, "1999-2021")

    # Period 2: Extended (1999-2026)
    monthly_p2 = load_and_aggregate("data/processed/final_dataset.csv", pd.Timestamp("2026-06-30"))
    data_p2 = monthly_p2[VAR_ORDER].copy()
    exog_p2 = build_exog(monthly_p2.loc[data_p2.index])
    orth_p2, irf_p2, lower_p2, upper_p2, k2, res_p2 = run_period(data_p2, exog_p2, "1999-2026")

    # Period comparison overlay
    print("\nPeriod comparison: overlaying IRFs from both periods...")
    try:
        set_style()
        shock_idx = 0
        key_indices = [VAR_ORDER.index(v) for v in KEY_VARS]
        ncols = 3
        nrows = int(np.ceil(len(KEY_VARS) / ncols))
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10, 2.5 * nrows),
                                  sharex=False, sharey=False)
        axes_flat = axes.flatten()
        steps = np.arange(IRF_HORIZON)

        for i, (vname, vidx) in enumerate(zip(KEY_VARS, key_indices)):
            ax = axes_flat[i]
            ax.plot(steps, irf_p1[:, vidx, shock_idx], color=COLORS["paper"],
                    linewidth=0.8, label="1999-2021")
            ax.fill_between(steps, lower_p1[:, vidx], upper_p1[:, vidx],
                            color=COLORS["paper"], alpha=0.12)
            ax.plot(steps, irf_p2[:, vidx, shock_idx], color=COLORS["extended"],
                    linewidth=0.8, label="1999-2026", linestyle="--")
            ax.fill_between(steps, lower_p2[:, vidx], upper_p2[:, vidx],
                            color=COLORS["extended"], alpha=0.08)
            ax.axhline(y=0, color=COLORS["zero"], linewidth=0.4, linestyle="--")
            ax.set_title(vname, fontsize=9, fontweight="bold")
            ax.set_xlabel("Months")
            if i % ncols == 0:
                ax.set_ylabel("Percentage points")
            if i == 0:
                ax.legend(fontsize=7, loc="upper right")

        for j in range(len(KEY_VARS), len(axes_flat)):
            axes_flat[j].set_visible(False)

        fig.suptitle("Response to Risk-off shock: unrestricted VAR, 1999-2021 versus 1999-2026",
                     fontsize=12, fontweight="bold", color=COLORS["text"], y=0.98)
        fig.text(0.5, 0.01, "Solid: 1999-2021. Dashed: 1999-2026. Shaded bands are 95% CIs.",
                 ha="center", fontsize=8, color=COLORS["muted"])
        plt.tight_layout(rect=[0, 0.02, 1, 0.95])
        fig.savefig(FIG_DIR / "irf_period_comparison_unrestricted.png", dpi=DPI, bbox_inches="tight")
        plt.close(fig)
        print("  Saved: irf_period_comparison_unrestricted.png")
    except Exception as e:
        print(f"  Period comparison failed: {e}")

    print(f"\nAll outputs saved to {OUT_DIR.resolve()}")
    print("Done.")


if __name__ == "__main__":
    main()
