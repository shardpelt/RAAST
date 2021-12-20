import sys
sys.path.append("..")

import math as m
import Helpers.helperBase as hb
import Route.coordinate as co

class AngleHelper(hb.HelperBase):
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

    def calcAngleBetweenCoordinates(self, current: co.Coordinate, headed: co.Coordinate):
        """
            Note: Delta of latitude and longitude can max be 90
            :arg current: Current coordinate of the boat
            :arg headed: Headed coordinate
            :returns: The angle to the next waypoint, in accordance to the 'loxodroom' formula
        """
        cLong = current.longitude * -1
        hLong = headed.longitude * -1
        deltaWidth = m.log(m.tan(self.toRadians(headed.latitude)/2 + m.pi/4)/m.tan(self.toRadians(current.latitude)/2 + m.pi/4))
        k = self.toDegrees(m.atan2(self.toRadians(hLong) - self.toRadians(cLong), deltaWidth))

        return k % 360

    def hypotenuseAngleToWaypoint(self, current: co.Coordinate, waypoint: co.Coordinate):
        """
            USE calcAngleBetweenCoordinates INSTEAD
        """
        xDelta = waypoint.longitude - current.longitude
        yDelta = waypoint.latitude - current.latitude
        return m.atan2(yDelta, xDelta)