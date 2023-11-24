import gpxpy
import gpxpy.gpx
import gzip
import pandas as pd
import shutil

# Extracting GPX files and unzipping zipped GPX files 
def extracting_gpx_files(activities_directory, gpx_files):
    
    # Iterating through each file in the activities directory 
    for file in activities_directory.iterdir():
        
        # Checking if the file has both a .gpx and .gz extension    
        if '.gpx' in str(file) and str(file).endswith('.gz'): # Not using 'endswith' for gpx since some files    contain .gpx but may end with .gz
    
            # Reading the gzip-compressed file in binary-read mode 
            with gzip.open(str(file), 'rb') as f_in:
                
                # Creating the path of the new unzipped files
                unzipped_path = gpx_files / file.parts[-1].replace(".gz", "")
                
                # Opening the file at the new path 
                with open(str(unzipped_path), 'wb') as f_out: 
                
                    # Copying the content of the file with shutil
                    shutil.copyfileobj(f_in, f_out)
                    
        # Checking if the file has only a .gpx extension 
        if '.gpx' in str(file) and not str(file).endswith('.gz'):
        
            # Creating the path of the new files 
            gpx_file_path = gpx_files / file.parts[-1]
        
            # Moving the file to the new gpx directory 
            shutil.move(str(file), str(gpx_file_path))

            
# Creating a function that takes in a file path and returns a dataframe
def gpx_files_to_df(file_path):
    
    # Parsing the gpx file 
    gpx = gpxpy.parse(open(file_path))   
    
    # Creating an empty list for each info we want to store in the df 
    lats = []
    longs = []
    elevs = []
    times = []
    
    # Iterating through each point in the segment of the track of the gpx file
    for point in gpx.tracks[0].segments[0].points:
    
    # Appending each info from the point to the correspondent empty list
        lats.append(point.latitude)
        longs.append(point.longitude)
        elevs.append(point.elevation)
        times.append(point.time)
        
    # Creating a dataframe with the information as names of the columns 
    my_df = pd.DataFrame.from_dict(
    {
        "longitude": longs,
        "latitude": lats,
        "elevation": elevs,
        "time": times,
    }
    )
    return my_df