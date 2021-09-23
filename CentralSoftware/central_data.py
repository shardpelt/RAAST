from Sensors.wind import Wind
from Sensors.gyroscope import Gyroscope
from Sensors.coordinate import Coordinate
from route import Route

class CentralData:

    def __init__(self):
        self.rudderAngle = None,
        self.sailAngle = None,
        self.wind = Wind(),
        self.route = Route(),
        self.gyroscope = Gyroscope(),
        self.currentCoordinate = Coordinate(),
        self.compass = None,
        self.movementOnSonar = False,
        self.powerStateAis = "Off"


    # Call when currentCoordinate gets updated
    def checkWaypointReached(self):
        if self.route.checkWaypointReached(self.currentCoordinate):
            self.updateRoute()


    # Call when checkRoute
    def updateRoute(self):
        self.route.update()




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
