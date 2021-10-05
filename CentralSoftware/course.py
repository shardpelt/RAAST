import sys
sys.path.append("..")
from Route.coordinate import Coordinate
from Helpers.angleHelper import AngleHelper
import math as m

class Course:
    def __init__(self):
        self.wantedAngle = None
        self.radians45 = AngleHelper.toRadians(45)
        self.fullRadians = 2 * m.pi
        self.sailingCloseHauled = False # CloseHauled -> 45 graden aan de wind
        self.closeHauledSide = ""
        self.tackingAngleMarge = AngleHelper.toRadians(5)
        self.boarderMarge = 0.005
        self.sonarInfinity = 1_000_000

    def calculateBestAngle(self, currCoordinate: Coordinate, waypoint: Coordinate, windAngle: float, boarders: dict):
        """
            :arg currCoordinate: Coordinate of the boat
            :arg waypoint: Coordinate of the current waypoint
            :arg windAngle: The radians at which the wind is blowing in relation to North
            :arg boarders: The absolute boarders in which the boat should stay during the trip
            :returns: The best course angle to set, according to the wind and the current waypoint
        """
        optimalAngle = AngleHelper.hypotenuseAngleToWaypoint(currCoordinate, waypoint)

        if self.boatAtBoarders(currCoordinate, boarders):
            self.forgetWantedCourse()

        if self.windFromDeadzone(optimalAngle, windAngle):
            self.wantedAngle = self.calculateBestAngleInDeadzone(optimalAngle, windAngle)

        elif self.windFromBehind(optimalAngle, windAngle):
            self.wantedAngle = optimalAngle



    def calculateBestAngleInDeadzone(self, optimalAngle, windAngle):
        angleLeftToDeadzone = (windAngle - self.radians45) % self.fullRadians
        angleRightToDeadzone = (windAngle + self.radians45) % self.fullRadians
        deltaAngles = AngleHelper.getDifferenceOfAngles(optimalAngle, angleLeftToDeadzone, angleRightToDeadzone)

        print(angleLeftToDeadzone, angleRightToDeadzone, deltaAngles)

        # If already sailing closeHauled try to continue direction chosen or perform tacking maneuvre
        if self.sailingCloseHauled:

            # Check if angle to waypoint is 90 degrees -> perform tack maneuvre
            if deltaAngles["L"] <= self.tackingAngleMarge:
                self.sailingCloseHauled, self.closeHauledSide = True, "L"
                return angleLeftToDeadzone
            elif deltaAngles["R"] <= self.tackingAngleMarge:
                self.sailingCloseHauled, self.closeHauledSide = True, "R"
                return angleRightToDeadzone
            else:
                if self.closeHauledSide == "L":
                    return angleLeftToDeadzone
                return angleRightToDeadzone

        # If not already sailing closeHauled, check which angle from deadzone is best to sail at.
        else:
            if deltaAngles["L"] <= deltaAngles["R"]:
                self.sailingCloseHauled, self.closeHauledSide = True, "L"
                return angleLeftToDeadzone

            self.sailingCloseHauled, self.closeHauledSide = True, "R"
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
        self.sailingCloseHauled = False
        self.closeHauledSide = ""

    def windFromDeadzone(self, optimal, wind):
        if AngleHelper.betweenAngles((wind - self.radians45) % self.fullRadians, optimal, (wind + self.radians45) % self.fullRadians):
            return True
        return False

    def windFromBehind(self, optimal, wind):
        backOfBoatAngle = (optimal - m.pi) % 2 * m.pi

        if AngleHelper.betweenAngles((wind - self.radians45) % self.fullRadians, backOfBoatAngle, (wind + self.radians45) % self.fullRadians):
            return True
        return False


# sl = SailingLogic()
#
# print(AngleHelper.toDegrees(sl.getBestCourseAngle(Coordinate(3, 1), Coordinate(3, 10), AngleHelper.toRadians(90))))
# print(AngleHelper.toDegrees(sl.getBestCourseAngle(Coordinate(5, 3), Coordinate(3, 10), AngleHelper.toRadians(50))))
# print(AngleHelper.toDegrees(sl.getBestCourseAngle(Coordinate(7, 5), Coordinate(3, 10), AngleHelper.toRadians(90))))
# print(AngleHelper.toDegrees(sl.getBestCourseAngle(Coordinate(9, 7), Coordinate(3, 10), AngleHelper.toRadians(90))))
