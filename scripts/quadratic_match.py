"""EViews-style quadratic-match average interpolation to trading-day grid."""

import pandas as pd
import numpy as np
import os

TMP_DIR = "data/tmp_quadratic"
OUT_DIR = f"{TMP_DIR}/v2"
FINAL_CSV = "data/processed/final_dataset.csv"

# Configure which native series to process: (path, value_col, freq)
SERIES = [
    ("log_reer_native.csv", "log_reer", "M"),
    ("debtsec_native.csv", "debtsec_pct", "M"),
    ("equity_native.csv", "equity_pct", "M"),
    ("other_native.csv", "other_pct", "M"),
    ("direct_native.csv", "direct_pct", "M"),
    ("log_rgdp_native.csv", "log_rgdp", "Q"),
    ("log_wui_native.csv", "log_wui", "Q"),
]


def _month_key(d):
    """Return (year, month) tuple for a date."""
    return (d.year, d.month)


def _quarter_key(d):
    """Return (year, quarter) tuple for a date."""
    return (d.year, (d.month - 1) // 3 + 1)


def _freq_key_fn(freq):
    return _month_key if freq == "M" else _quarter_key


def _period_keys(dates, key_fn):
    """Vectorized period key extraction for numpy datetime64 array."""
    dt = pd.DatetimeIndex(dates)
    if key_fn == _month_key:
        return list(zip(dt.year, dt.month))
    else:
        return list(zip(dt.year, ((dt.month - 1) // 3 + 1)))


def quadratic_match_average(dates_low, values_low, dates_high, freq):
    """
    EViews quadratic-match average interpolation.

    For each low-frequency observation, fits a local quadratic through the
    triplet of adjacent observations (previous, current, next) positioned
    at sequential integer indices. Evaluates at uniformly-spaced positions
    within the observation's calendar period, then additively shifts so the
    mean of interpolated values equals the source value. Discontinuities at
    period boundaries are expected.
    """
    dates_low = np.asarray(pd.to_datetime(dates_low))
    values_low = np.asarray(values_low, dtype=float)
    dates_high = np.asarray(pd.to_datetime(dates_high))

    key_fn = _freq_key_fn(freq)

    # Map each source observation to its period key and sequential index
    obs_periods = _period_keys(dates_low, key_fn)
    # Build sequential index: only non-NA observations in date order
    valid = ~np.isnan(values_low)
    obs_vals_arr = values_low[valid]
    obs_periods_list = [p for i, p in enumerate(obs_periods) if valid[i]]

    n_obs = len(obs_vals_arr)
    if n_obs < 3:
        raise ValueError("Need at least 3 valid source observations")

    # Build (period_key -> sequential_index) mapping
    period_to_seq = {}
    for idx, p in enumerate(obs_periods_list):
        period_to_seq[p] = idx

    # Map each HF date to its period key and sequential index of source obs
    hf_periods = _period_keys(dates_high, key_fn)
    hf_seq_idx = np.full(len(dates_high), -1, dtype=np.int64)
    for i, p in enumerate(hf_periods):
        if p in period_to_seq:
            hf_seq_idx[i] = period_to_seq[p]

    result = np.full(len(dates_high), np.nan)

    for k in range(n_obs):
        # Find HF dates belonging to this observation's period
        mask = hf_seq_idx == k
        n_hf = mask.sum()
        if n_hf == 0:
            continue

        y_t = obs_vals_arr[k]

        # Get triplet y_{k-1}, y_k, y_{k+1}
        if k == 0:
            # First observation: use first three
            y_prev, y_curr, y_next = obs_vals_arr[0], obs_vals_arr[1], obs_vals_arr[2]
        elif k == n_obs - 1:
            # Last observation: use last three
            y_prev, y_curr, y_next = obs_vals_arr[-3], obs_vals_arr[-2], obs_vals_arr[-1]
        else:
            y_prev, y_curr, y_next = (
                obs_vals_arr[k - 1],
                obs_vals_arr[k],
                obs_vals_arr[k + 1],
            )

        # Quadratic coefficients f(u) = a*u^2 + b*u + c
        # fitted through (-1, y_prev), (0, y_curr), (1, y_next)
        # Note: y_curr is at u=0, y_prev at u=-1, y_next at u=+1
        a_coef = (y_prev - 2 * y_curr + y_next) / 2.0
        b_coef = (y_next - y_prev) / 2.0
        c_coef = y_curr

        # Normalized positions for HF dates within period [-0.5, 0.5]
        i = np.arange(n_hf, dtype=float)
        u = (i + 0.5) / n_hf - 0.5

        # Evaluate quadratic
        f_vals = a_coef * u**2 + b_coef * u + c_coef

        # Mean-preserving shift so mean of interpolated values = source value
        mean_f = np.mean(f_vals)
        result[mask] = f_vals + (y_t - mean_f)

    return result


def process_one(native_path, value_col, freq, out_path):
    """Interpolate a single native-frequency variable to trading-day grid."""
    native = pd.read_csv(
        os.path.join(TMP_DIR, native_path), parse_dates=["date"]
    )

    # Restrict to anchors >= 1998-01-01 to avoid early sparse data
    native = native[native["date"] >= "1998-01-01"].copy()
    native = native.dropna(subset=[value_col])

    # Load trading-day grid from final dataset
    final = pd.read_csv(FINAL_CSV, parse_dates=["date"])
    dates_high = final["date"].values

    values = quadratic_match_average(
        native["date"].values,
        native[value_col].values,
        dates_high,
        freq=freq,
    )

    out = pd.DataFrame({"date": dates_high, value_col: values})
    out.to_csv(out_path, index=False)
    return out


def validate_mean_preservation(out, native_path, value_col, freq):
    """Check mean of interpolated HF values within each period matches source."""
    native = pd.read_csv(
        os.path.join(TMP_DIR, native_path), parse_dates=["date"]
    )
    native = native[native["date"] >= "1998-01-01"].copy()
    native = native.dropna(subset=[value_col])

    key_fn = _freq_key_fn(freq)
    out_periods_list = _period_keys(out["date"].values, key_fn)
    native_periods_list = _period_keys(native["date"].values, key_fn)

    # Build native period -> value dict
    native_dict = {}
    for p, v in zip(native_periods_list, native[value_col].values):
        native_dict[p] = v

    passes = 0
    fails = 0
    checked = 0

    for p, native_val in native_dict.items():
        mask = [k == p for k in out_periods_list]
        n_hf = sum(mask)
        if n_hf == 0:
            continue
        masked_vals = out.loc[mask, value_col]
        if masked_vals.isna().all():
            continue
        mean_val = masked_vals.mean(skipna=True)
        diff = abs(mean_val - native_val)
        checked += 1
        if diff < 1e-8:
            passes += 1
        else:
            fails += 1
            print(
                f"  FAIL period {p}: source={native_val:.10f}, "
                f"mean={mean_val:.10f}, diff={diff:.2e}"
            )

    print(f"  Mean preservation: {passes}/{checked} passed, {fails} failed")
    return passes, fails, checked


def validate_boundary_jumps(out, value_col):
    """Report max abs diffs at period boundaries vs within periods."""
    vals = out[value_col].values
    is_valid = ~np.isnan(vals)
    # Only compute diffs where both adjacent values are valid
    valid_pair = is_valid[1:] & is_valid[:-1]
    diffs = np.full(len(vals) - 1, np.nan)
    diffs[valid_pair] = np.abs(np.diff(vals)[valid_pair])

    dates = pd.DatetimeIndex(pd.to_datetime(out["date"]))
    years = dates.year.to_numpy()
    months = dates.month.to_numpy()
    same_month = (years[1:] == years[:-1]) & (months[1:] == months[:-1])

    boundary_diffs = diffs[(~same_month) & ~np.isnan(diffs)]
    within_diffs = diffs[same_month & ~np.isnan(diffs)]

    if len(boundary_diffs) > 0:
        print(
            f"  Boundary jumps: mean={boundary_diffs.mean():.6e}, "
            f"max={boundary_diffs.max():.6e}, count={len(boundary_diffs)}"
        )
    if len(within_diffs) > 0:
        print(
            f"  Within-period diffs: mean={within_diffs.mean():.6e}, "
            f"max={within_diffs.max():.6e}, count={len(within_diffs)}"
        )
    if len(boundary_diffs) > 0 and len(within_diffs) > 0:
        ratio = boundary_diffs.max() / (within_diffs.max() + 1e-300)
        print(f"  Max boundary/within ratio: {ratio:.4f}")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    for native_name, value_col, freq in SERIES:
        stem = native_name.replace("_native.csv", "")
        out_name = f"{stem}_qdmatch.csv"
        out_path = os.path.join(OUT_DIR, out_name)

        print(f"\n{'='*60}")
        print(f"Processing: {native_name} -> {out_name}")
        print(f"{'='*60}")

        out = process_one(native_name, value_col, freq, out_path)

        print(f"  Output: {out_path}")
        print(f"  Shape: {out.shape}")
        print(f"  Non-NA: {out[value_col].notna().sum()} / {len(out)}")
        print(f"  Head:")
        for _, r in out.head(5).iterrows():
            v = r[value_col]
            v_str = f"{v:.8f}" if pd.notna(v) else "NA"
            print(f"    {pd.Timestamp(r['date']).strftime('%Y-%m-%d')}  {v_str}")
        print(f"  Tail:")
        for _, r in out.tail(5).iterrows():
            v = r[value_col]
            v_str = f"{v:.8f}" if pd.notna(v) else "NA"
            print(f"    {pd.Timestamp(r['date']).strftime('%Y-%m-%d')}  {v_str}")
        print(f"  Summary stats:")
        print(f"    mean={out[value_col].mean(skipna=True):.8f}, "
              f"std={out[value_col].std(skipna=True):.8f}, "
              f"min={out[value_col].min(skipna=True):.8f}, "
              f"max={out[value_col].max(skipna=True):.8f}")

        passes, fails, checked = validate_mean_preservation(
            out, native_name, value_col, freq
        )
        validate_boundary_jumps(out, value_col)

        if fails > 0:
            print(f"  WARNING: {fails} mean-preservation failures")
        else:
            print(f"  All mean-preservation checks passed")


if __name__ == "__main__":
    main()
