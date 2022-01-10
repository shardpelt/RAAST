import sys
sys.path.append("..")

import Route.coordinate as co
import Enums.waypoint_type_enum as we

class Waypoint:
    def __init__(self, coordinate: co.Coordinate, origin: we.WpType):
        self.coordinate = coordinate
        self.origin = origin