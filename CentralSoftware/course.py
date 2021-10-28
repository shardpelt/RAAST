import sys
sys.path.append("..")
from Route.coordinate import Coordinate
from Helpers.angleHelper import AngleHelper
from CentralData.central_data import CentralData

class Course:
    radians45 = AngleHelper.toRadians(45)

    def __init__(self, centralData: CentralData):
        self.data = centralData
        self.wantedAngle = None
        self.wantedAngleMarge = 5 # TODO: beste marge op de koers nader te bepalen
        self.closeHauled = {"flag":False, "chosenSide":"", "forbiddenSide":""}
        self.tackingAngleMarge = AngleHelper.toRadians(5)
        self.boarderMarge = 0.005

    def isOnTrack(self):
        return AngleHelper.angleIsBetweenAngles(self.data.compass.angle, self.wantedAngle - self.wantedAngleMarge, self.wantedAngle + self.wantedAngleMarge)

    def updateWantedAngle(self, waypoint: Coordinate, boarders: dict):
        """
            :arg waypoint: Coordinate of the current waypoint
            :arg boarders: The absolute boarders in which the boat should stay during the trip
            :returns: The best course angle to set, according to the wind and the current waypoint
        """
        optimalAngle = AngleHelper.hypotenuseAngleToWaypoint(self.data.currentCoordinate, waypoint)

        if self.boatAtBoarders(self.data.currentCoordinate, boarders):
            self.forgetCloseHauledCourse()

        if self.windFromDeadzone(optimalAngle, self.data.wind.angle):
            self.wantedAngle = self.calcBestAngleWindFromDeadzone(optimalAngle, self.data.wind.angle)

        elif self.windFromBehind(optimalAngle, self.data.wind.angle):
            self.wantedAngle = optimalAngle

    def calcBestAngleWindFromDeadzone(self, optimalAngle, windAngle):
        angleLeftToDeadzone = windAngle - self.radians45
        angleRightToDeadzone = windAngle + self.radians45
        deltaAngles = AngleHelper.getDeltasOfLeftAndRight(optimalAngle, angleLeftToDeadzone, angleRightToDeadzone)

        # If already sailing closeHauled try to continue direction chosen or perform tacking maneuvre
        if self.closeHauled["flag"]:

            # Check if angle to waypoint is 90 degrees -> perform tack maneuvre
            if deltaAngles["L"] <= self.tackingAngleMarge:
                self.closeHauled["flag"] = True
                self.closeHauled["chosenSide"] = "left"
                return angleLeftToDeadzone
            elif deltaAngles["R"] <= self.tackingAngleMarge:
                self.closeHauled["flag"] = True
                self.closeHauled["chosenSide"] = "right"
                return angleRightToDeadzone
            else:
                if self.closeHauled["chosenSide"] == "left":
                    return angleLeftToDeadzone
                return angleRightToDeadzone

        # If not already sailing closeHauled, check which angle from deadzone is best to sail at.
        else:
            if deltaAngles["L"] <= deltaAngles["R"]:
                self.closeHauled["flag"] = True
                self.closeHauled["chosenSide"] = "left"
                return angleLeftToDeadzone

            self.closeHauled["flag"] = True
            self.closeHauled["chosenSide"] = "right"
            return angleRightToDeadzone

    def boatAtBoarders(self, currCoordinate, boarders):
        if currCoordinate.latitude <= (boarders["down"] + self.boarderMarge):
            return True
        elif currCoordinate.latitude >= (boarders["top"] - self.boarderMarge):
            return True
        elif currCoordinate.longitude <= (boarders["left"] + self.boarderMarge):
            return True
        elif currCoordinate.longitude >= (boarders["right"] - self.boarderMarge):
            return True

        return False

    def forgetCloseHauledCourse(self):
        self.closeHauled["flag"] = True
        self.closeHauled["chosenSide"] = ""

    def windFromDeadzone(self, optimal, wind):
        if AngleHelper.angleIsBetweenAngles(optimal, wind - self.radians45, wind + self.radians45):
            return True
        return False

    def windFromBehind(self, optimal, wind):
        backOfBoatAngle = optimal - AngleHelper.fullRadians / 2

        if AngleHelper.angleIsBetweenAngles(backOfBoatAngle, wind - self.radians45, wind + self.radians45):
            return True
        return False



