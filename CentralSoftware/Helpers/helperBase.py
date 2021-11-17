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
        return tuple(angle % 360 for angle in angles)

    def angleIsBetweenAngles(self, n, left, right):
        """
            Checks for a given angle (n) if it is between an angle of its left and right sight.
        """
        n, left, right = self.reduceAngles(n, left, right)
        if left < right:
            return left <= n <= right
        return n >= left or n <= right

    def windFromDeadzone(self, optimal, wind):
        if self.angleIsBetweenAngles(optimal, wind - 45, wind + 45):
            return True
        return False

    def windFromBehind(self, optimal, wind):
        backOfBoatAngle = optimal - 180

        if self.angleIsBetweenAngles(backOfBoatAngle, wind - 45, wind + 45):
            return True
        return False
