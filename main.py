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

directions = gmapobj.directions("511 albert street, waterloo ON", 
                                "200 University Avenue, Waterloo ON",
                                mode="driving")

# Data dictionary is stored in the first element of the list
directions_dict = directions[0]

journey_legs = directions_dict["legs"][0]
print type(journey_legs)
print journey_legs.keys()

trip_steps = journey_legs['steps']
print (trip_steps)


# End of file
