from Route.boarders import Boarders
from Route.coordinate import Coordinate
from SensorData.sensor_data import SensorData
from Helpers.angleHelper import AngleHelper

class Course:
    def __init__(self, sensorData: SensorData):
        self.shouldUpdate = True
        self.data = sensorData
        self.angleHelper = AngleHelper()
        self.wantedAngle = None
        self.wantedAngleMarge = 5 # TODO: beste marge op de koers/zeil nader te bepalen
        self.wantedSailMarge = 5
        self.toTheWind = None       # "left" or "right"
        self.cantChooseSide = None  # "left" or "right"
        self.tackingAngleMarge = 5
        self.boarderMarge = 0.005

    def isOffTrack(self):
        return not self.angleHelper.angleIsBetweenAngles(self.data.compass.angle, self.wantedAngle - self.wantedAngleMarge, self.wantedAngle + self.wantedAngleMarge)

    def updateWantedAngle(self, waypoint: Coordinate, boarders: Boarders):
        """
            :arg waypoint: Coordinate of the current waypoint
            :arg boarders: The absolute boarders in which the boat should stay during the trip
            :returns: The best course angle to set, according to the wind and the current waypoint
        """
        optimalAngle = self.angleHelper.calcAngleBetweenCoordinates(self.data.currentCoordinate, waypoint)

        if self.boatAtBoarders(self.data.currentCoordinate, boarders):
            self.forgetToTheWindCourse()

        if self.angleHelper.windFromDeadzone(optimalAngle, self.data.wind.angle):
            self.wantedAngle = self.calcBestAngleWindFromDeadzone(optimalAngle, self.data.wind.angle)
        else:
        #elif self.angleHelper.windFromBehind(optimalAngle, self.data.wind.angle):
            self.wantedAngle = optimalAngle

    def calcBestAngleWindFromDeadzone(self, optimalAngle, windAngle):
        angleLeftToDeadzone = windAngle - 45
        angleRightToDeadzone = windAngle + 45
        deltaAngles = self.angleHelper.getDeltaLeftAndRightToAngle(optimalAngle, angleLeftToDeadzone, angleRightToDeadzone)

        # If already sailing to the wind try to continue direction chosen or perform tacking maneuvre
        if self.toTheWind:

            # Check if angle to waypoint is 90 degrees -> perform tack maneuvre
            if deltaAngles["left"] <= self.tackingAngleMarge:
                self.toTheWind = "left"
                return angleLeftToDeadzone
            elif deltaAngles["right"] <= self.tackingAngleMarge:
                self.toTheWind = "right"
                return angleRightToDeadzone
            else:
                if self.toTheWind == "left":
                    return angleLeftToDeadzone
                return angleRightToDeadzone

        # If not already sailing to the wind, check which angle from deadzone is best to sail at.
        else:
            if deltaAngles["left"] <= deltaAngles["right"]:
                self.toTheWind = "left"
                return angleLeftToDeadzone

            self.toTheWind = "right"
            return angleRightToDeadzone

    def boatAtBoarders(self, currCoordinate: Coordinate, boarders: Boarders):
        if currCoordinate.latitude <= (boarders.down + self.boarderMarge):
            return True
        elif currCoordinate.latitude >= (boarders.top - self.boarderMarge):
            return True
        elif currCoordinate.longitude <= (boarders.left + self.boarderMarge):
            return True
        elif currCoordinate.longitude >= (boarders.right - self.boarderMarge):
            return True

        return False

    def forgetToTheWindCourse(self):
        self.toTheWind = None
        self.cantChooseSide = None