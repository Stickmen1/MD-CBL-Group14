#Prerequirement - pip install geopandas shapely
# data: https://data.london.gov.uk/dataset/statistical-gis-boundary-files-london
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import os

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

def analyze_time_influence(data_folder):
    # Dictionary to store aggregated data
    aggregated_data = {}

    # Traverse the UK_police_data folder
    for root, dirs, files in os.walk(data_folder):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)

                # Read the CSV file
                try:
                    df = pd.read_csv(file_path)

                    # Ensure the file has a 'Date' column
                    if 'Date' in df.columns:
                        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                        df['YearMonth'] = df['Date'].dt.to_period('M')

                        # Aggregate data by YearMonth and Crime type
                        if 'Crime type' in df.columns:
                            grouped = df.groupby(['YearMonth', 'Crime type']).size().reset_index(name='Count')

                            for _, row in grouped.iterrows():
                                key = (row['YearMonth'], row['Crime type'])
                                aggregated_data[key] = aggregated_data.get(key, 0) + row['Count']

                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    # Convert aggregated data to DataFrame
    result_df = pd.DataFrame(
        [(key[0], key[1], count) for key, count in aggregated_data.items()],
        columns=['YearMonth', 'Crime type', 'Count']
    )

    # Plot the data
    plot_data(result_df)

def plot_data(df):
    plt.figure(figsize=(12, 6))

    # Pivot data for better visualization
    pivot_df = df.pivot(index='YearMonth', columns='Crime type', values='Count').fillna(0)

    # Plot each crime type over time
    for crime_type in pivot_df.columns:
        plt.plot(pivot_df.index.astype(str), pivot_df[crime_type], label=crime_type)

    plt.title('Crime Trends Over Time')
    plt.xlabel('Year-Month')
    plt.ylabel('Number of Incidents')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    data_folder = "UK_police_data"
    analyze_time_influence(data_folder)
