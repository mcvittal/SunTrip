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
# Contains the time, weather and location for each waypoint 
# Format:{ NumMins:{"weather":WeatherObj, "lat":Latitude, "lon":Longitude}}
twl_dict = {} 

# Get the API key for directions from api_key.py
google_api_key = api.directions_api_key
    
# Create a GoogleMapss object using the API key
gmapobj = googlemaps.Client(key=google_api_key)

def sum_time(leg_time, lat, lon, total_traveltime):
    global twl_dict
    # Convert leg_time to minutes
    leg_time = leg_time / 60.0
    
    # Flag that is triggered if the current leg time brings it close enough to
    # be at the next hour of the journey
    flag = False
    hours_before = int(total_traveltime) / 60

    total_traveltime += leg_time
    hours_now = int(total_traveltime) / 60

    if total_traveltime % 60 > 50:
        total_traveltime = (hours_now + 1) * 60
        print total_traveltime


    return total_traveltime
def calc_directions(start, end, dir_mode):
    directions = gmapobj.directions(start, end,  mode=dir_mode)
    # Data dictionary is stored in the first element of the list
    directions_dict = directions[0]
    print len(directions_dict["legs"])
    journey_legs = directions_dict["legs"][0]
    total_traveltime = 0 
    # Iterate through the steps
    for step in journey_legs['steps']:
        # print (step.keys())
        # print total_traveltime
        total_traveltime = sum_time(step["duration"]["value"],
                                    step["end_location"]["lat"],
                                    step["end_location"]["lng"],
                                    total_traveltime)
        

# Sample calc_directions method call - also for testing

calc_directions("511 albert street, waterloo ON", 
                "69 Cardill Crescent, Ottawa, ON",
                "driving")




# End of file
