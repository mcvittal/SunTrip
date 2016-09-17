#!/usr/bin/env python2
'''
Main class
Imports everything and calls external libraries 
Written 17 September 2016 by Alex McVittie
Licensed under GNU GPLv3
'''


# Import local libraries
import api_key as api

# Import external libraries
import googlemaps

# Initialize variables that are to be accessed from multiple functions
total_traveltime = 0

# Contains the time, weather and location for each waypoint 
# Format:{ NumMins:{"weather":WeatherObj, "lat":Latitude, "lon":Longitude}}
twl_dict = {} 

# Get the API key for directions from api_key.py
google_api_key = api.directions_api_key
    
# Create a GoogleMapss object using the API key
gmapobj = googlemaps.Client(key=google_api_key)

def sum_time(leg_time, lat, lon):
    global twl_dict
    global total_traveltime
    # Convert leg_time to minutes
    leg_time = leg_time / 60.0
    
    # Flag that is triggered if the current leg time brings it close enough to
    # be at the next hour of the journey
    flag = False
    # Calculate number of hours before adding current leg
    num_hrs_before = int(total_traveltime) / 60
    num_mins_before = int(total_traveltime) % 60 
    
    num_mins_after = num_mins_before + leg_time
    total_traveltime += leg_time
    if num_mins_after > 50:
        flag = True 
        twl_dict[num_hrs_before + 1] = {"lat":lat, "lon":lon}
        print lat
        print lon
        print num_hrs_before + 1
        print ""
        print ""
        
    

def calc_directions(start, end, dir_mode):
    directions = gmapobj.directions(start, end,  mode=dir_mode)
    # Data dictionary is stored in the first element of the list
    directions_dict = directions[0]
    print len(directions_dict["legs"])
    journey_legs = directions_dict["legs"][0]

    # Iterate through the steps
    for step in journey_legs['steps']:
        # print (step.keys())
        sum_time(step["duration"]["value"],
                 step["end_location"]["lat"],
                 step["end_location"]["lng"])
        

# Sample calc_directions method call - also for testing

calc_directions("511 albert street, waterloo ON", 
                "69 Cardill Crescent, Ottawa, ON",
                "driving")




# End of file
