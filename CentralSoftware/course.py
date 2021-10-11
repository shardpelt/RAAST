import sys
sys.path.append("..")
from Route.coordinate import Coordinate
from Helpers.angleHelper import AngleHelper
from CentralData.central_data import CentralData
import math as m

class Course:
    def __init__(self, centralData: CentralData):
        self.data = centralData
        self.wantedAngle = None
        self.radians45 = AngleHelper.toRadians(45)
        self.fullRadians = 2 * m.pi
        self.closeHauled = {"flag":False, "chosenSide":"", "forbiddenSide":""}
        self.tackingAngleMarge = AngleHelper.toRadians(5)
        self.boarderMarge = 0.005
        self.sonarInfinity = 1_000_000

    def update(self, waypoint: Coordinate, boarders: dict):
        """
            :arg waypoint: Coordinate of the current waypoint
            :arg boarders: The absolute boarders in which the boat should stay during the trip
            :returns: The best course angle to set, according to the wind and the current waypoint
        """
        optimalAngle = AngleHelper.hypotenuseAngleToWaypoint(self.data.currentCoordinate, waypoint)

        if self.boatAtBoarders(self.data.currentCoordinate, boarders):
            self.forgetWantedCourse()

        if self.windFromDeadzone(optimalAngle, self.data.wind.angle):
            self.wantedAngle = self.calculateBestAngleInDeadzone(optimalAngle, self.data.wind.angle)

        elif self.windFromBehind(optimalAngle, self.data.wind.angle):
            self.wantedAngle = optimalAngle

    def calculateBestAngleInDeadzone(self, optimalAngle, windAngle):
        angleLeftToDeadzone = windAngle - self.radians45
        angleRightToDeadzone = windAngle + self.radians45
        deltaAngles = AngleHelper.getDifferenceOfAngles(optimalAngle, angleLeftToDeadzone, angleRightToDeadzone)

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
    
    def circumnavigateSonarDetection(self, sonar):
        i = 0 - len(sonar) / 2
        leftAngle = self.sonarInfinity
        rightAngle = self.sonarInfinity
        smallestDistance = self.sonarInfinity
        
        while i < len(sonar) / 2:
            if sonar[i] < self.sonarInfinity:
                if sonar [i] < smallestDistance:
                    smallestDistance = sonar[i]
                if leftAngle == self.sonarInfinity:
                    leftAngle = i
                else:
                    rightAngle = i
                
            i = i + 1
        
        return [leftAngle, rightAngle, smallestDistance]

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

    def forgetWantedCourse(self):
        self.closeHauled["flag"] = True
        self.closeHauled["chosenSide"] = ""

    def windFromDeadzone(self, optimal, wind):
        if AngleHelper.betweenAngles(optimal, wind - self.radians45, wind + self.radians45):
            return True
        return False

    def windFromBehind(self, optimal, wind):
        backOfBoatAngle = optimal - AngleHelper.fullRadians / 2

        if AngleHelper.betweenAngles(backOfBoatAngle, wind - self.radians45, wind + self.radians45):
            return True
        return False


    def checkCurrentCourse(self):
        pass
