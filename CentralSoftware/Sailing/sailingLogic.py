import sys
sys.path.append("..")
from Sailing.coordinate import Coordinate
from Helpers.angleHelper import AngleHelper
import math as m

class SailingLogic:
    def __init__(self):
        self.radians45 = AngleHelper.toRadians(45)
        self.fullRadians = 2 * m.pi
        self.sailingCloseHauled = False # CloseHauled -> 45 graden aan de wind
        self.closeHauledSide = ""

    def getBestCourseAngle(self, currCoordinate: Coordinate, waypoint: Coordinate, windAngle: float):
        """
            :arg currCoordinate: Coordinate of the boat
            :arg waypoint: Coordinate of the current waypoint
            :arg windAngle: The radians at which the wind is blowing in relation to North
            :returns: The best course angle to set, according to the wind and the current waypoint
        """
        optimalAngle = AngleHelper.hypotenuseAngleToWaypoint(currCoordinate, waypoint)

        if self.windFromDeadzone(optimalAngle, windAngle):
            return self.calcAngleInDeadzone(optimalAngle, windAngle)

        elif self.windFromBehind(optimalAngle, windAngle):
            pass

        return optimalAngle


    def calcAngleInDeadzone(self, optimalAngle, windAngle):
        angleLeftToDeadzone = (windAngle - self.radians45) % self.fullRadians
        angleRightToDeadzone = (windAngle + self.radians45) % self.fullRadians
        deltaAngles = AngleHelper.getDifferenceOfAngles(optimalAngle, angleLeftToDeadzone, angleRightToDeadzone)

        print(angleLeftToDeadzone, angleRightToDeadzone, deltaAngles)

        # First check if tacking maneuver is needed.
        if deltaAngles["L"] <= 5:
            self.sailingCloseHauled, self.closeHauledSide = True, "L"
            return angleLeftToDeadzone
        if deltaAngles["R"] <= 5:
            self.sailingCloseHauled, self.closeHauledSide = True, "R"
            return angleRightToDeadzone

        # Check if course was already closeHauled and continue direction. TODO: When to allow the boat to perform tack?
        if self.sailingCloseHauled:
            if self.closeHauledSide == "L":
                return angleLeftToDeadzone
            return angleRightToDeadzone

        if deltaAngles["L"] <= deltaAngles["R"]:
            self.sailingCloseHauled, self.closeHauledSide = True, "L"
            return angleLeftToDeadzone
        self.sailingCloseHauled, self.closeHauledSide = True, "R"
        return angleRightToDeadzone


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
# print(AngleHelper.toDegrees(sl.getBestCourseAngle(Coordinate(5, 3), Coordinate(3, 10), AngleHelper.toRadians(90))))
# print(AngleHelper.toDegrees(sl.getBestCourseAngle(Coordinate(7, 5), Coordinate(3, 10), AngleHelper.toRadians(90))))
# print(AngleHelper.toDegrees(sl.getBestCourseAngle(Coordinate(9, 7), Coordinate(3, 10), AngleHelper.toRadians(90))))
