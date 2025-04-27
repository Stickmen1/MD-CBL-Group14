import requests
from police_api import Crime, PoliceAPI, utils
import csv
import pandas as pd
import folium
import webbrowser

api = PoliceAPI()

### Since the API function does not work properly, we will use the following function to get the data from the API.
def get_crimes(boundary, date) -> list[Crime]: 
    params = {'poly': utils.encode_polygon(boundary), 'date': date}
    x = requests.post('https://data.police.uk/api/crimes-street/all-crime', params)    
    crimes = []
    for crime in x.json():
        crimes.append(Crime(api, data = crime))
    return crimes

def get_crime_data(policeForce, date):    
    coordinates = "coordinates.csv"
    with open(coordinates, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Type", "Latitude", "Longitude"]) 

    print(f"CSV file '{coordinates}' created. You can now add data.")

    force = api.get_force(policeForce)   
    for neighbourhood in force.neighbourhoods:
        crimes = get_crimes(neighbourhood.boundary, date)
        print(f'Number of crimes in {neighbourhood.name} is {len(crimes)} in {date}')
        for crime in crimes:
            with open(coordinates, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([crime.category, crime.location.latitude, crime.location.longitude])
            #print(crime.category)   
            
#maps the crimes committed in a given month handled by a given force
def map():
    df = pd.read_csv("coordinates.csv") 
    loc_center = [df.Latitude.mean(), df.Longitude.mean()]
    my_map = folium.Map(location = loc_center, tiles='Openstreetmap', zoom_start = 14, control_scale=True)

    for index, loc in df.iterrows():
        if loc['Type']=='<CrimeCategory> Burglary':
            color = 'red'
        else:
            color = 'black'
        folium.CircleMarker([loc['Latitude'], loc['Longitude']], radius=2, color=color, weight=5, popup=loc['Type']).add_to(my_map)

    folium.LayerControl().add_to(my_map) 

    my_map.save("map.html")
    webbrowser.open("map.html")

get_crime_data('city-of-london', '2025-02')
map()