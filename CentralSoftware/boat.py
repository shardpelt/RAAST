from Route.coordinate import Coordinate
from Sensors.compass import Compass
from Sensors.gyroscope import Gyroscope

class Boat:
    def __init__(self):
        self.rudderAngle = None,
        self.sailAngle = None,
        self.gyroscope = Gyroscope(),
        self.coordinate = Coordinate(),
        self.compass = Compass()

    @property
    def currentCourse(self):
        return self.compass.angle

    def setToWantedCourse(self, wantedCourse):
        pass