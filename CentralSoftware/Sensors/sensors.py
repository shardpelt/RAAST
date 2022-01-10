import sys
sys.path.append("..")

from copy import copy
import Sensors.Entities.gps as gp
import Sensors.Entities.ais as ai
import Sensors.sensors_image as di
import Sensors.Entities.compass as cm
import Sensors.Entities.gyroscope as gy
import Sensors.Entities.sonar as so
import Sensors.Entities.wind as wi
import Helpers.angle_helper as ah

class Sensors:
    def __init__(self):
        self.gyroscope = gy.Gyroscope()
        self.gps = gp.Gps()
        self.compass = cm.Compass()
        self.wind = wi.Wind()
        self.sonar = so.Sonar()
        self.ais = ai.Ais()
        self.rudderAngle = None
        self.sailAngle = None
        self._image = di.SensorDataImage()      # Storing important last used data for calculations
        self._angleHelper = ah.AngleHelper()

    def makeImage(self) -> None:
        self._image.wind = copy(self.wind)

    def enoughDataToSail(self) -> bool:
        return self.gps.hasData() and self.compass.hasData() and self.wind.hasData()

    def checkChangesInWind(self) -> bool:
        maxWindDeviation = 10

        if self._image.wind is not None:
            return self._angleHelper.angleIsBetweenAngles(self._image.wind.angle, self.wind.relative - maxWindDeviation, self.wind.relative + maxWindDeviation)
        return False

    def set_movementOnSonar(self, sonar: list):
        self.sonar = sonar
        # TODO: - Krijgen we een boolean of zit hier metadata zoals afstand en hoek bij?
        #		- Krijgen we data bij detectie of constant?

    def set_gyroscope(self, value):
        pass
        # TODO: - Welke data krijgen we van de gyroscoop sensor?
        #		- Krijgen we data bij omslag of constant?

    def set_wind(self, relativeAngle, speed = None):
        self.wind.relative = relativeAngle % 360
        self.wind.speed = speed

        if self.compass.hasData():
            self.wind.toNorth = (relativeAngle + self.compass.angle) % 360

    def set_rudderAngle(self, angle: float):
        self.rudderAngle = angle % 360

    def set_sailAngle(self, angle: float):
        self.sailAngle = angle % 360

    def set_compassAngle(self, angle: float):
        self.compass.angle = angle % 360

    def set_gps(self, latitude: float, longitude: float):
        self.gps.coordinate.latitude = latitude
        self.gps.coordinate.longitude = longitude

    def set_ais(self, ais):
        self.ais = ais
