import sys
sys.path.append("..")

import Route.boarders as bo
import Route.coordinate as co
import Route.waypoint as wp
import Helpers.angleHelper as ah

class Course:
    def __init__(self, boat):
        self.shouldUpdate = True
        self._boat = boat
        self._angleHelper = ah.AngleHelper()
        self.wantedAngle = None
        self.wantedAngleMarge = 5 # TODO: beste marge op de koers/zeil nader te bepalen
        self.wantedSailMarge = 5
        self.toTheWind = None       # "left" or "right"
        self.cantChooseSide = None  # "left" or "right"
        self.tackingAngleMarge = 5
        self.boarderMarge = 0.005

    def isOffTrack(self):
        return not self._angleHelper.angleIsBetweenAngles(self._boat.data.compass.angle, self.wantedAngle - self.wantedAngleMarge, self.wantedAngle + self.wantedAngleMarge)

    def updateWantedAngle(self, waypoint: wp.Waypoint, boarders: bo.Boarders):
        """
            :arg waypoint: The current waypoint
            :arg boarders: The absolute boarders in which the _boat should stay during the trip
            :returns: The best course angle to set, according to the wind and the current waypoint
        """
        optimalAngle = self._angleHelper.calcAngleBetweenCoordinates(self._boat.data.currentCoordinate, waypoint.coordinate)

        if self._boatAtBoarders(self._boat.data.currentCoordinate, boarders):
            self.forgetToTheWindCourse()

        if self._angleHelper.windFromDeadzone(self._boat.data.wind.angle):
            self.wantedAngle = self.calcBestAngleWindFromDeadzone(optimalAngle, self._boat.data.wind.angle)
        else:
        #elif self._angleHelper.windFromBehind(optimalAngle, self._boat.data.wind.angle):
            self.wantedAngle = optimalAngle

    def calcBestAngleWindFromDeadzone(self, optimalAngle, windAngle):
        angleLeftToDeadzone = ((windAngle - 45) % 360 + self._boat.data.compass.angle) % 360
        angleRightToDeadzone = ((windAngle + 45) % 360 + self._boat.data.compass.angle) % 360

        deltaAngles = self._angleHelper.getDeltaLeftAndRightToAngle(optimalAngle, angleLeftToDeadzone, angleRightToDeadzone)

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

    def _boatAtBoarders(self, currCoordinate: co.Coordinate, boarders: bo.Boarders):
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