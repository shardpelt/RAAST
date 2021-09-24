import math as m
from Sensors.coordinate import Coordinate

def optimalAngleToWaypoint(currCoordinate : Coordinate, waypoint: Coordinate):
    xDelta = waypoint.longitude - currCoordinate.longitude
    yDelta = waypoint.latitude - currCoordinate.latitude

    radians = m.atan(yDelta / xDelta)
    return radians



optimalAngleToWaypoint(Coordinate(8, 0), Coordinate(12, 4))