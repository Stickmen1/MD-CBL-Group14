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

    print("Reading road links...")
    road_links = gpd.read_file("datasets/uk_road.gpkg", layer="road_link")
    print("Done reading. Reprojecting...")

    road_links = road_links.to_crs("EPSG:4326")
    print("Done reprojecting. Clipping to London...")

    london_roads = gpd.clip(road_links, bbox_gdf)
    print("Clipping done.")

    london_roads.to_file("datasets/london_road_links_only.gpkg", layer="road_node", driver="GPKG")


def get_lsoa_geodata(lsoa_folder: str = "datasets/lsoa_boundaries/") -> gpd.GeoDataFrame:
    # Folder where you downloaded all borough LSOA files
    folder_path = lsoa_folder

    print("Getting lsoa geodata...")

    # List all files (e.g. all shapefiles or GeoJSONs)
    files = [f for f in os.listdir(folder_path) if f.endswith('.shp')]  # or '.shp'

    # Read and concatenate all files
    lsoa_list = []
    for file in files:
        gdf = gpd.read_file(os.path.join(folder_path, file))
        lsoa_list.append(gdf)

    # Combine into one GeoDataFrame
    lsoa_all = gpd.GeoDataFrame(pd.concat(lsoa_list, ignore_index=True))

    return lsoa_all


def map_burglaries_to_roads(df):
        # Plot
        fig, ax = plt.subplots(figsize=(12, 12))

        # Use burglary count to color the roads
        df.plot(
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


def add_wards_to_data(data_df_path: str, lsoa_to_ward_path: str, new_file_name: str = 'single__sheet_merged_including_wards.xlsx') -> None:
     # Get the data
    df_main = pd.read_csv(data_df_path)
    df_lookup = pd.read_csv(lsoa_to_ward_path)

    # Merge the data on LSOA's
    df_merged: pd.DataFrame = df_main.merge(
    df_lookup[['LSOA21NM', 'WD24CD', 'WD24NM']],
    left_on='LSOA',
    right_on='LSOA21NM',
    how='left'
    )

    # Get rid of the double LSOA column since it is no longer needed
    df_merged = df_merged.drop(columns=['LSOA21NM'])
    
    print(df_merged[['LSOA', 'WD24NM']].head())
    print(df_merged.head())

    df_merged.to_csv(new_file_name, index=False)
    print('Created new data file named: ', new_file_name)
    


if __name__ == "__main__":
    # # To see intermediate plots, uncomment the respective lines
    lsoa_data = get_lsoa_geodata()

    london_roads = gpd.read_file('datasets/london_road_links_only.gpkg')

    london_roads = london_roads.to_crs(lsoa_data.crs)

    roads_with_lsoa = gpd.sjoin(london_roads, lsoa_data, how="left", predicate="intersects")

    #print(roads_with_lsoa['lsoa21nm'].unique())

    # # roads_with_lsoa.plot(markersize=5, color='red')
    # # plt.show()

    # # # Plot the new map
    # # fig, ax = plt.subplots(figsize=(12, 12))

    # # # Plot road links on top
    # # london_roads.plot(ax=ax, color='red', linewidth=0.5)

    # # # Plot LSOA polygons (background)
    # # lsoa_data.plot(ax=ax, facecolor='none', edgecolor='grey', linewidth=0.5)

    # # # Optional title and display
    # # ax.set_title("London Roads Overlaid on LSOA Boundaries", fontsize=15)
    # # plt.show()

    # # print(roads_with_lsoa.columns)
    # # print(roads_with_lsoa[['id', 'lsoa21cd', 'lsoa21nm']].head())

    # roads_with_lsoa = roads_with_lsoa.rename(columns={"lsoa21nm": "LSOA"})

    # # road_counts = roads_with_lsoa.groupby('LSOA').size().reset_index(name='road_count')
    # # print(road_counts.head())

    # grouped_roads = roads_with_lsoa.dissolve(by='LSOA', as_index=False)

    # lsoa_data = pd.read_csv("burglary_risk_forecast_all_months.csv")
    # grouped_roads = grouped_roads.merge(lsoa_data, on='LSOA', how='left')

    # print(grouped_roads.head())

    # map_burglaries_to_roads(grouped_roads)

    # Used for adding ward classifications to the LSOA's, creating a new data file
    add_wards_to_data("burglary_risk_forecast_all_months.csv", "datasets/LSOA_(2021)_to_Electoral_Ward_(2024)_to_LAD_(2024).csv", 'burglary_risk_forecast_all_months_incl_wards.csv')