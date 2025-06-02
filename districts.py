import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import box
import networkx as nx
import numpy as np
from shapely.geometry import MultiLineString
from collections import defaultdict
import random

from neighbourhoods import get_lsoa_geodata


def get_data_including_roads(path_to_road_links: str = 'datasets/london_road_links_only.gpkg', path_to_data_sheet: str = "single__sheet_merged_including_wards.xlsx"):
    """
    Generates a Dataframe which includes all the data from the merged data excel file, but now also includes the roads that are in each LSOA. 
    """
    
    lsoa_data = get_lsoa_geodata()
    print('Retrieved LSOA geodata')

    london_roads = gpd.read_file(path_to_road_links)

    london_roads = london_roads.to_crs(lsoa_data.crs)
    print('Retrieved london roads')

    roads_with_lsoa = gpd.sjoin(london_roads, lsoa_data, how="left", predicate="intersects")

    roads_with_lsoa = roads_with_lsoa.rename(columns={"lsoa21cd": "LSOA code"})
    print('Joined roads with LSOAs')

    grouped_roads = roads_with_lsoa.dissolve(by='LSOA code', as_index=False)

    lsoa_data = pd.read_excel(path_to_data_sheet)
    grouped_roads = grouped_roads.merge(lsoa_data, on='LSOA code', how='left')

    return grouped_roads


def generate_graph(df) -> nx.Graph:
    """
    Given a Dataframe with LSOA's and the roads within, generates a graph with LSOA's as nodes with edges between touching LSOA's. 
    """
    # Clean up the GeoDataFrame
    gdf = df.copy().reset_index(drop=True)

    # Drop conflicting columns if they exist
    for col in ['index_right', 'index1']:
        if col in gdf.columns:
            gdf = gdf.drop(columns=[col])

    # Add custom ID for spatial join tracking
    gdf['index1'] = gdf.index
    gdf['LSOA_code'] = gdf['LSOA code']

    gdf['geometry_buffered'] = gdf.geometry.buffer(10)  # buffer by 10 meters

    print('Generating neighbours...')
    # Run spatial join
    neighbors = gpd.sjoin(
        gdf.set_geometry('geometry_buffered'), 
        gdf.set_geometry('geometry_buffered'), 
        how="inner", predicate="intersects"
    )

    # Check what columns are present
    print(neighbors.columns)

    # Remove self-joins
    neighbors = neighbors[neighbors['index1_left'] != neighbors['index1_right']]

    # Build graph
    G = nx.Graph()

    print('Generating graph...')
    for _, row in gdf.iterrows():
        G.add_node(row['LSOA code'], workload=row['Crime Score'])

    for _, row in neighbors.iterrows():
        try:
            node1 = row['LSOA_code_left']
            node2 = row['LSOA_code_right']
            G.add_edge(node1, node2)
        except Exception as e:
            print(f"Edge creation failed: {e}")

    return G


def region_growing_partition(df, G, k):
    """
    Takes in our data and a graph G made from the LSOA's and an integer k, and divides the area into k patrol districts balanced by workload. 
    """

    total_workload = df['Crime Score'].sum()
    target_workload = total_workload / k
    assigned = set()
    districts = defaultdict(list)
    district_workload = defaultdict(float)
    
    # Select the top-k highest workload LSOAs as seeds
    seed_lsoas = df.sort_values('Crime Score', ascending=False)['LSOA code'].tolist()[:k]
    for i, seed in enumerate(seed_lsoas):
        districts[i].append(seed)
        district_workload[i] += G.nodes[seed]['workload']
        assigned.add(seed)

    for district_id, nodes in districts.items():
        total_workload = sum(df.loc[df['LSOA code'].isin(nodes), 'Crime Score'])
        print(f"District {district_id}: {len(nodes)} areas, workload = {total_workload}")

    # Grow each region
    frontier = {i: set(G.neighbors(seed)) - assigned for i, seed in enumerate(seed_lsoas)}

    changed = True
    while changed:
        changed = False
        for i in range(k):
            # Prioritize frontier nodes by lowest workload
            candidates = list(frontier[i])
            candidates.sort(key=lambda lsoa: G.nodes[lsoa]['workload'])

            for candidate in candidates:
                if candidate in assigned:
                    continue
                if district_workload[i] + G.nodes[candidate]['workload'] > target_workload * 1.1:
                    continue

                # Assign and update
                districts[i].append(candidate)
                district_workload[i] += G.nodes[candidate]['workload']
                assigned.add(candidate)
                changed = True

                # Add new neighbors to frontier
                for neighbor in G.neighbors(candidate):
                    if neighbor not in assigned:
                        frontier[i].add(neighbor)

                frontier[i].remove(candidate)
                break  # move to next district to ensure fairness

    # # Handle any unassigned (e.g., disconnected areas)
    # unassigned = set(G.nodes) - assigned
    # for ua in unassigned:
    #     # Assign to nearest district by workload
    #     best = min(district_workload, key=lambda i: district_workload[i])
    #     districts[best].append(ua)
    #     district_workload[best] += G.nodes[ua]['workload']

    return districts

if __name__ == "__main__":
    df = get_data_including_roads()

    ward_to_divide = 'Holland'
    df = df[df['WD24NM'] == ward_to_divide].copy()

    print(df.head())

    # Build graph
    G = generate_graph(df)
    print("Number of connected components (buffered):", nx.number_connected_components(G))

    degrees = [d for n, d in G.degree()]
    print("Average degree:", sum(degrees)/len(degrees))

    # Choose number of patrol districts
    k = 3 

    # Run partitioning
    districts = region_growing_partition(df, G, k)

    # Assign back to GeoDataFrame
    district_map = {lsoa: i for i, group in districts.items() for lsoa in group}
    df['patrol_district'] = df['LSOA code'].map(district_map)

    print('Plotting patrol districts')
    fig, ax = plt.subplots(figsize=(10, 10))

    # Plot LSOA polygons (background)
    lsoa_data = get_lsoa_geodata()
    lsoa_data.plot(ax=ax, facecolor='none', edgecolor='grey', linewidth=0.5)

    # Plot patrol districts
    df.plot(ax=ax, column='patrol_district', cmap='tab20', legend=False, figsize=(10, 10))
    plt.title('Patrol Districts Map')
    plt.axis('off')  # Optional: remove axis ticks for cleaner map
    plt.show()

    # Plot workload bar chart
    df.groupby('patrol_district')['Crime Score'].sum().plot(
        kind='bar', title='Workload per Patrol District', figsize=(10, 6))
    plt.xlabel('Patrol District')
    plt.ylabel('Sum of Crime Score')
    plt.show()