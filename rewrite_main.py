#!/usr/bin/env python2
'''
Rewrite of main.py to be more legible
Written 3 March 2017 by Alex McVittie
Licensed under GNU GPLv3

Purpose

Determines weather along a route.


Requirements

1. Library requirements
	forecastio:	pip install python-forecastio
	googlemaps:	pip install googlemaps
	math:		Should be preinstalled
	sys:		Should be preinstalled 

2. API key requirements
	Stored in api_key.py, NOT pushed to Git repository 
	
	Sample api_key.py variable values:
	directions_api_key = "ab4c704c5e906a12e9829a556bd45ab4"
	weather_api_key = "e4a595ee9b0caa402e7eadacce3c7442"

	API USE CONSTRAINTS
	Weather API: 	1000 requests/day free
			$0.0001 per request after 
	https://darksky.net/dev/ 
 
	Google API: 	2500 requests/day free
			$0.50 per 1000 extra requests
	https://developers.google.com/maps/documentation/directions/ 
'''
# ----------------------------------------------------------
#           Library imports, API authentications
# ----------------------------------------------------------

# Import external python classes/libraries
import googlemaps, forecastio, math, sys

# Import the api keys as an object
import api_key as api

# Set the api keys to local variables
google_api_key = api.directions_api_key
weather_api_key = api.weather_api_key

# Authenticate a google maps directions object 
gmapobj = googlemaps.Client(key=google_api_key)

# ----------------------------------------------------------
#                     Global variables
# ----------------------------------------------------------

# tl_dict
# Contains the time and location for each waypoint every 
# 	half hour. For use with getting weather every half hour
# 	along the route.
#
# Format: { NumMins:{"lat":Latitude, "lon":Longitude}}
tl_dict = {} 


# ----------------------------------------------------------
#                     Methods/Functions
# ----------------------------------------------------------

# gap_filling: Dictionary --> Dictionary
#
# METHOD PURPOSE
# Takes in a set of waypoints on a route, and if there's a gap in 
# the waypoints, it fills in the midpoints using trigonometry.
#
# INPUT VARIABLE PURPOSES
# dct: 	Dictionary containing where the user will be every half hour.
#	Keys:	Datatype: Real Integer
#			Time elapsed on the journey in minutes
#
#	Values:	Dictionary, length 2
#		Keys: "lat", "lon"
#		Contains the latitude and longitude of where the 
#		user will be at the given time of the key.
#
# OUTPUT
# The output of the method will either be the exact same as the input
# (No gap filling was needed), or it will be longer than the input
# with calculated locations. 
#
# EXAMPLE RUN
#
# INPUT
#  gap_filling({0:{"lat":1, "lon":1}, {30:{"lat":2, "lon":1.5}})
#
# OUTPUT
#  {0:{"lat":1, "lon":1}, {30:{"lat":2, "lon":1.5}}
#
# INPUT
#  gap_filling({0:{"lat":1, "lon":1}, 150:{"lat":8, "lon":2}, 300:{"lat":1, "lon":1}})
#
# OUTPUT
#  {0: {'lat': 1, 'lon': 1}, 30: {'lat': 3.3333333333333335, 'lon': 1.3333333333333333}, 
#   60: {'lat': 5.666666666666667, 'lon': 1.6666666666666665}, 90: {'lat': 8, 'lon': 2},
#   120: {'lat': 4.5, 'lon': 1.5}, 150: {'lat': 1, 'lon': 1}}

