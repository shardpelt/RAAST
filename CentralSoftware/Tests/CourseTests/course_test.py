import math 
import sys
sys.path.append("../..")

import Course.course as cou
import Route.coordinate as co
import Route.boarders as bo
import Sensors.sensors as sd
import Boat.boat as bt
import Route.waypoint as wp

x = 0
y = 10
waypoint = wp.Waypoint(co.Coordinate (y, x), None)
boarders = bo.Boarders (90, 10, 20, 60)

boat = bt.Boat()
boat.sensors.wind.toNorth = 10
boat.sensors.gps.coordinate.latitude = 0
boat.sensors.gps.coordinate.longitude = 0

optimalAngle = 20


#updateWantedAngle
boat.course.updateWantedAngle(waypoint, boarders)
print (111, boat.course.wantedCourseAngle)

#calcBestAngleWindFromDeadzone
result2 = boat.course.calcBestAngleWindFromDeadzone(optimalAngle)
print (222, boat.course.sailingToTheWind)
print (333, result2)

#boatAtBoarders
result3 = boat.course.boatAtBoarders(co.Coordinate(0, 0), boarders)
print (444, result3)