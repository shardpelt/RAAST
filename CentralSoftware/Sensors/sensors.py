import sys
sys.path.append("..")

import Sensors.Entities.gps as gp
import Sensors.Entities.ais as ai
import Sensors.Entities.compass as cm
import Sensors.Entities.gyroscope as gy
import Sensors.Entities.sonar as so
import Sensors.Entities.wind as wi
import Helpers.angle_helper as ah

class Sensors:
    def __init__(self):
        self._angleHelper = ah.AngleHelper()
        self.gyroscope = gy.Gyroscope()
        self.gps = gp.Gps()
        self.compass = cm.Compass()
        self.wind = wi.Wind()
        self.sonar = so.Sonar()
        self.ais = ai.Ais()
        self.actualRudderAngle = None
        self.actualSailAngle = None

    def enoughDataToSail(self) -> bool:
        return self.gps.hasData() and self.compass.hasData() and self.wind.hasData()

    def set_gyroscope(self, pitch, roll):
        self.gyroscope.pitch = pitch
        self.gyroscope.roll = roll

    def set_wind(self, relativeAngle, speed = None):
        self.wind.relative = relativeAngle % 360
        self.wind.speed = speed

        if self.compass.hasData():
            self.wind.toNorth = (relativeAngle + self.compass.angle) % 360

    def set_actualRudderAngle(self, angle: float):
        self.actualRudderAngle = angle % 360

    def set_actualSailAngle(self, angle: float):
        self.actualSailAngle = angle % 360

    def set_compassAngle(self, angle: float):
        self.compass.angle = angle % 360

    def set_gps(self, latitude: float, longitude: float):
        self.gps.coordinate.latitude = latitude
        self.gps.coordinate.longitude = longitude

    def set_movementOnSonar(self, objectDetected: bool):
        self.sonar.objectDetected = objectDetected

    def set_ais(self, nearbyShips):
        self.ais.nearbyShips = nearbyShips

