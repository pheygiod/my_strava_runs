import folium 

# Creating a map of the routes 
def creating_routes_map(list_of_dfs, route_map):
    for df in list_of_dfs:
    
        # Iterating through each row in each df 
        for _, row in df.iterrows(): 
        
            # making a circle marker at each longitude and latitude combination
            folium.CircleMarker( 
                location=[row['latitude'], row['longitude']],
                radius=3, # setting the circle radius 
            ).add_to(route_map) # adding the markers to the map 
            

def connecting_circle_markers(list_of_dfs, route_map):
    # Creating a nested for loop to connect the circle markers
    for df in list_of_dfs: 
        for row in df: 
        
            # Extracting geolocation info as a list of tuples
            coordinates = [tuple(x) for x in df[['latitude', 'longitude']].to_numpy()]  
            folium.PolyLine( # Creating polylines with list of tuples
                coordinates,
                weight=3 # choosing line thickness
            ).add_to(route_map)