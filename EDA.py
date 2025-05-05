from __future__ import annotations

import re
import importlib
from pathlib import Path
from typing import Iterable

import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("default")  # keep matplotlib dependency‑free
#local path because relative wasn't working just change this at your own desire
DATA_DIR = Path(r"C:\Users\20232369\OneDrive\Y2\Q4\DC2\MD-CBL-Group14\UK_police_data")

if not DATA_DIR.exists():
    raise FileNotFoundError(f"DATA_DIR '{DATA_DIR}' does not exist – double‑check the path.")

CACHE_DIR = DATA_DIR / "_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

_PARQUET_OK = any(importlib.util.find_spec(p) is not None for p in ("pyarrow", "fastparquet"))
_FOLIUM_OK = importlib.util.find_spec("folium") is not None
if not _FOLIUM_OK:
    print("[Info] folium not found – map plotting disabled.  pip install folium  to enable.")

def _parse_month_from_fname(fname: str) -> str | None:
    m = re.search(r"(\d{4}-\d{2})", fname)
    return m.group(1) if m else None


def _find_files(dataset_type: str) -> Iterable[Path]:
    return DATA_DIR.rglob(f"*-{dataset_type}.csv")


def load_dataset(dataset_type: str, force_reload: bool = False) -> pd.DataFrame:
    if dataset_type not in {"street", "outcomes", "stop-and-search"}:
        raise ValueError("dataset_type must be 'street', 'outcomes' or 'stop-and-search'")

    cache_path = CACHE_DIR / f"all_{dataset_type}.parquet"
    if _PARQUET_OK and cache_path.exists() and not force_reload:
        return pd.read_parquet(cache_path)

    files = sorted(_find_files(dataset_type))
    if not files:
        raise FileNotFoundError(
            f"No '*-{dataset_type}.csv' files found under {DATA_DIR} (searched recursively)"
        )

    frames = []
    for f in files:
        df = pd.read_csv(f)
        df["source_file"] = f.relative_to(DATA_DIR).as_posix()
        df["month"] = _parse_month_from_fname(f.name)
        frames.append(df)

    big = pd.concat(frames, ignore_index=True, copy=False)

    if _PARQUET_OK:
        big.to_parquet(cache_path, index=False)
    else:
        print("[Info] pyarrow / fastparquet not found – skipping Parquet cache.")

    return big

def focus_on_london_burglary(
    street_df: pd.DataFrame,
    lsoa_file: Path | None = DATA_DIR / "london_lsoa.txt",
    bbox_filter: bool = True,
) -> pd.DataFrame:
    """Return Street dataframe filtered to London residential burglary only."""
    # 1) crime type
    bur = street_df[street_df["Crime type"].str.contains("burglary", case=False)].copy()

    # 2) spatial filter ─────────────
    # 2a) lat/lon bounding box (fast)
    if bbox_filter:
        from london_boundry import LON_MIN, LON_MAX, LAT_MIN, LAT_MAX
        bur = bur[
            bur["Longitude"].between(LON_MIN, LON_MAX)
            & bur["Latitude"].between(LAT_MIN, LAT_MAX)
        ]

    # 2b) LSOA whitelist (precise)
    if lsoa_file and Path(lsoa_file).exists():
        london_lsoas = set(Path(lsoa_file).read_text().splitlines())
        bur = bur[bur["LSOA code"].isin(london_lsoas)]

    # 3) tidy date
    bur["month"] = pd.to_datetime(bur["month"]).dt.to_period("M").dt.to_timestamp()
    return bur


def make_unit_month(bur: pd.DataFrame) -> pd.DataFrame:
    """Aggregate to LSOA × Month count (use when 'Ward' column is missing)."""
    out = (
        bur.groupby(["LSOA code", "month"], dropna=False)
           .size()
           .rename("burglary_cnt")
           .reset_index()
           .rename(columns={"LSOA code": "unit"})   # neutral name
    )
    return out


def overview(df: pd.DataFrame, name: str):
    print("\n" + "═" * 80)
    print(f"Overview – {name}  |  rows: {df.shape[0]:,}  cols: {df.shape[1]}")
    df.info(max_cols=0, show_counts=True)

    na_pct = df.isna().mean().mul(100).sort_values(ascending=False)
    print("\nMissing values (top 10):\n", na_pct.head(10).round(1).to_string())


def describe_categoricals(df: pd.DataFrame, cat_cols: list[str], top_n: int = 10):
    for col in cat_cols:
        if col in df.columns:
            print("\n" + "─" * 80)
            print(f"{col} – top {top_n}")
            print(df[col].value_counts(dropna=False).head(top_n).to_string())

def plot_time_series(df: pd.DataFrame, col: str, title: str | None = None, relative: bool = False):
    if "month" not in df.columns:
        raise KeyError("DataFrame must contain a 'month' column from load_dataset()")

    monthly = df.groupby(["month", col], dropna=False).size().unstack(fill_value=0).sort_index()
    if relative:
        monthly = monthly.div(monthly.sum(axis=1), axis=0)

    monthly.plot(figsize=(10, 6))
    plt.title(title or f"Monthly counts by {col}")
    plt.xlabel("Month")
    plt.ylabel("Proportion" if relative else "Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

# Map helper ------------------------------------------------------------------
if _FOLIUM_OK:
    import folium  # type: ignore

    def plot_map(df: pd.DataFrame, outfile: str = "crime_map.html", sample: int | None = 5000):
        """Create an interactive Folium map of crime points.

        Parameters
        ----------
        df : DataFrame
            Must contain **Latitude**, **Longitude**, and **Crime type** columns.
        outfile : str
            HTML file name to write (it is opened in the system browser).
        sample : int | None
            Number of points to plot (random sample).  None = all points.
        """
        geo = df.dropna(subset=["Latitude", "Longitude"]).copy()
        if sample and len(geo) > sample:
            geo = geo.sample(sample, random_state=42)

        center = [geo["Latitude"].mean(), geo["Longitude"].mean()]
        m = folium.Map(location=center, zoom_start=11, tiles="cartodbpositron")

        for _, row in geo.iterrows():
            folium.CircleMarker(
                location=(row["Latitude"], row["Longitude"]),
                radius=3,
                popup=f"{row['Crime type']}<br>{row.get('Location', '')}",
                fill=True,
                fill_opacity=0.6,
                weight=0,
            ).add_to(m)

        m.save(outfile)
        print(f"Map saved to {outfile} – it should open automatically.")
        try:
            import webbrowser
            webbrowser.open(outfile)
        except Exception:
            pass

else:
    def plot_map(*args, **kwargs):  # type: ignore
        raise ImportError("folium is required for plot_map – pip install folium")


if __name__ == "__main__":
    # 0  load raw street table (cached)
    street = load_dataset("street")

    # 1  keep London residential burglary only
    bur_lon = focus_on_london_burglary(
    street_df=street,
    lsoa_file=Path("london_lsoa.txt"),         # ← new whitelist
    bbox_filter=True,                          # quick geo guard
)
    overview(bur_lon, "London Residential Burglary")

    # 2  aggregate → Ward × Month counts
    wm = make_unit_month(bur_lon)
    overview(wm, "Ward-Month table")

    # 3  tiny sanity visual
    plot_time_series(
    wm,
    col="unit",                       # <- the column created in make_unit_month()
    title="Burglary totals per LSOA",
    relative=False,
)


    # 4  (save for modelling later)
    wm.to_csv(CACHE_DIR / "ward_month_burglary_london.csv", index=False)
    print("✅  Saved ward-month table →", CACHE_DIR / "ward_month_burglary_london.csv")
