import math 
import sys
sys.path.append("../..")
import Course.course as cou
import Route.coordinate as co
import Route.boarders as bo
import SensorData.sensor_data as sd

x = 0
y = 10
waypoint = co.Coordinate (y, x)
boarders = bo.Boarders (90, 10, 20, 60)

sensorData = sd.SensorData()

sensorData.wind.angle = 10
sensorData.currentCoordinate = co.Coordinate (0, 0)

optimalAngle = 20

course = cou.Course(sensorData)

currentCoordinate = co.Coordinate (0, 0)


#updateWantedAngle
course.updateWantedAngle(waypoint, boarders)
print (111, course.wantedAngle)

#calcBestAngleWindFromDeadzone
result2 = course.calcBestAngleWindFromDeadzone(optimalAngle, sensorData.wind.angle)
print (222, course.toTheWind)
print (333, result2)

#boatAtBoarders
result3 = course.boatOutsideBoarders(currentCoordinate, boarders)
print (444, result3)