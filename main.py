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
import googlemaps, math

# Initialize variables that are to be accessed from multiple functions
# Contains the time and location for each waypoint , rounded to the nearest
# half hour.
# Format:{ NumMins:{"lat":Latitude, "lon":Longitude}}
tl_dict = {} 

# Get the API key for directions from api_key.py
google_api_key = api.directions_api_key
    
# Create a GoogleMapss object using the API key
gmapobj = googlemaps.Client(key=google_api_key)

def gap_filling(dct):
    existing = sorted(dct.keys())
    missing = []
    for x in range(0, existing[-1:][0], 30):
        if x not in existing:
            missing.append(x)
    i = 0
    flag = False
    z = 0
    for x in range(0, max(existing), 30):
        if x in missing and not flag:
            i += 1 
            flag = True
            z = x - 30
            s_lon = dct[z]["lon"]
            s_lat = dct[z]["lat"]
        elif x in missing and flag:
            i += 1 
        elif x not in missing and flag:
            flag = False
            # Get start and end longitude and latitude 
            e_lon = dct[x]["lon"]
            e_lat = dct[x]["lat"]
            
            Y = e_lat - s_lat
            X = e_lon - s_lon
            D = float(math.sqrt(X ** 2 + Y ** 2))

            theta = math.atan(float(Y) / X)
            
            for j in range(1, i + 1):
                m_lon = (D / i) * math.cos(theta) * j
                m_lat = (D / i) * math.sin(theta) * j
                m_lon = m_lon + s_lon
                m_lat = m_lat + s_lat
                
                dct[z + 30 * j] = {"lat":m_lat, "lon":m_lon}


            
            flag = False
    for k in sorted(dct.keys()):
        print "{}: {},{}".format(k, dct[k]["lon"], dct[k]["lat"])
            
            






def sum_time(leg_time, lat, lon, total_traveltime):
    global tl_dict
    # Convert leg_time to minutes
    leg_time = leg_time / 60.0
    
    # Flag that is triggered if the current leg time brings it close enough to
    # be at the next hour of the journey
    flag = False
    hhours_before = int(total_traveltime) / 30 
    total_traveltime += leg_time
    hhours_now = int(total_traveltime) / 30
    if total_traveltime % 30 > 15:
        total_traveltime = (hhours_now + 1) * 30
        tl_dict[total_traveltime] = {"lat":lat, "lon":lon}
        # Determine if this
    elif total_traveltime % 30 <= 15:
        total_traveltime = (hhours_now) * 30
        tl_dict[total_traveltime] = {"lat":lat, "lon":lon}





    return total_traveltime
def calc_directions(start, end, dir_mode):
    global tl_dict
    directions = gmapobj.directions(start, end,  mode=dir_mode)
    # Data dictionary is stored in the first element of the list
    directions_dict = directions[0]
    print len(directions_dict["legs"])
    journey_legs = directions_dict["legs"][0]
    total_traveltime = 0
    # Set the starting location so that you get weather at hour 0.
    tl_dict[0] = {"lat":journey_legs['steps'][0]['start_location']['lat'],
                  "lon":journey_legs['steps'][0]['start_location']['lng']}
    # Iterate through the steps
    for step in journey_legs['steps']:
        # print (step.keys())
        # print total_traveltime
        total_traveltime = sum_time(step["duration"]["value"],
                                    step["end_location"]["lat"],
                                    step["end_location"]["lng"],
                                    total_traveltime)
    print tl_dict
    gap_filling(tl_dict)

# Sample calc_directions method call - also for testing

calc_directions("511 albert street, waterloo ON", 
                "69 Cardill Crescent, Ottawa, ON",
                "driving")




# End of file
