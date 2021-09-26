import math as m
from coordinate import Coordinate

def optimalAngleToWaypoint(currCoordinate : Coordinate, waypoint: Coordinate):
    xDelta = waypoint.longitude - currCoordinate.longitude
    yDelta = waypoint.latitude - currCoordinate.latitude

    radians = m.atan(xDelta / yDelta)
    return radians



print(optimalAngleToWaypoint(Coordinate(10, 10), Coordinate(20, 50)))