# This file requires data of roads and LSOA's
# Find road data here (the GeoPackage file): https://www.data.gov.uk/dataset/65bf62c8-eae0-4475-9c16-a2e81afcbdb0/os-open-roads1
# Find LSOA data here (the one that says 'Contains LSOA 2021 boundaries grouped by Boroughs'): https://data.london.gov.uk/dataset/statistical-gis-boundary-files-london

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import os
from shapely.geometry import box


def get_london_roads(path_to_uk_road_file: str = 'datasets/uk_road.gpkg'):
    # Rough bounding box for Greater London (WGS84 coordinates)
    london_bbox = box(-0.5103, 51.2868, 0.3340, 51.6919)  # (minx, miny, maxx, maxy)

    # Convert to GeoDataFrame
    bbox_gdf = gpd.GeoDataFrame({'geometry': [london_bbox]}, crs="EPSG:4326")

    print("Reading road nodes...")
    road_links = gpd.read_file("datasets/uk_road.gpkg", layer="road_node")
    print("Done reading. Reprojecting...")

    road_links = road_links.to_crs("EPSG:4326")
    print("Done reprojecting. Clipping to London...")

    london_roads = gpd.clip(road_links, bbox_gdf)
    print("Clipping done.")

    london_roads.to_file("datasets/london_road_nodes_only.gpkg", layer="road_node", driver="GPKG")


london_roads = gpd.read_file('datasets/london_road_links_only.gpkg')


def get_lsoa_geodata(lsoa_folder: str = "datasets/lsoa_boundaries/") -> gpd.GeoDataFrame:
    # Folder where you downloaded all borough LSOA files
    folder_path = lsoa_folder

    # List all files (e.g. all shapefiles or GeoJSONs)
    files = [f for f in os.listdir(folder_path) if f.endswith('.shp')]  # or '.shp'

    # Read and concatenate all files
    lsoa_list = []
    for file in files:
        print(f"Loading {file}...")
        gdf = gpd.read_file(os.path.join(folder_path, file))
        lsoa_list.append(gdf)

    # Combine into one GeoDataFrame
    lsoa_all = gpd.GeoDataFrame(pd.concat(lsoa_list, ignore_index=True))

    return lsoa_all


# To see intermediate plots, uncomment the respective lines
lsoa_data = get_lsoa_geodata()

# lsoa_data.plot()
# plt.show()

london_roads = london_roads.to_crs(lsoa_data.crs)

roads_with_lsoa = gpd.sjoin(london_roads, lsoa_data, how="left", predicate="intersects")

# roads_with_lsoa.plot(markersize=5, color='red')
# plt.show()

# # Plot the new map
# fig, ax = plt.subplots(figsize=(12, 12))

# # Plot road links on top
# london_roads.plot(ax=ax, color='red', linewidth=0.5)

# # Plot LSOA polygons (background)
# lsoa_data.plot(ax=ax, facecolor='none', edgecolor='grey', linewidth=0.5)

# # Optional title and display
# ax.set_title("London Roads Overlaid on LSOA Boundaries", fontsize=15)
# plt.show()

print(roads_with_lsoa.columns)
print(roads_with_lsoa[['id', 'lsoa21cd', 'lsoa21nm']].head())

roads_with_lsoa = roads_with_lsoa.rename(columns={"lsoa21cd": "LSOA code"})

road_counts = roads_with_lsoa.groupby('LSOA code').size().reset_index(name='road_count')
print(road_counts.head())

grouped_roads = roads_with_lsoa.dissolve(by='LSOA code', as_index=False)

lsoa_data = pd.read_excel("single_sheet_merged.xlsx")
grouped_roads = grouped_roads.merge(lsoa_data, on='LSOA code', how='left')

print(grouped_roads.head())

def map_burglaries_to_roads():
    # Plot
    fig, ax = plt.subplots(figsize=(12, 12))

    # Use burglary count to color the roads
    grouped_roads.plot(
        ax=ax,
        column='Crime Score',   # Color by this column
        cmap='Reds',               # Choose a colormap (e.g., 'Reds', 'OrRd', 'viridis')
        linewidth=1,
        legend=True,
        legend_kwds={'label': "Crime score by LSOA"}
    )

    ax.set_title("London Roads Colored by Crime Score", fontsize=15)
    ax.axis('off')
    plt.show()

map_burglaries_to_roads()