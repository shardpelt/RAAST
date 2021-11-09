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
            deltaL = abs(mainAngle + (2 * m.pi - leftAngle))
        else:
            deltaL = abs(mainAngle - leftAngle)

        if rightAngle < mainAngle:
            deltaR = abs(mainAngle - (2 * m.pi + rightAngle))
        else:
            deltaR = abs(mainAngle - rightAngle)

        return {"L": deltaL, "R": deltaR}

    @staticmethod
    def calcRhumbLine(current: Coordinate, waypoint: Coordinate):
        """
            :arg current: Current coordinate of the boat
            :arg waypoint: Current waypoint of the boat
            :returns: The angle to the next waypoint, in accordance to the 'loxodroom' formula
        """
        deltaWidth = m.log(m.tan(waypoint.latitude/2 + m.pi/4)/m.tan(current.latitude/2 + m.pi/4))
        return m.atan2(deltaWidth, waypoint.longitude - current.longitude)


    def hypotenuseAngleToWaypoint(self, current: Coordinate, waypoint: Coordinate):
        """
            USE CALCRHUMBLINE INSTEAD
        """
        xDelta = waypoint.longitude - current.longitude
        yDelta = waypoint.latitude - current.latitude
        return m.atan2(yDelta, xDelta)
