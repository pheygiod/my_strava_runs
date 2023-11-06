import requests
import urllib3
import calendar
import pandas as pd

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


AUTH_URL = "https://www.strava.com/oauth/token"
ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"

def getting_access_and_refresh_tokens(client_id, client_secret, refresh_token):
    """
    Function to do bla. has 3 args, must be strings
    """
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': "refresh_token",
        'f': 'json'
    }
    
    print("Requesting Token...\n")
    res = requests.post(AUTH_URL, data=payload, verify=False)
    access_token = res.json()['access_token']
    
    return access_token
   

def get_dataset(access_token):
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': 200, 'page': 1}
    my_dataset = requests.get(ACTIVITIES_URL, headers=header, params=param).json()
    # Creating a dataframe
    df = pd.DataFrame(my_dataset)
    return df



# Converting the moving_time column into hours, minutes, and seconds
def convert_to_hhmmss(moving_time): # Creating a function that takes in as input a moving time 
    # converting seconds into integers 
    total_seconds = int(moving_time)
    
    # dividing seconds and assigning the final number to hours 
    hours = total_seconds // 3600
    
    # converting total number of seconds into minutes 
    minutes = (total_seconds % 3600) // 60 # computing the remainder when total_seconds is divided by 3600
    
    # calculating the number of seconds 
    seconds = total_seconds % 60 # dividing total_seconds by 60 (which is the amount of seconds in a minute)   
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# Splitting the start date into year, month, day, and time
def start_date_to_y_m_d_t(start_date):
    split_start_date = start_date.split("T")
    y_m_d = split_start_date[0]
    split_y_m_d = y_m_d.split("-")
    year = split_y_m_d[0]
    month = split_y_m_d[1]
    day = split_y_m_d[2]
    time = split_start_date[1].rstrip("Z")
    
    return pd.Series({
        "year" : int(year),
        "month" : int(month),
        "day" : int(day),
        "time" : time
    })

def converting_num_months_to_strings(df):
    # Swapping numeric 'month' with its corresponding name
    df['month'] = df['month'].apply(lambda x: calendar.month_name[x]) # converting numeric month to month names
    
    # Defining the custom month order
    custom_month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    # Converting the 'month' column to categorical with custom order
    df['month'] = pd.Categorical(df['month'], categories=custom_month_order, ordered=True)
    
    return df

def clean_up_df(df):
    df_copy = df.copy()
    
    # Dropping unnecessary columns
    df_copy = df_copy.drop(['resource_state', 'athlete', 'type', 'workout_type', 'id', 'start_date_local', 'utc_offset', 'location_state', 'location_country', 'trainer', 'commute', 'private', 'flagged', 'gear_id', 'display_hide_heartrate_option', 'upload_id', 'upload_id_str', 'external_id', 'from_accepted_tag', 'average_watts', 'kilojoules', 'device_watts', 'average_cadence', 'has_heartrate', 'heartrate_opt_out', 'elapsed_time', 'timezone', 'location_city'], axis=1)
    
    df_copy["moving_time"] = df_copy["moving_time"].apply(convert_to_hhmmss)
    df_copy[["year", "month", "day", "time"]] = df_copy["start_date"].apply(start_date_to_y_m_d_t)
    
    return df_copy