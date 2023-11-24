# my_strava_runs
Scraping data from my personal Strava account via the API they provide and creating data visualisations and map routes!🏃

# Table of Contents
- General Info
- Setup
- Usage
- Project Status
- Room for Improvement
- Acknowledgements
- Contact

# General Information 
I’m uploading my code of the physical activities I analysed using Strava's APIs!💻🏈 The goal was to explore the activities I tracked and uploaded onto my Strava account and see if I could make some nice plots. With this initiative I also want to support other coders who are sports fanatics like me and are willing to plot your own maps!🗺️🔎👣

The data I extracted is made up of 137 rows and 58 columns. I helped myself with [this](https://towardsdatascience.com/using-the-strava-api-and-pandas-to-explore-your-activity-data-d94901d9bfde) article, which explains how to get the data through Strava's APIs. I got the data, cleansed it🛁, and started exploring it.

# Setup
First off, make sure you have conda🐍👀:

`conda create -n <replace-with-name-you-want> python=3.11`

`conda activate <replace-with-name-you-want>`

`pip install -r requirements.txt`


# Usage 
Check out the py files in my repo to see how I've processed the data, exported the gpx files, and created the maps!

- data_processing.py🎰 
- gpx_files_processing.py📂
- geospatial_data_processing.py🌏 

For a full walkthrough of the project, check out the `strava_project.ipynb` file!📌

# Project Results 
I discovered that my most frequent activity in the past couple of years was running, and the most common run distance was 5km🏃. I also found out that my average pace decreased during my short runs. Probably because I was training for a marathon. Last but not least, Oxfordshire is the county where I exercised the most since I live here🏡🇬🇧. 

# Future Data Exploration Ideas
For future use, we could design some time series visualisations to track our fitness progress over time⏰(e.g., heart rate, calories burned, etc.). We could also create a radar chart to compare our runs with the ones of our partners/friends'📊. We could even plot a chart to compare the ranking of teams during sports tournaments🥇(e.g., metrics could include defense, offense, rating). For me, the sport would be padel🎾. For you, it can be any sport/activity that you like!

# Acknowledgements
A massive thank you to `Matt Ambrogi` for the awesome tutorial on diving into Strava data with Python APIs. Your insights have been a game-changer for me!

Big kudos to `Meg` from Strava for the fantastic tutorial on bulk-export data through APIs – your efforts have made the process so much clearer and user-friendly!

Last but not least, a special shoutout to `Ward Haddadin` for always motivating me in my coding journey! Ward, your help in checking my code and pushing me do big things has been invaluable. 

# Contact
For any question, drop me a line at giorgiadt14@gmail.com and I'll be happy to help you out! Feel free to message me on [LinkedIn](https://www.linkedin.com/in/giorgia-dim/) too! Happy coding!