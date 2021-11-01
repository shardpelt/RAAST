import copy
from SensorData.sensor_data_image import SensorDataImage
from SensorData.Entities.compass import Compass
from SensorData.Entities.gyroscope import Gyroscope
from SensorData.Entities.sonar import Sonar
from SensorData.Entities.wind import Wind
from Helpers.angleHelper import AngleHelper

class SensorData:
    def __init__(self):
        self.angleHelper = AngleHelper()
        self.rudderAngle = None
        self.sailAngle = None
        self.gyroscope = Gyroscope()
        self.currentCoordinate = None
        self.compass = Compass()
        self.wind = Wind()
        self.sonar = Sonar()
        self.ais = None
        self.image = SensorDataImage()      # Storing important last used data for calculations

    def makeImage(self):
        self.image.wind = copy.deepcopy(self.wind)

    def checkCriticalDataChanges(self):
        maxWindDeviation = 10

        if self.image.wind is not None:
            return self.angleHelper.angleIsBetweenAngles(self.image.wind.angle, self.wind.angle - maxWindDeviation, self.wind.angle + maxWindDeviation)
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
        self.rudderAngle = angle % self.angleHelper.fullRadians

    def set_sailAngle(self, angle: float):
        self.sailAngle = angle % self.angleHelper.fullRadians

    def set_compassAngle(self, angle: float):
        self.compass.angle = angle % self.angleHelper.fullRadians

    def set_currentCoordinate(self, latitude: float, longitude: float):
        self.currentCoordinate.latitude = latitude
        self.currentCoordinate.longitude = longitude

    def set_powerStateAis(self, ais):
        self.ais = ais

