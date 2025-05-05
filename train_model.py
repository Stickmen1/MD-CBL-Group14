"""
burglary_allocation_engine_fixed.py

Adapted to integrate directly with preloaded DataFrames (e.g., bur_lon and sas),
avoiding any CLI or filesystem search. Writes weekly patrol schedule for each LSOA.
"""

from __future__ import annotations

import calendar, datetime as dt, math, random
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd

# Constants – same as before
WEEKDAY_SHARE = 0.70
WEEKEND_SHARE = 0.30
DAY_SHARE = 0.40
NIGHT_SHARE = 0.60

BASE_SLOT_WEIGHTS = np.array([DAY_SHARE / 6] * 6 + [NIGHT_SHARE / 12] * 2)
SLOT_LABELS = [f"{6+i*2:02d}-{8+i*2:02d}" for i in range(8)]

NEAR_REPEAT_DECAY = [1.00, 0.70, 0.50, 0.35, 0.25, 0.18, 0.12, 0.08, 0.06, 0.04, 0.03, 0.02, 0.015, 0.01]

OFFICER_SPLIT = {
    "high_visibility": 80,
    "cocooning_van": 10,
    "plain_clothes": 10,
}
TOTAL_OFFICERS = 100
assert sum(OFFICER_SPLIT.values()) == TOTAL_OFFICERS

GRID_SIZE_M = 250
TOP_GRID_N = 3

EARTH_R = 6_371_000

# Core functions unchanged, but CLI removed and integration enabled

def build_slot_weights(sas_df: pd.DataFrame) -> np.ndarray:
    sas_df = sas_df.copy()
    sas_df["datetime"] = pd.to_datetime(sas_df["Date"], errors="coerce")
    sas_df = sas_df.dropna(subset=["datetime"])
    sas_df["slot"] = sas_df["datetime"].dt.hour.apply(lambda h: (h - 6) // 2 if 6 <= h < 22 else np.nan)
    activity = sas_df.groupby("slot").size().reindex(range(8), fill_value=0).to_numpy()
    activity_norm = np.where(activity > 0, activity / activity.mean(), 1.0)
    weights = BASE_SLOT_WEIGHTS * activity_norm
    return weights / weights.sum()

def day_weights() -> np.ndarray:
    return np.array([WEEKDAY_SHARE / 5] * 5 + [WEEKEND_SHARE / 2] * 2)

def monte_carlo_disaggregate(unit, month_ts, n_events, slot_weights, n_draws):
    y, m = month_ts.year, month_ts.month
    _, ndays = calendar.monthrange(y, m)
    dates = [dt.date(y, m, d) for d in range(1, ndays + 1)]
    d_weights = day_weights()
    date_probs = np.array([d_weights[d.weekday()] for d in dates])
    date_probs = date_probs / date_probs.sum()

    draws = n_events * n_draws
    picked_dates = random.choices(dates, weights=date_probs, k=draws)
    picked_slots = random.choices(range(8), weights=slot_weights, k=draws)

    times = [
        dt.datetime.combine(d, dt.time.min) + dt.timedelta(hours=6 + s * 2, minutes=random.randint(0, 119))
        for d, s in zip(picked_dates, picked_slots)
    ]
    return pd.DataFrame({
        "unit": unit,
        "timestamp": times,
        "slot": picked_slots,
        "dow": [t.weekday() for t in times],
    })

def expected_matrix(sim_df: pd.DataFrame, n_draws: int) -> pd.DataFrame:
    mat = sim_df.groupby(["dow", "slot"]).size().unstack(fill_value=0) / n_draws
    mat.index = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    mat.columns = SLOT_LABELS
    return mat

def pick_top_four(mat: pd.DataFrame) -> List[Tuple[int, int]]:
    picks = []
    flat = (
        mat.stack()
        .reset_index()
        .rename(columns={"level_0": "dow", "level_1": "slot", 0: "risk"})
        .sort_values("risk", ascending=False)
    )
    for _, row in flat.iterrows():
        d, s = row["dow"], row["slot"]
        if (d, s) in picks:
            continue
        wd_count = sum(1 for d0, _ in picks if d0 < 5)
        we_count = len(picks) - wd_count
        if d < 5 and wd_count >= 2:
            continue
        if d >= 5 and we_count >= 2:
            continue
        picks.append((d, s))
        if len(picks) == 4:
            break
    return picks

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * EARTH_R * np.arcsin(np.sqrt(a))

def make_micro_grids(df: pd.DataFrame, grid_size_m=GRID_SIZE_M):
    if df.empty:
        return []
    lat_grid = (df["Latitude"] * 111_320).round(-int(math.log10(grid_size_m)))
    lon_grid = (
        df["Longitude"].mul(np.cos(np.radians(df["Latitude"].mean()))) * 111_320
    ).round(-int(math.log10(grid_size_m)))
    counts = (
        df.groupby([lat_grid, lon_grid]).size().sort_values(ascending=False).head(TOP_GRID_N)
    )
    centers = []
    for (latm, lonm), _ in counts.items():
        lat_c = latm / 111_320
        lon_c = lonm / (111_320 * np.cos(np.radians(lat_c)))
        centers.append((lat_c, lon_c))
    return centers

# ─────────────────────────────────────────────────────────────────────────────
# 🚀 Public function to call with your preloaded data
# ─────────────────────────────────────────────────────────────────────────────

def run_burglary_schedule(
    bur_df: pd.DataFrame,
    sas_df: pd.DataFrame,
    month: str,
    unit_col: str = "LSOA code",
    n_draws: int = 100,
    output_path: Path = Path("weekly_schedule.csv")
) -> pd.DataFrame:
    slot_weights = build_slot_weights(sas_df)

    burg_df = bur_df.copy()
    burg_df = burg_df[burg_df["Crime type"].str.contains("burglary", case=False, na=False)]
    burg_df = burg_df.rename(columns={unit_col: "unit"})

    if "Month" not in burg_df.columns:
        burg_df["Month"] = pd.to_datetime(burg_df["month"])

    agg = burg_df.groupby(["unit", "Month"]).size().reset_index(name="count")

    weekly_rows = []
    for unit, sub in agg.groupby("unit"):
        sims = []
        for _, row in sub.iterrows():
            sims.append(
                monte_carlo_disaggregate(
                    unit, row["Month"], int(row["count"]), slot_weights, n_draws
                )
            )
        if not sims:
            continue
        sims_df = pd.concat(sims, ignore_index=True)
        mat = expected_matrix(sims_df, n_draws)
        picks = pick_top_four(mat)
        unit_burgs = burg_df[burg_df["unit"] == unit]
        grids = make_micro_grids(unit_burgs)
        for dow, slot in picks:
            weekly_rows.append({
                "unit": unit,
                "dow": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dow],
                "slot": SLOT_LABELS[slot],
                "high_visibility": OFFICER_SPLIT["high_visibility"],
                "cocooning_van": OFFICER_SPLIT["cocooning_van"],
                "plain_clothes": OFFICER_SPLIT["plain_clothes"],
                "grid_centers": grids,
            })

    schedule = pd.DataFrame(weekly_rows)
    schedule = schedule.sort_values(["unit", "dow", "slot"])
    schedule.to_csv(output_path, index=False)
    print(f"✅  Weekly schedule saved to: {output_path} (rows: {len(schedule):,})")
    return schedule
