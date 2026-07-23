"""Fetch JPNRGDPEXP vintage data from the FRED/ALFRED graph API."""

import json
import gzip
import csv
import datetime
import urllib.request
import urllib.error
import os
import sys


API_BASE = "https://fred.stlouisfed.org/graph/api"
SERIES_ID = "JPNRGDPEXP"
VINTAGES = ["2021-06-01", "2022-01-01"]
OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "raw", "vintage",
)


def _filter_notes(obj):
    """Strip 'notes' keys from the chart state (required by the API)."""
    if isinstance(obj, dict):
        return {k: _filter_notes(v) for k, v in obj.items() if k != "notes"}
    if isinstance(obj, list):
        return [_filter_notes(v) for v in obj]
    return obj


def _decompress(data):
    if data[:2] == b"\x1f\x8b":
        return gzip.decompress(data)
    return data


def fetch_initial_payload(series_id, mode, vintage_date=None):
    """Get the chart metadata — required before fetching observations."""
    url = f"{API_BASE}/series/?id={series_id}&width=800&mode={mode}"
    if vintage_date:
        url += f"&vintage_date={vintage_date}"
    req = urllib.request.Request(url, headers={
        "Accept-Encoding": "gzip, deflate",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        parsed = json.loads(_decompress(resp.read()))
    chart_state = {
        "chart": parsed["chart"],
        "seriesObjects": parsed["chart_series"],
    }
    return _filter_notes(chart_state)


def fetch_observations(series_id, chart_state):
    """Post the chart state to retrieve observation data."""
    body = json.dumps(chart_state, separators=(",", ":"))
    url = f"{API_BASE}/series/?obs=true&sid={series_id}"
    req = urllib.request.Request(
        url, data=body.encode("utf-8"), headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
        }, method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        parsed = json.loads(_decompress(resp.read()))
    obs_groups = parsed.get("observations", [])
    if not obs_groups:
        return {}
    result = {}
    for ts_ms, val in obs_groups[0]:
        dt = datetime.datetime.fromtimestamp(ts_ms / 1000, datetime.UTC)
        result[dt.strftime("%Y-%m-%d")] = val
    return result


def fetch_vintage(series_id, vintage_date):
    """Fetch a single vintage using the two-step ALFRED API."""
    state = fetch_initial_payload(series_id, "alfred", vintage_date)
    return fetch_observations(series_id, state)


def save_csv(filepath, observations):
    """Write date,rgdp CSV sorted by date."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "rgdp"])
        for d in sorted(observations.keys()):
            writer.writerow([d, observations[d]])


def main():
    for vintage in VINTAGES:
        out_path = os.path.join(
            OUTPUT_DIR, f"{SERIES_ID}_vintage_{vintage}.csv"
        )
        print(f"Fetching {SERIES_ID} as of {vintage} ...", end=" ", flush=True)
        try:
            obs = fetch_vintage(SERIES_ID, vintage)
            if not obs:
                print(f"FAILED: no observations returned")
                continue
            save_csv(out_path, obs)
            dates = sorted(obs.keys())
            print(
                f"OK — {len(obs)} obs, "
                f"{dates[0]} to {dates[-1]}"
            )
        except urllib.error.HTTPError as e:
            print(f"HTTP {e.code}: {e.reason}")
        except Exception as e:
            print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
