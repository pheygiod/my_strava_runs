import requests
import urllib3
import calendar
import pandas as pd
import matplotlib.pyplot as plt

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

def sorting_values_by_year(df):
    df = df.sort_values("year")
    return df

# Converting metres to km
def converting_metres_into_kms(df):
    df['distance_km'] = df['distance'] / 1000 # Converting metres to km
    df['distance_km'] = df['distance_km'].round() # Rounding the distances  
    df.drop(columns=['distance'], inplace=True) # Dropping the original 'distance' column 
    return df 

def creating_a_total_column(frequency_table):
    frequency_table['total'] = frequency_table.sum(axis=1)
    frequency_table.sort_values('total', inplace=True, ascending=False) # sorting the values in the total column
    frequency_table.drop(columns=["total"], inplace=True) # the total column is not needed anymore 
    return frequency_table 

# Plotting a frequency table into a grouped bar chart 
def plotting_table_into_grouped_bar_chart(frequency_table):
    frequency_table.T.plot(kind='bar', stacked=True, figsize=(10,6))
    plt.xlabel('Month')
    plt.ylabel('Frequency')
    plt.ylim(0, 20) # setting the y-axis limit
    plt.title('My Sport Activity by Month in 2023 only') # setting a title 
    plt.legend(title='Sport', bbox_to_anchor=(1.05, 1), loc='upper left') # adjusting the legend's position
    plt.xticks(rotation=45) # choosing the rotation of the ticks labels 
    plt.show # showing the plot 
    return frequency_table

# Removing activities practiced only once or twice
def remove_rows_by_sport_type(filtered_df, sport_types_to_remove):
    filtered_df = filtered_df[~filtered_df['sport_type'].isin(sport_types_to_remove)]
    return filtered_df

# Creating bins using the cut function
def creating_bins(run_df, column_name, bin_intervals, labels=None):
    run_df['distance_bins'] = pd.cut(run_df[column_name], 
                                                   bins=bin_intervals, labels=labels
                                                  )
    return run_df

# Calculating basic statistics
def calculating_basic_statistics(run_df, column_name):
    column_data = run_df[column_name]
    statistics_dict = {
        'median': column_data.median(),
        'mean': column_data.mean(),
        'std': column_data.std()
    }
    return statistics_dict

# Plotting a histogram
def plotting_a_histogram(run_df, column_name):
    plt.figure(figsize=(10,6))
    plt.hist(run_df['distance_km'], bins=bin_intervals, edgecolor='Blue', alpha=0.7)
    
    # Adding vertical lines for mean and median
    plt.axvline(mean_distance, color='red', linestyle='dashed', linewidth=1, label='Mean')
    plt.axvline(median_distance, color='black', linestyle='dashed', linewidth=1, label='Median')
    
    # Setting labels and title
    plt.xlabel('Distance (km)')
    plt.ylabel('Frequency')
    plt.title('Distribution of my Run\'s Distances')
    plt.legend()
    
    # Displaying the plot
    plt.show()
    return run_df

def clean_up_df(df):
    df_copy = df.copy()
    
    # Dropping unnecessary columns
    df_copy = df_copy.drop(['resource_state', 'athlete', 'type', 'workout_type', 'id', 'start_date_local', 'utc_offset', 'location_state', 'location_country', 'trainer', 'commute', 'private', 'flagged', 'gear_id', 'display_hide_heartrate_option', 'upload_id', 'upload_id_str', 'external_id', 'from_accepted_tag', 'average_watts', 'kilojoules', 'device_watts', 'average_cadence', 'has_heartrate', 'heartrate_opt_out', 'elapsed_time', 'timezone', 'location_city'], axis=1)
    
    df_copy["moving_time"] = df_copy["moving_time"].apply(convert_to_hhmmss)
    df_copy[["year", "month", "day", "time"]] = df_copy["start_date"].apply(start_date_to_y_m_d_t)
    
    return df_copy