def gap_filling(dct):
	# Get the existing times in minutes as a sorted list
	existing_times = sorted(dct.keys())
	
	# List to store the missing times
	missing_times = []

	# Fill the missing times list with values that need to be calculated
	latest_time = int(max(existing_times))
	for x in range(0, latest_time + 1, 30):
		if x not in existing_times:
			missing_times.append(x)
	
	# Number of points to calculate
	i = 1
	# Boolean flag representing if we are currently in a missing area
	flag = False
	# Stores the starting lat/lon time of the missing segment
	z = 0

	# Variables to store starting lat/lon
	starting_latitude = 0
	starting_longitude = 0
	ending_latitude = 0
	ending_longitude = 0
	for x in range(0, latest_time + 1, 30):
		#Determine the starting latitude and longitude for the missing area
		if x in missing_times and not flag:
			# Start increasing the number of missing points
			i += 1 
			# Entering a missing section
			flag = True
			# Get the starting time and store to variable
			z = x - 30
			
			# Get the starting lat/lon of the missing area
			starting_latitude = dct[z]["lat"]
			starting_longitude = dct[z]["lon"]
		# Check if we are still in a missing section 
		elif x in missing_times and flag:
			# Increase the count for missing waypoints
			i += 1
		# Check to see if we have exited the missing section
		elif x not in missing_times and flag:
			# Set the boolean flag to represent we have exited the 
			flag = False

			# Grab the end lat/lon
			ending_latitude = dct[x]["lat"]
			ending_longitude = dct[x]["lon"]
			# Calculate length of missing segment using pythagoras theorem
			A = math.fabs(math.fabs(ending_latitude) - math.fabs(starting_latitude))
			B = math.fabs(math.fabs(ending_longitude) - math.fabs(starting_longitude))
			C = float(math.sqrt(A ** 2 + B ** 2))
			
			# Calculate angle in triangle
			theta  = math.atan(float(B) / A)
			
			# Iterate across the hypotenuse and calculate the missing locations
			for j in range (1, i):
				m_lat = (C / i) * math.cos(theta) * j
				m_lon = (C / i) * math.sin(theta) * j 

				# Check to see what direction the segment is
				if starting_longitude <= ending_longitude:
					# Travelling north
					new_longitude = starting_longitude + m_lon
				else:
					# Travelling south
					new_longitude = starting_longitude - m_lon
				if starting_latitude <= ending_latitude:
					# Travelling east
					new_latitude = starting_latitude + m_lat
				else:
					# Travelling west
					new_latitude = starting_latitude - m_lat
				
				dct[z + 30 * j] = {"lat":new_latitude, "lon":new_longitude}
			# Reset variables
			flag = False
			i = 1
			z = 0 
			
	
		# End of if block
	# End of for loop 
	
	# Return gap filled dictionary 
	return dct 
# End of gap_filling


# sum_time: Float Float Float Float --> Float
#
# METHOD PURPOSE
# This method determines if after the current leg, the coordinates passed in 
# will be at a half hour mark to assign weather information at the locations.
#
# It assigns this information to the globally available dictionary tl_dict. 
#
# INPUT VARIABLE PURPOSES
# leg_time:	The amount of time the current leg takes to traverse. 
# 		Passed in as seconds.
#
# lat:		The end latitude of the trip segment.
#
# lon:		The end longitude of the trip segment.
#
# total_time:	The total time elapsed on the journey so far prior to this leg. 
# 		Passed in as minutes.
#
# OUTPUT
# sum_time outputs the amount of time travelled once this leg of the journey
# has been completed, in minutes.
# 
# EXAMPLE RUN
#
# INPUTS
#  sum_time(75, 43.25, -82.65, 32)
#
#  tl_dict: unchanged.
#
# OUTPUTS
#  33.25
#
# INPUTS
#  sum_time(60, 43, -80, 118):
#
# tl_dict: Indice at 
#
# sum_time(44.6, 
def sum_time(leg_time, lat, lon, total_traveltime):
	# Reference the global tl_dict variable
	global tl_dict
	
	# Convert the leg time into minutes
	leg_time = leg_time / 60.0

	# Get the number of half hours elapsed prior to this leg.
	# Uses integer division to floor the value. Fix if upgraded to python3
	half_hours_before = int(total_traveltime) / 30 

	# Save old travel time to variable
	old_traveltime = total_traveltime

	# Get total travel time with this leg attached
	total_traveltime += leg_time
	half_hours_now = int(total_traveltime) / 30

	# Did it make it really close to the next half hour? Apply rounding if within five minutes.
	if (total_traveltime - half_hours_now  * 30 >= 25):
		half_hours_now += 1 
		total_traveltime = (half_hours_now * 30) 

	# Determine if it has reached over a half hour in time with the new travel leg
	if half_hours_now > half_hours_before:		
		# total_traveltime = (half_hours_now) * 30
		tl_dict[total_traveltime] = {"lat":lat, "lon":lon}

	# Return the updated travel time
	return total_traveltime
# End of sum_time

