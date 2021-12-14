import math
import sys
sys.path.append("..")

import Helpers.objectToDictHelper as ds
import Route.coordinate as co

"""
    Ais gives us a list of nearby ships
    A ship is an tuple object with it's coordinate and course angle
"""

class Ais(ds.DictSerializer):
    def __init__(self):
        self.reach = 30
        self.nearbyShips = None #[{"latitude": 10, "longitude": 40, "angle": 90}, {"latitude": 10, "longitude": 20, "angle": 90}]

    def checkThreat(self):
        return True if self.nearbyShips else False

    def getAisOrderedByDistance(self, currentCoordinate: co.Coordinate):
        for ship in self.nearbyShips:
            ship["distance"] = int(math.sqrt((ship["latitude"] - currentCoordinate.latitude)**2 + (ship["longitude"] - currentCoordinate.longitude)**2))

        return sorted([list(ship.values()) for ship in self.nearbyShips], key=lambda s: s[3])

# ais = Ais()
# print(ais.getAisOrderedByDistance(co.Coordinate(10, 15)))