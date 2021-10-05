from Sensors.wind import Wind
from Route.coordinate import Coordinate
from Route.route import Route
from course import Course
from boat import Boat

class CentralData:

    def __init__(self):
        self.boat = Boat(),
        self.route = Route(),
        self.course = Course(),
        self.wind = Wind(),
        self.movementOnSonar = False,
        self.powerStateAis = "Off"

    # Call: 2
    def updateCourse(self):
        self.course.calculateBestAngle(self.boat.coordinate, self.route.currentWaypoint, self.wind.angle, self.route.boarders)

    # Call: 1
    def checkWaypointReached(self):
        if self.route.checkWaypointReached(self.boat.coordinate):
            self.route.updateToNextWaypoint()


    def circumnavigateObstacle(self, coordinate: Coordinate, distance: float, angle: float):
        self.route.findWayAroundObstacle(coordinate, distance, angle)

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