# calc_weather: Str, Str, Str -> Dict
#
# METHOD PURPOSE
# Calculates the directions between a start and end point by specified mode
# of transportation, determines the location at roughly every half hour,
# and then determines the weather at every hourly point and returns 
# a dictionary containing the lat/lon and weather at those locations.
# 
#
# INPUT VARIABLE PURPOSES
# start:	Contains a starting address or coordinate.
# 
# end: 		Contains an ending address or coordinate
#
# dir_mode: 	The method of transportation.
#		One of: "driving", "bicycling", "walking"
#		
# OUTPUT
# Outputs a dictionary that contains the forecast along the route. 
# Keys: 	
#		"forecast": Forecast at the 
#		"latitude"
#		"longitude"
# 
# EXAMPLE RUN
# 
# INPUTS
#   calc_weather("University of Waterloo, Waterloo, ON", "square one, mississauga, ON", "bicycling")
# OUTPUTS
#

def calc_weather(start, end, dir_mode):
	# Reference global dictionary
	global tl_dict
	
	# Initialize a variable to store the ongoing travel time
	total_traveltime = 0 

	# Fetch the directions JSON object from google maps 
	directions = gmapobj.directions(start, end, mode=dir_mode)[0]

	# Get the legs of the journey information 
	journey_legs = directions["legs"][0]
	
	# Set the starting location to get weather at hour 0 of trip 
	tl_dict[0] = {"lat":journey_legs['steps'][0]['start_location']['lat'],
		      "lon":journey_legs['steps'][0]['start_location']['lng']}

	# Iterate through the direction steps 
	for step in journey_legs['steps']:
		total_traveltime = sum_time(step["duration"]["value"],
					    step["end_location"]["lat"],
					    step["end_location"]["lng"],
					    total_traveltime)

	# Now that the actual 30 minute interval locations are recorded,
	# apply gap filling if needed.
	tl_dict = gap_filling(tl_dict)
	

	# Initialize a dictionary to store the raw weather forecast along route
	raw_forecast = {}
	
	# Get the forecast at every hour
	for k in sorted(tl_dict.keys()):
		if k % 60 == 0 or k == 0:
			latitude = tl_dict[k]["lat"]
			longitude = tl_dict[k]["lon"]
			raw_forecast[k] = {"forecast":forecastio.load_forecast(weather_api_key,
										latitude, 
										longitude).hourly().data[int(k / 60)],
					   "lat":latitude,
					   "lon":longitude}

	return raw_forecast
# End of calc_directions


def write_to_csv(weather_dict, location="output.csv"):
	f = open(location, "w")
	f.write("LAT,LON,WEATHER\n")
	for key in sorted(weather_dict.keys()):
		f.write("{},{},{}\n".format(weather_dict[key]["lat"], weather_dict[key]["lon"], weather_dict[key]["forecast"]))
	f.close()



# ----------------------------------------------------------
#                    Function calls
# ----------------------------------------------------------

# Call weather calculation using command line parameters
route = ""
try:
	start = sys.argv[1]
	end = sys.argv[2]
except:
	start = raw_input("Enter a start location: ")
	end = raw_input(  "Enter an end location:  ")
	route = raw_input("Choose a transportation method.\n[1] bicycling (default)\n[2] driving\n[3] walking\n: ")
	write = raw_input("Write to file? (Y/n):   ")
	if write != "n" or write != "N":
		filename = raw_input("Enter a filename. Leave blank for default (results.csv):  ")
	try:
		route = int(route)
		if route == 3:
			route = "walking"
		elif route == 2:
			route = "driving"
		else:
			route = "bicycling"
	except:
		route = "bicycling"

try:
	route = sys.argv[3]
except:
	route = "bicycling"

results = calc_weather(start, end, route)
if write == "n":
	for key in sorted(results.keys()):
		print "{}\n{} {}".format(results[key]["forecast"], results[key]["lat"], results[key]["lon"])
else:
	
	if filename == "":
		write_to_csv(results)
	else:
		write_to_csv(results, filename)


# ----------------------------------------------------------
#                         Testing
# ----------------------------------------------------------



'''
Successful tests

f = calc_weather("University of Waterloo, Waterloo, ON", "square one, mississauga, ON", "bicycling")
print f[120]["forecast"]
print f[120]["lat"]

f = gap_filling({0:{"lat":1, "lon":1}, 90:{"lat":8, "lon":2}, 150:{"lat":1, "lon":1}} )

g = sorted(f.keys())
for x in g:
	print "{}: {}".format(x, f[x])

f = gap_filling({0:{"lat":1, "lon":1}, 30:{"lat":2, "lon":1.5}})

g = sorted(f.keys())
for x in g:
	print "{}: {}".format(x, f[x])

'''