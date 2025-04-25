
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
    street = load_dataset("street")
    outcomes = load_dataset("outcomes")
    searches = load_dataset("stop-and-search")

    overview(street, "Street")
    overview(outcomes, "Outcomes")
    overview(searches, "Stop & Search")

    describe_categoricals(
        street,
        cat_cols=["Crime type", "Last outcome category", "LSOA name", "Reported by"],
    )
    describe_categoricals(
        searches,
        cat_cols=["Legislation", "Outcome", "Object of search", "Gender"],
    )

    plot_time_series(street, col="Crime type", title="Crime type trends (street)")
    plot_time_series(searches, col="Outcome", title="Search outcomes (relative)", relative=True)

    # ── New: interactive map of crime locations (street data) ──
    if _FOLIUM_OK:
        plot_map(street, outfile="crime_map.html", sample=7000)


