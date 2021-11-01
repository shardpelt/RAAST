import math as m
from Helpers.helperBase import HelperBase
from Route.coordinate import Coordinate

class AngleHelper(HelperBase):
    def __init__(self):
        super().__init__()

    def getDeltaLeftAndRightToAngle(self, mainAngle, leftAngle, rightAngle):
        """
            Computes the difference between the mainAngle and the left/right angle
            This method is used to determine which angle is best to set course at
        """
        mainAngle, leftAngle, rightAngle = self.reduceAngles(mainAngle, leftAngle, rightAngle)
        if leftAngle >= mainAngle:
            deltaL = abs(mainAngle + (2 * m.pi - leftAngle))
        else:
            deltaL = abs(mainAngle - leftAngle)

        if rightAngle < mainAngle:
            deltaR = abs(mainAngle - (2 * m.pi + rightAngle))
        else:
            deltaR = abs(mainAngle - rightAngle)

        return {"L": deltaL, "R": deltaR}

    def hypotenuseAngleToWaypoint(self, currCoordinate: Coordinate, waypoint: Coordinate):
        """
            Calculates the angle to the next waypoint which is, without any other inputs like wind etc, the most optimal.
            :arg currCoordinate: The current coordinate of the boat
            :arg waypoint: The waypoint which the boat is headed
            :returns: The most optimal angle in radians to next waypoint, without taking into account the wind etc.
        """
        xDelta = waypoint.longitude - currCoordinate.longitude
        yDelta = waypoint.latitude - currCoordinate.latitude
        return m.atan2(yDelta, xDelta)
