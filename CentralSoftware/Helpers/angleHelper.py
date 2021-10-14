import math as m
from Route.coordinate import Coordinate

class AngleHelper:
    fullRadians = 2 * m.pi
    fullDegrees = 360

    @staticmethod
    def toRadians(degrees):
        return degrees * (m.pi / 180)

    @staticmethod
    def toDegrees(radians):
        return radians * (180 / m.pi)

    def reduceAngles(*angles):
        """
            Makes sure that for every angle as input, the angle is between 0 and 2pi radians
        """
        return tuple(angle % AngleHelper.fullRadians for angle in angles)

    @staticmethod
    def angleIsBetweenAngles(n, left, right):
        """
            Checks for a given angle (n) if it is between an angle of its left and right sight.
        """
        n, left, right = AngleHelper.reduceAngles(n, left, right)
        if left < right:
            return left <= n <= right
        return n >= left or n <= right

    @staticmethod
    def getDeltasOfLeftAndRight(mainAngle, leftAngle, rightAngle):
        """
            Computes the difference between the mainAngle and the left/right angle
            This method is used to determine which angle is best to set course at
        """
        mainAngle, leftAngle, rightAngle = AngleHelper.reduceAngles(mainAngle, leftAngle, rightAngle)
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
