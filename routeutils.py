
import openrouteservice as ors
import folium
import requests
from itertools import permutations
colors=['red','blue','orange','green','gray','black','pink','purple']
#colors=['cadetblue', 'darkpurple', 'gray', 'lightgreen', 'pink', 'orange', 'blue', 'beige', 'darkred', 'red', 'lightred', 'purple', 'green', 'darkblue', 'darkgreen', 'lightblue', 'lightgray', 'black']
#colors=['#440154', '#5F9EA0', '#301934', '#808080', '#90EE90', '#FFC0CB', '#FFA500', '#0000FF', '#F5F5DC', '#8B0000', '#FF0000', '#FFCCCB', '#800080', '#008000', '#00008B', '#013220', '#000000', ]

# Replace 'your_api_key_here' with your actual API key
api_key = "5b3ce3597851110001cf62480eb660ed2b7f422288ffd1bbff0ce7b4"
endpoint = 'https://api.openrouteservice.org/geocode/search'
client = ors.Client(key=api_key)

def SimpleMatrix():
    locations = [
        [52.520008, 13.404954],  # Berlin, Germany
        [48.856613, 2.352222],   # Paris, France
        #[48.712776, 4.005974], # New York, USA
        #[51.507222, -0.12750],   # London, UK
    ]

    # Calculate the time-traveled matrix
    matrix = client.distance_matrix(
        locations=locations,
        #profile='driving-car',
        metrics=['distance'],
        units='km',
        #sources=[0],  # Index of the source location (Berlin in this example)
        #destinations=list(range(1, len(locations)))  # All other locations
    )

    # Extract the time-traveled values from the matrix response
    time_matrix = matrix['durations'][0]

    # Print the time matrix
    for i, row in enumerate(time_matrix):
        for j, time in enumerate(row):
            print(f"Travel time from {locations[i]} to {locations[j+1]}: {time} seconds")


def GetCoordinates(zip1="3572 JJ, 38"):
    params1 = {
            'api_key': api_key,
            'text': zip1,
            'boundary.country': 'NL',  # Specify the country as Netherlands
            'size': 1,  # Limit the number of results to 1
        }
    resp = requests.get(endpoint, params=params1)
    if resp.status_code != 200:
        # This means something went wrong.
        assert False
    data=resp.json()
    coord=data['features'][0]['geometry']['coordinates']
    print(zip1,coord)
    return coord

def GetRoutingData(coordinates):
    #coordinates = [coord1,coord2]
    route = client.directions(
        coordinates=coordinates,
        #profile='foot-walking',
        profile='driving-car',
        format='geojson',
        #options={"avoid_features": ["steps"]},
        validate=False,
    )
    
    locations = [list(reversed(coord)) 
                            for coord in 
                            route['features'][0]['geometry']['coordinates']]
    duration=route['features'][0]['properties']['summary']['duration'] # in seconds
    #print("This route takes",duration/60,"minutes")
    return {'locations':locations, 'duration':int(duration)} #duration is in seconds

def SimpleRoute(m=None, zip1="3572JJ, 38",zip2="3311 PE, 134", color="red"):
    if m==None:
        m = folium.Map(location=[52.097, 5.138], tiles='cartodbpositron', zoom_start=10)
    params1 = {
            'api_key': api_key,
            'text': zip1,
            'boundary.country': 'NL',  # Specify the country as Netherlands
            'size': 1,  # Limit the number of results to 1
        }
    response1 = requests.get(endpoint, params=params1)
    data1=response1.json()
    coord1=data1['features'][0]['geometry']['coordinates']

    params2 = {
            'api_key': api_key,
            'text': zip2,
            #'boundary.country': 'NL',  # Specify the country as Netherlands
            'size': 1,  # Limit the number of results to 1
        }
    response2 = requests.get(endpoint, params=params2)
    data2=response2.json()
    coord2=data2['features'][0]['geometry']['coordinates']

    # Initialize the OpenRouteService client
    coordinates = [coord1,coord2]
    route = client.directions(
        coordinates=coordinates,
        #profile='foot-walking',
        profile='driving-car',
        format='geojson',
        #options={"avoid_features": ["steps"]},
        validate=False,
    )
    folium.PolyLine(
        #color="#FF0000",
        color=color,
        weight=5,
        tooltip="From Boston to San Francisco",
        locations=[list(reversed(coord)) 
                            for coord in 
                            route['features'][0]['geometry']['coordinates']]).add_to(m)
    folium.Marker([52.0, 5.13], 
                  popup='London Bridge', 
                  icon=folium.Icon(prefix='fa',icon='university',color='green')).add_to(m)
    folium.CircleMarker([51.4183, 0.2206],
                    radius=30,
                    popup='East London',
                    color='red',
                    ).add_to(m)
    duration=route['features'][0]['properties']['summary']['duration'] # in seconds
    print("This route takes",duration/60,"minutes")
    return m

