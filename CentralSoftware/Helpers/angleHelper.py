import math as m
from Sailing.coordinate import Coordinate

class AngleHelper:

    @staticmethod
    def toRadians(degrees):
        return degrees * (m.pi / 180)

    @staticmethod
    def toDegrees(radians):
        return radians * (180 / m.pi)

    @staticmethod
    def betweenAngles(left, n, right):
        """
            Check if angle n is between a left and right angle
        """
        if left < right:
            return left <= n <= right
        return n >= left or n <= right

    @staticmethod
    def getDifferenceOfAngles(mainAngle, leftAngle, rightAngle):
        if leftAngle >= mainAngle:
            deltaL = abs(mainAngle + (2 * m.pi - leftAngle))
        else:
            deltaL = abs(mainAngle - leftAngle)

        if rightAngle < mainAngle:
            deltaR = abs(mainAngle - (2 * m.pi + rightAngle))
        else:
            deltaR = abs(mainAngle - rightAngle)

        return {"L": deltaL, "R": deltaR}


    @staticmethod
    def hypotenuseAngleToWaypoint(currCoordinate: Coordinate, waypoint: Coordinate):
        """
            Calculates the angle to the next waypoint which is, without any other inputs like wind etc, the most optimal.
            :arg currCoordinate: The current coordinate of the boat
            :arg waypoint: The waypoint which the boat is headed
            :returns: The most optimal angle in radians to next waypoint, without taking into account the wind etc.
        """
        xDelta = waypoint.longitude - currCoordinate.longitude
        yDelta = waypoint.latitude - currCoordinate.latitude
        angle = abs(m.atan(yDelta / xDelta))

        if xDelta > 0:
            if yDelta > 0:
                return AngleHelper.toRadians(90) - angle
            return AngleHelper.toRadians(90) + angle
        else:
            if yDelta < 0:
                return AngleHelper.toRadians(180) + (90 - angle)
            return AngleHelper.toRadians(270) + angle
