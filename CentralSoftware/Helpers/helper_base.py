import math as m

class HelperBase:
    @staticmethod
    def toRadians(degrees):
        return degrees * (m.pi / 180)

    @staticmethod
    def toDegrees(radians):
        return radians * (180 / m.pi)

    @staticmethod
    def reduceAngles(*angles):
        """
            Makes sure that for every angle as input, the angle is between 0 and 360 degrees
        """
        if len(angles) == 1:
            return angles[0] % 360
        return tuple(angle % 360 for angle in angles)

    def angleIsBetweenAngles(self, angle, left, right):
        """
            Checks for a given angle (n) if it is between an angle of its left and right sight.
        """
        angle, left, right = self.reduceAngles(angle, left, right)
        if left < right:
            return left <= angle <= right
        return angle >= left or angle <= right

    def windFromDeadzone(self, optimalSailingAngle, wind):
        return self.angleIsBetweenAngles(optimalSailingAngle, wind.toNorth - 45, wind.toNorth + 45)

    def windFromBehind(self, optimal, wind):
        backOfBoatAngle = optimal - 180

        if self.angleIsBetweenAngles(backOfBoatAngle, wind - 45, wind + 45):
            return True
        return False
