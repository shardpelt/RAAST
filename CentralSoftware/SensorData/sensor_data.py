import sys
sys.path.append("..")

from copy import copy
import SensorData.Entities.ais as ai
import SensorData.sensor_data_image as di
import SensorData.Entities.compass as cm
import SensorData.Entities.gyroscope as gy
import SensorData.Entities.sonar as so
import SensorData.Entities.wind as wi
import Route.coordinate as co
import Helpers.angleHelper as ah

class SensorData:
    def __init__(self):
        self._angleHelper = ah.AngleHelper()
        self.rudderAngle = None
        self.sailAngle = None
        self.gyroscope = gy.Gyroscope()
        self.currentCoordinate = co.Coordinate()
        self.compass = cm.Compass()
        self.wind = wi.Wind()
        self.sonar = so.Sonar()
        self.ais = ai.Ais()
        self._image = di.SensorDataImage()      # Storing important last used data for calculations

    def makeImage(self) -> None:
        self._image.wind = copy(self.wind)

    def hasRequiredData(self) -> bool:
        #self.gyroscope.isUpRight()
        return True and self.currentCoordinate.hasData() and self.compass.hasData() and self.wind.hasData()

    def checkChangesInWind(self) -> bool:
        maxWindDeviation = 10

        if self._image.wind is not None:
            return self._angleHelper.angleIsBetweenAngles(self._image.wind.angle, self.wind.angle - maxWindDeviation, self.wind.angle + maxWindDeviation)
        return False

    def set_movementOnSonar(self, sonar: list):
        self.sonar = sonar
        # TODO: - Krijgen we een boolean of zit hier metadata zoals afstand en hoek bij?
        #		- Krijgen we data bij detectie of constant?

    def set_gyroscope(self, value):
        pass
        # TODO: - Welke data krijgen we van de gyroscoop sensor?
        #		- Krijgen we data bij omslag of constant?

    def set_wind(self, angle, speed):
        self.wind.angle = angle % 360
        self.wind.speed = speed

    def set_rudderAngle(self, angle: float):
        self.rudderAngle = angle % 360

    def set_sailAngle(self, angle: float):
        self.sailAngle = angle % 360

    def set_compassAngle(self, angle: float):
        self.compass.angle = angle % 360

    def set_currentCoordinate(self, latitude: float, longitude: float):
        self.currentCoordinate.latitude = latitude
        self.currentCoordinate.longitude = longitude

    def set_ais(self, ais):
        self.ais = ais
