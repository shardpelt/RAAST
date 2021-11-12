import math as m

class HelperBase:
    fullRadians = 2 * m.pi
    radians45 = 45 * (m.pi / 180)

    @staticmethod
    def toRadians(degrees):
        return degrees * (m.pi / 180)

    @staticmethod
    def toDegrees(radians):
        return radians * (180 / m.pi)

    def reduceAngles(self, *angles):
        """
            Makes sure that for every angle as input, the angle is between 0 and 2pi radians
        """
        return tuple(angle % self.fullRadians for angle in angles)

    def angleIsBetweenAngles(self, n, left, right):
        """
            Checks for a given angle (n) if it is between an angle of its left and right sight.
        """
        n, left, right = self.reduceAngles(n, left, right)
        if left < right:
            return left <= n <= right
        return n >= left or n <= right

    def windFromDeadzone(self, optimal, wind):
        if self.angleIsBetweenAngles(optimal, wind - self.radians45, wind + self.radians45):
            return True
        return False

    def windFromBehind(self, optimal, wind):
        backOfBoatAngle = optimal - self.fullRadians / 2

        if self.angleIsBetweenAngles(backOfBoatAngle, wind - self.radians45, wind + self.radians45):
            return True
        return False
