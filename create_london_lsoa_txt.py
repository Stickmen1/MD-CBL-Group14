"""
Build london_lsoa.txt from the 2021 boundary CSV you downloaded.

✱ Point CSV_PATH at your file (leave the r-prefix so back-slashes are OK).
✱ Run once:  python create_london_lsoa_from_csv.py
✱ Result:    london_lsoa.txt  (~5 000 lines) in the working folder.
"""

from pathlib import Path
import re
import pandas as pd

# ── ①  Location of the file you said you downloaded ──────────────────────────
CSV_PATH = Path(
    r"C:\Users\20232369\OneDrive\Y2\Q4\DC2\MD-CBL-Group14\LSOA_data"
    r"\Lower_layer_Super_Output_Areas_(December_2021)_Boundaries_EW_BFE_(V10)_and_RUC.csv"
)
if not CSV_PATH.exists():
    raise FileNotFoundError(f"CSV not found – fix CSV_PATH:\n{CSV_PATH}")

# ── ②  Read just what we need (LSOA code + name) ─────────────────────────────
use_cols = ["LSOA21CD", "LSOA21NM"]     # code, name (contains borough)
df = pd.read_csv(CSV_PATH, usecols=use_cols, dtype=str)

# ── ③  Extract the borough name from `LSOA21NM` ──────────────────────────────
# e.g.  "Barking and Dagenham 016A"  ->  "Barking and Dagenham"
def borough_from_name(txt: str) -> str:
    return re.sub(r"\s\d{3}[A-Z]?$", "", txt)   # strip " 016A" suffix

df["borough"] = df["LSOA21NM"].map(borough_from_name)

LONDON_BOROUGHS = {
    "Barking and Dagenham", "Barnet", "Bexley", "Brent", "Bromley", "Camden",
    "Croydon", "Ealing", "Enfield", "Greenwich", "Hackney",
    "Hammersmith and Fulham", "Haringey", "Harrow", "Havering", "Hillingdon",
    "Hounslow", "Islington", "Kensington and Chelsea", "Kingston upon Thames",
    "Lambeth", "Lewisham", "Merton", "Newham", "Redbridge",
    "Richmond upon Thames", "Southwark", "Sutton", "Tower Hamlets",
    "Waltham Forest", "Wandsworth", "Westminster", "City of London",
}

london_codes = (
    df[df["borough"].isin(LONDON_BOROUGHS)]["LSOA21CD"]
    .dropna()
    .unique()
)

# ── ④  Write the whitelist ───────────────────────────────────────────────────
OUT = Path("london_lsoa.txt")
OUT.write_text("\n".join(sorted(london_codes)))
print(f"🎉  Wrote {len(london_codes):,} codes → {OUT.resolve()}")
