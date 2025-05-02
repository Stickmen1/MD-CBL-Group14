import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

wards = gpd.read_file("esri/London_Ward_CityMerged.shp")

# Optional preview ward shapes
# wards.plot()
# plt.show()

crimes = pd.read_csv("UK_police_data/2024-04/2024-04-metropolitan-street.csv")
# Filter only residential burglaries (optional if not done during download)
crimes = crimes[crimes["Crime type"] == "Burglary"]

#convert to geodataframe
geometry = [Point(xy) for xy in zip(crimes["Longitude"], crimes["Latitude"])]
crimes_gdf = gpd.GeoDataFrame(crimes, geometry=geometry, crs="EPSG:4326")

#peproject to match ward shapefile CRS
crimes_gdf = crimes_gdf.to_crs(wards.crs)

#join by attaching ward info to each crime
joined = gpd.sjoin(crimes_gdf, wards, how="inner", predicate="intersects")

#Time freature -> adds "Month" to datetime and extract additional info
joined["Month"] = pd.to_datetime(joined["Month"])
joined["Month_Period"] = joined["Month"].dt.to_period("M")
joined["Year"] = joined["Month"].dt.year
joined["Season"] = joined["Month"].dt.month % 12 // 3 + 1  # Seasons (1=winter, 2=spring ... 4=autumn)

# TODO: Add holiday/weekend features if needed

#aggregation by ward and month
monthly_ward = joined.groupby(["NAME", "Month_Period"]).size().reset_index(name="Burglary_Count")

#vis boundaries in one month specified above
# Select month
selected_month = "2024-04"
map_data = monthly_ward[monthly_ward["Month_Period"] == selected_month]

#merge with geometry to visualize
wards_with_data = wards.merge(map_data, on="NAME", how="left")

#plot choropleth map
wards_with_data.plot(column="Burglary_Count", cmap="OrRd", legend=True, edgecolor="black")
plt.title(f"Residential Burglaries per Ward – {selected_month}")
plt.axis("off")
plt.tight_layout()
plt.show()

# ======================================
# 9. TODO: Add Socioeconomic Data
# ======================================
# Join IMD or other deprivation data per LSOA/ward here
# Example: deprivation = pd.read_csv("imd_data.csv") → join on NAME or LSOA

# ======================================
# 10. EXPORT OR CONTINUE TO FORECASTING
# ======================================
# monthly_ward.to_csv("output/monthly_burglary_counts.csv", index=False)
