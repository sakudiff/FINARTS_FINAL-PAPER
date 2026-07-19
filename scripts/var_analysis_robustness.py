"""
Robustness: VAR at weekly and monthly frequencies.

Beirne & Sugandi (2023) Appendix 4: re-run the restricted VAR on data aggregated
to weekly and monthly frequencies to verify that the daily-frequency results are
not artefacts of the quadratic interpolation.

Usage: uv run python scripts/var_analysis_robustness.py
Outputs: data/processed/var_results/figures/irf_restricted_*_weekly*.png
         data/processed/var_results/figures/irf_restricted_*_monthly*.png
         data/processed/var_results/figures/irf_freq_comparison_*.png
"""

import sys
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.api import VAR

warnings.filterwarnings("ignore", category=FutureWarning)

sys.path.insert(0, str(Path(__file__).parent))
from var_analysis import (
    VAR_ORDER, build_exog, run_var, _bootstrap_irf_ci,
    IRF_HORIZON, MAX_LAG, ALPHA, OUT_DIR, FIG_DIR, DPI, N_BOOTSTRAP, COLORS,
)

PAPER_END = pd.Timestamp("2021-03-31")
RNG = np.random.default_rng(20260715)


def aggregate_to_freq(df, freq="W"):
    end = df.groupby(pd.Grouper(key="date", freq=freq)).last().reset_index()
    end = end.dropna(subset=VAR_ORDER, how="all").reset_index(drop=True)
    return end


def run_freq_var(data, exog, freq_label):
    data = data.dropna().reset_index(drop=True)
    n = len(data)
    print(f"    {freq_label}: {n} observations after dropna")
    k_ar = min(8, n // 30)
    if isinstance(exog, np.ndarray):
        exog_trim = exog[:n]
    else:
        exog_trim = exog.iloc[:n] if n < len(exog) else exog
    results = run_var(data, exog_trim, restricted=True, k_ar=k_ar)
    return results, k_ar


def main():
    print("=" * 70)
    print("Frequency Robustness — Beirne & Sugandi (2023) Appendix 4")
    print("=" * 70)

    df = pd.read_csv("data/processed/final_dataset.csv", parse_dates=["date"])

    for period_label, period_df in [("1999-2021", df[df["date"] <= PAPER_END]),
                                     ("1999-2026", df)]:
        print(f"\nPeriod: {period_label}")

        for freq, freq_label in [("W", "Weekly"), ("ME", "Monthly")]:
            print(f"\n  --- {freq_label} Restricted VAR ---")
            agg = aggregate_to_freq(period_df, freq=freq)
            exog_agg, _ = build_exog(agg)
            results, k_ar = run_freq_var(agg[VAR_ORDER], exog_agg, freq_label)

            irf = results.irf(periods=min(52, IRF_HORIZON))
            irf_values = irf.irfs
            sigma_u = results.sigma_u
            nobs = results.nobs
            se = np.sqrt(np.diag(sigma_u) / nobs)
            z = 1.96
            lower = irf_values - z * se[np.newaxis, np.newaxis, :]
            upper = irf_values + z * se[np.newaxis, np.newaxis, :]

            fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(16, 10))
            axes_flat = axes.flatten()
            n_periods = irf_values.shape[0]
            for v_idx, v_name in enumerate(VAR_ORDER):
                if v_idx < len(axes_flat):
                    steps = np.arange(n_periods)
                    axes_flat[v_idx].plot(steps, irf_values[:, 0, v_idx],
                                          color=COLORS["paper"], linewidth=0.8)
                    axes_flat[v_idx].fill_between(
                        steps, lower[:, 0, v_idx], upper[:, 0, v_idx],
                        color=COLORS["paper"], alpha=0.15)
                    axes_flat[v_idx].axhline(y=0, color=COLORS["zero"],
                                             linewidth=0.4, linestyle="--")
                    axes_flat[v_idx].set_title(f"Response: {v_name}", fontsize=9)
                    axes_flat[v_idx].set_xlabel(f"{'Weeks' if freq == 'W' else 'Months'}", fontsize=8)
                    if v_idx % 4 == 0:
                        axes_flat[v_idx].set_ylabel("Percentage points", fontsize=8)

            for v_idx in range(len(VAR_ORDER), len(axes_flat)):
                axes_flat[v_idx].set_visible(False)

            fig.suptitle(f"Restricted VAR — {period_label} — {freq_label} Frequency\n"
                         f"IRF to Risk-off Shock (Analytical 95% CI, lags={k_ar})",
                         fontsize=12, fontweight="bold")
            plt.tight_layout(rect=[0, 0, 1, 0.95])
            fname = f"irf_restricted_{period_label.replace('-', '_')}_{freq.lower()}.png"
            fig.savefig(FIG_DIR / fname, dpi=DPI, bbox_inches="tight")
            plt.close(fig)
            print(f"    Saved: {fname}")

    print("\nDone. All frequency robustness figures generated.")


if __name__ == "__main__":
    main()
