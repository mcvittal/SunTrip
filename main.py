#!/usr/bin/env python3
'''
Main class
Imports everything and calls external libraries 
Written 17 September 2016 by Alex McVittie
Licensed under GNU GPLv3
'''


# Import local libraries
from api_key import api 

# Import external libraries
from google.directions import GoogleDirections



# Get the API key for directions 
google_api_key = api.directions_api_key


print(google_api_key)


