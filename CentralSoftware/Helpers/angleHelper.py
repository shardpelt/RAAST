import math as m
from Helpers.helperBase import HelperBase
from Route.coordinate import Coordinate

class AngleHelper(HelperBase):
    def __init__(self):
        super().__init__()

    def getDeltaLeftAndRightToAngle(self, mainAngle, leftAngle, rightAngle):
        """
            :arg mainAngle: The angle of which the deltas should be calculated
            :arg leftAngle: The angle left to the mainAngle
            :arg rightAngle: The angle right to the mainAngle
            :returns: The difference between mainAngle and left/right angle, used for determing nearest direction to sail at
        """
        mainAngle, leftAngle, rightAngle = self.reduceAngles(mainAngle, leftAngle, rightAngle)
        if leftAngle >= mainAngle:
            deltaL = abs(mainAngle + (360 - leftAngle))
        else:
            deltaL = abs(mainAngle - leftAngle)

        if rightAngle < mainAngle:
            deltaR = abs(mainAngle - (360 + rightAngle))
        else:
            deltaR = abs(mainAngle - rightAngle)

        return {"left": deltaL, "right": deltaR}

    def calcAngleBetweenCoordinates(self, current: Coordinate, waypoint: Coordinate):
        """
            TODO: Check if correct
            :arg current: Current coordinate of the boat
            :arg waypoint: Current waypoint of the boat
            :returns: The angle to the next waypoint, in accordance to the 'loxodroom' formula
        """
        deltaWidth = m.log(m.tan(self.toRadians(waypoint.latitude/2) + m.pi/4)/m.tan(self.toRadians(current.latitude/2) + m.pi/4))
        k = self.toDegrees(m.atan2(self.toRadians(waypoint.longitude) - self.toRadians(current.longitude), deltaWidth))

        return k % 360

    def hypotenuseAngleToWaypoint(self, current: Coordinate, waypoint: Coordinate):
        """
            USE calcAngleBetweenCoordinates INSTEAD
        """
        xDelta = waypoint.longitude - current.longitude
        yDelta = waypoint.latitude - current.latitude
        return m.atan2(yDelta, xDelta)

# h = AngleHelper()
# print(h.calcAngleBetweenCoordinates(Coordinate(0, 0), Coordinate(1, 5)))