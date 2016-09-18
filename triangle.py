#!/usr/bin/env python2

import math

n = 5

# Coordinates
a_lat = 7
a_lon = 5

b_lat = 18
b_lon = 19

Y = b_lat - a_lat
X = b_lon - a_lon

D = float(math.sqrt(X ** 2 + Y ** 2))

print D
print X
print Y

theta = math.atan(float(Y) / X)  
theta_deg = (theta * 180)/math.pi
print theta
print theta_deg

x1 = (D / n ) * math.cos(theta) * 1 # the * 1 is actually gonna be * j
y1 = (D / n ) * math.sin(theta) * 1 
print x1
print y1
