import copy
from CentralData.central_data_image import CentralDataImage
from Sensors.compass import Compass
from Sensors.gyroscope import Gyroscope
from Sensors.sonar import Sonar
from Sensors.wind import Wind
from Helpers.angleHelper import AngleHelper

class CentralData:
    def __init__(self):
        self.rudderAngle = None
        self.sailAngle = None
        self.gyroscope = Gyroscope()
        self.currentCoordinate = None
        self.compass = Compass()
        self.wind = Wind()
        self.sonar = Sonar()
        self.ais = None
        self.image = CentralDataImage()      # Storing important last used data for calculations

    def makeImage(self):
        self.image.wind = copy.deepcopy(self.wind)

    def checkCriticalDataChanges(self):
        maxWindDeviation = 10

        if self.image.wind is not None:
            return AngleHelper.angleIsBetweenAngles(self.image.wind.angle, self.wind.angle - maxWindDeviation, self.wind.angle + maxWindDeviation)
        return False

    def set_movementOnSonar(self, sonar: list):
        self.sonar = sonar
        # TODO: - Krijgen we een boolean of zit hier metadata zoals afstand en hoek bij?
        #		- Krijgen we data bij detectie of constant?

    def set_gyroscope(self, value):
        pass
        # TODO: - Welke data krijgen we van de gyroscoop sensor?
        #		- Krijgen we data bij omslag of constant?

    def set_wind(self, speed, angle):
        self.wind.set_speed(speed)
        self.wind.set_angle(angle)
        # TODO: - Vanuit welke hoek krijgen we de direction?

    def set_rudderAngle(self, angle: float):
        self.rudderAngle = angle % AngleHelper.fullRadians

    def set_sailAngle(self, angle: float):
        self.sailAngle = angle % AngleHelper.fullRadians

    def set_compassAngle(self, angle: float):
        self.compass.angle = angle % AngleHelper.fullRadians

    def set_currentCoordinate(self, latitude: float, longitude: float):
        self.currentCoordinate.latitude = latitude
        self.currentCoordinate.longitude = longitude

    def set_powerStateAis(self, ais):
        self.ais = ais

