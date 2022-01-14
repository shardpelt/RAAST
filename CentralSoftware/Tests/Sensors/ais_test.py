import math 
import sys
sys.path.append("../..")

import Sensors.Entities.ais as ais
import Route.coordinate as co

ais =  ais.Ais()
ais.nearbyShips = [{"latitude": 10, "longitude": 40, "angle": 90}, {"latitude": 5, "longitude": 20, "angle": 50}, {"latitude": 10, "longitude": 10, "angle": 70}, {"latitude": 30, "longitude": 40, "angle": 30}]

result = ais.getAisOrderedByDistance(co.Coordinate(0, 0))
print (result) 