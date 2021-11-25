from copy import copy
from SensorData.sensor_data_image import SensorDataImage
from SensorData.Entities.compass import Compass
from SensorData.Entities.gyroscope import Gyroscope
from SensorData.Entities.sonar import Sonar
from SensorData.Entities.wind import Wind
from Route.coordinate import Coordinate
from Helpers.angleHelper import AngleHelper

class SensorData:
    def __init__(self):
        self.angleHelper = AngleHelper()
        self.rudderAngle = None
        self.sailAngle = None
        self.gyroscope = Gyroscope()
        self.currentCoordinate = Coordinate()
        self.compass = Compass()
        self.wind = Wind()
        self.sonar = Sonar()
        self.ais = None
        self.image = SensorDataImage()      # Storing important last used data for calculations

    def getDict(self):
        d = vars(copy(self))
        del d["angleHelper"]
        del d["image"]

        for k, v in d.items():
            try:
                d[k] = vars(v)
            except:
                pass

        return d

    def makeImage(self) -> None:
        self.image.wind = copy(self.wind)

    def hasRequiredData(self) -> bool:
        #self.gyroscope.isUpRight()
        return True and self.currentCoordinate.hasData() and self.compass.hasData() and self.wind.hasData()

    def checkChangesInWind(self) -> bool:
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
        self.wind.speed = speed
        self.wind.angle = angle % 360
        # TODO: - Vanuit welke hoek krijgen we de direction?

    def set_rudderAngle(self, angle: float):
        self.rudderAngle = angle % 360

    def set_sailAngle(self, angle: float):
        self.sailAngle = angle % 360

    def set_compassAngle(self, angle: float):
        self.compass.angle = angle % 360

    def set_currentCoordinate(self, latitude: float, longitude: float):
        self.currentCoordinate.latitude = latitude
        self.currentCoordinate.longitude = longitude

    def set_powerStateAis(self, ais):
        self.ais = ais

