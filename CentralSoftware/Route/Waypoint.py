import sys
sys.path.append("..")

import Route.coordinate as co
import enum as en

class WpType(en.Enum):
    Predefined = 1
    Finish = 2
    AisAvoidance = 3
    SonarAvoidance = 4

class Waypoint:
    def __init__(self, coordinate: co.Coordinate, origin: WpType):
        self.coordinate = coordinate
        self.origin = origin