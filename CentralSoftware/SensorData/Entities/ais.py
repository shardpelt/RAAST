from Route.coordinate import Coordinate

"""
    Ais gives us a list of nearby ships
    A ship is an tuple object with it's coordinate and course angle
"""

class Ais:
    def __init__(self):
        self.nearbyShips = [{"latitude": 10, "longitude": 90, }]

    def checkThreat(self):
        # TODO: implement Ais check ->
        #  0.5 km marge aan een schip
        #  Angle is 511 als het schip niet vaart
        #  Uitwijken aan kant waar schip vandaan komt als die vaart + marge

        angleToShips = [ship for ship in self.nearbyShips]