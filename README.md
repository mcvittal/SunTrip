# SunTrip
Determine a weather forecast along a route using Google Directions API.

If you want to test it, you'll need to get a Google Directions API key as well
as a forecast.io key. 

Both of these keys should go into a file named api_key.py. This file will have
two variables: directions_api_key and weather_api_key. The file isn't synced to
github because I don't want my API keys abused. 

## Usage

For command line usage, simply call main.py and follow the prompts.

    ./main.py
    Enter a start location: University of Waterloo
    Enter an end location:  Square One, Mississauga, ON
    Choose a transportation method.
    [1] bicycling (default)
    [2] driving
    [3] walking
    : 1
    Write to file? (Y/n):   Y
    Enter a filename. Leave blank for default (results.csv): 

## Screenshots of output

![Clear weather, with forecast along route](http://i.imgur.com/BfU6RzE.png) 

![Semi-bad conditions along the route](http://i.imgur.com/uh8XgEU.png)
