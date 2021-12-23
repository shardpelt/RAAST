import sys
sys.path.append("../../Route")

import Route.coordinate as co

class Gps:
    def __init__(self):
        self.coordinate = co.Coordinate()

    def hasData(self):
        return self.coordinate.hasData()