from Sensors.compass import Compass
from Sensors.wind import Wind
from Sensors.gyroscope import Gyroscope
from Sailing.coordinate import Coordinate
from Sailing.sailingCourse import SailingCourse

class CentralData:

    def __init__(self):
        self.rudderAngle = None,
        self.sailAngle = None,
        self.wantedCourse = None,
        self.wind = Wind(),
        self.sailingCourse = SailingCourse(),
        self.gyroscope = Gyroscope(),
        self.currentCoordinate = Coordinate(),
        self.compass = Compass(),
        self.movementOnSonar = False,
        self.powerStateAis = "Off"

    @property
    def currentCourse(self):
        return self.compass.angle

    # Call: 2
    def updateCourse(self):
        self.wantedCourse = self.sailingCourse.calculateBestCourse(self.currentCoordinate, self.wind.angle)

    # Call: 1
    def checkWaypointReached(self):
        if self.sailingCourse.checkWaypointReached(self.currentCoordinate):
            self.sailingCourse.updateToNextWaypoint()

    def circumnavigateObstacle(self, coordinate: Coordinate, distance: float, angle: float):
        self.sailingCourse.findWayAroundObstacle(coordinate, distance, angle)

    def set_movementOnSonar(self, movement: bool):
        self.movementOnSonar = movement
        # TODO: - Krijgen we een boolean of zit hier metadata zoals afstand en hoek bij?
        #		- Krijgen we data bij detectie of constant?


    def set_gyroscope(self, value):
        pass
        # TODO: - Welke data krijgen we van de gyroscoop sensor?
        #		- Krijgen we data bij omslag of constant?


    def set_wind(self, speed, direction):
        self.wind.set_speed(speed)
        self.wind.set_direction(direction)
        # TODO: - Vanuit welke hoek krijgen we de direction?


    def set_rudderAngle(self, angle: int):
        self.rudderAngle = angle % 360


    def set_sailAngle(self, angle: int):
        self.rudderAngle = angle % 360


    def set_compassAngle(self, angle: int):
        self.compass = angle % 360


    def set_currentCoordinate(self, latitude: float, longitude: float):
        self.currentCoordinate.latitude = latitude
        self.currentCoordinate.longitude = longitude


    def set_powerStateAis(self, powerState: str):
        self.powerStateAis = powerState