def Test():
    # Define the two zip codes (origin and destination)
    origin_zip_code = "3311 PE"  # Replace with the first zip code
    destination_zip_code = "3572 JJ"  # Replace with the second zip code

    # Use geocoding to get the coordinates for the zip codes
    origin_coordinates = client.pelias_search(origin_zip_code)
    destination_coordinates = client.pelias_search(destination_zip_code)

    # Extract the latitude and longitude for the coordinates
    origin_lat, origin_lon = origin_coordinates['features'][0]['geometry']['coordinates']
    destination_lat, destination_lon = destination_coordinates['features'][0]['geometry']['coordinates']

    # Define the coordinates as waypoints for the route
    waypoints = [(origin_lon, origin_lat), (destination_lon, destination_lat)]
    route2 = client.directions(
        coordinates=waypoints,
        profile='foot-walking',
        format='geojson',
        options={"avoid_features": ["steps"]},
        validate=False,
    )
    n = folium.Map(location=[-75,10], tiles='cartodbpositron', zoom_start=13)
    m.save("test2.html")
    folium.PolyLine(locations=[list(reversed(coord)) 
                            for coord in 
                            route['features'][0]['geometry']['coordinates']]).add_to(n)


    # Calculate the travel time between the two coordinates
    routes = client.directions(
        coordinates=waypoints,
        profile='driving-car',  # You can change this to 'driving-car', 'cycling-regular', 'foot-walking', etc.
        format='json',
        units='km',  # You can change this to 'mi' for miles
    )

    # Extract the travel time in seconds
    travel_time_seconds = routes['features'][0]['properties']['segments'][0]['duration']

    # Convert travel time to minutes
    travel_time_minutes = travel_time_seconds / 60

    print(f"Travel time between {origin_zip_code} and {destination_zip_code} is approximately {travel_time_minutes:.2f} minutes.")

#SimpleMatrix()
#m = SimpleRoute(zip1="lijsterstraat, leeuwarden",zip2="keizersgracht, amsterdam",color="red")
#m = SimpleRoute(m,zip1="singel 134, dordrecht",zip2="buitenwatersloot 175, delft",color="blue")
#m.save("test.html")

def AddSegment(m,locations,color="red"):
    folium.PolyLine(
        #color="#FF0000",
        color=color,
        weight=2,
        tooltip="text",
        locations=locations).add_to(m)
    return m

def BuildRoute(routes, allroutes, wp2coord):
    m = folium.Map(location=[52.097, 5.138], tiles='cartodbpositron', zoom_start=10)
    driver_distances=[0 for i in range(len(routes))]
    for k,wps in enumerate(routes.values()):
        col=colors[k%(len(colors))]
        if len(wps)<2:
            folium.CircleMarker([wp2coord[wps[0]][1],wp2coord[wps[0]][0]],
                            radius=10,
                            popup='text',
                            color=col,
                            fill=True,
                            fill_color='white',# if i==0 else col,
                            fill_opacity=1, # if i==0 else 0.5,
                            weight=3
                            ).add_to(m)
            continue
        #wps=route[0]
        for i in range(len(wps)-1):
            m=AddSegment(m,allroutes[(wps[i],wps[i+1])]['locations'],color=col)
            driver_distances[k] += allroutes[(wps[i],wps[i+1])]['duration']
            # folium.Marker(allroutes[(wps[i],wps[i+1])]['locations'][0], 
            #                 popup='wp', 
            #                 icon=folium.Icon(prefix='fa',icon='university',color=col)).add_to(m)
            folium.CircleMarker(allroutes[(wps[i],wps[i+1])]['locations'][0],
                            radius=10,
                            popup='text',
                            color=col,
                            fill=True,
                            fill_color='white' if i==0 else col,
                            fill_opacity=1 if i==0 else 0.5,
                            weight=3
                            ).add_to(m)
        folium.Marker(allroutes[(wps[-2],wps[-1])]['locations'][-1],
                      popup='wp', 
                      icon=folium.Icon(prefix='fa',icon='university',color=col)).add_to(m)
    return m