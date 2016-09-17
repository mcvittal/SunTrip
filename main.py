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

# Get the API key for directions from api_key.py
google_api_key = api.directions_api_key
    
# Create a GoogleMapss object using the API key
gmapobj = googlemaps.Client(key=google_api_key)


def calc_directions(start, end, dir_mode):
    directions = gmapobj.directions(start, end,  mode=dir_mode)
    # Data dictionary is stored in the first element of the list
    directions_dict = directions[0]

    journey_legs = directions_dict["legs"][0]

    # Troubleshooting/testing
    #print type(journey_legs)
    #print journey_legs.keys()

    trip_steps = journey_legs['steps'][0[]
    # print (trip_steps)

calc_directions("511 albert street, waterloo ON", 
                "200 university avenue, waterloo ON",
                "driving")



# End of file
