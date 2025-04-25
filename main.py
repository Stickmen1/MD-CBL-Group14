#Prerequirement - pip install geopandas shapely
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt

#data loading
wards = gpd.read_file("esri/London_Ward_CityMerged.shp")
date = "2024-11"
crimes = pd.read_csv("UK_police_data/2024-11/2024-11-metropolitan-street.csv")
print(wards.head())

#converting to GeoDataFrame
geometry = [Point(xy) for xy in zip(crimes["Longitude"], crimes["Latitude"])]
crimes_gdf = gpd.GeoDataFrame(crimes, geometry=geometry, crs="EPSG:4326")

#spacial join
crimes_gdf = crimes_gdf.to_crs(wards.crs)
joined = gpd.sjoin(crimes_gdf, wards, how="inner", predicate="intersects")

joined["Month"] = pd.to_datetime(joined["Month"]).dt.to_period("M")
monthly_ward = joined.groupby(["NAME", "Month"]).size().reset_index(name="Burglary_Count")

#plotting
wards.plot()
plt.show()

map_data = monthly_ward[monthly_ward["Month"] == date]
wards_with_data = wards.merge(map_data, on="NAME")

wards_with_data.plot(column="Burglary_Count", cmap="OrRd", legend=True, edgecolor="black")
plt.title("Residential Burglary per Ward in London" + date)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
