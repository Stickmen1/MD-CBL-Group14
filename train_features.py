# train_features_final.py – Builds feature matrix used by train_model_final.py
# -------------------------------------------------------------------------
# 1. Load the tidy LSOA‑ (or Ward‑) month count file
# 2. Create calendar, lag and rolling features
# 3. Save as Parquet so downstream training is fast
#
# Run:  python train_features_final.py

from pathlib import Path
import pandas as pd

# ──────────────────────────────────────────────────────────────────────────
# 0. Paths  (stand‑alone, no imports from EDA.py needed)
# ──────────────────────────────────────────────────────────────────────────
DATA_DIR  = Path(r"C:\Users\20232369\OneDrive\Y2\Q4\DC2\MD-CBL-Group14\UK_police_data")
CACHE_DIR = DATA_DIR / "_cache"

# --->  If you changed the tidy CSV name, do it here  <---
TIDY_CSV  = CACHE_DIR / "ward_month_burglary_london.csv"   # or lsoa_month_burglary_london.csv

print("\n===  Building feature matrix  ===")

# ──────────────────────────────────────────────────────────────────────────
# 1. Load tidy table (ward/L‑SOA × month counts)
# ──────────────────────────────────────────────────────────────────────────
wm = pd.read_csv(TIDY_CSV, parse_dates=["month"])

# ──────────────────────────────────────────────────────────────────────────
# 2. Date & lag features
# ──────────────────────────────────────────────────────────────────────────
wm["year"]       = wm["month"].dt.year
wm["month_i"]    = wm["month"].dt.month                # 1‑12
wm["year_month"] = ((wm["month"].dt.year - wm["month"].dt.year.min())*12
                    + wm["month"].dt.month)

wm = wm.sort_values(["unit", "month"])

for lag in [1, 3, 6, 12]:
    wm[f"lag_{lag}"] = wm.groupby("unit")["burglary_cnt"].shift(lag)

wm["roll_3"] = (wm.groupby("unit")["burglary_cnt"].shift(1)
                               .rolling(3).mean()
                               .reset_index(level=0, drop=True))

feature_cols = ["year", "month_i", "year_month",
                "lag_1", "lag_3", "lag_6", "lag_12", "roll_3"]
wm_feat = wm.dropna(subset=feature_cols + ["burglary_cnt"]).reset_index(drop=True)

print("✅  Feature matrix ready →", wm_feat.shape)
print(wm_feat.head())

# ──────────────────────────────────────────────────────────────────────────
# 3. Persist for downstream modelling
# ──────────────────────────────────────────────────────────────────────────
OUT_PATH = CACHE_DIR / "features_burglary.parquet"
wm_feat.to_parquet(OUT_PATH, index=False)
print("✅  Saved features →", OUT_PATH)
