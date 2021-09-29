import math as m
from Sailing.coordinate import Coordinate
from Helpers.angleHelper import AngleHelper as ah


def getNearestAngleD(optimalAngle, bestLeft, bestRight):
    if bestLeft > optimalAngle:
        deltaL = abs(optimalAngle + (360 - bestLeft))
    else:
        deltaL = abs(optimalAngle - bestLeft)

    if bestRight < optimalAngle:
        deltaR = abs(optimalAngle - (360 + bestRight))
    else:
        deltaR = abs(optimalAngle - bestRight)

    print(deltaL, deltaR)

    return {"L": deltaL, "R": deltaR}

def hypotenuseAngleToWaypoint(currCoordinate: Coordinate, waypoint: Coordinate):
    """
        Calculates the angle to the next waypoint which is, without any other inputs like wind etc, the most optimal.
        :arg currCoordinate: The current coordinate of the boat
        :arg waypoint: The waypoint which the boat is headed
        :returns: The most optimal angle in radians to next waypoint, without taking into account the wind etc.
    """
    xDelta = waypoint.longitude - currCoordinate.longitude
    yDelta = waypoint.latitude - currCoordinate.latitude
    angle = ah.toDegrees(abs(m.atan(yDelta / xDelta)))
    print(xDelta, yDelta, angle)

    if xDelta > 0:
        if yDelta > 0:
            return 90 - angle
        return 90 + angle
    else:
        if yDelta < 0:
            return 180 + (90 - angle)
        return 270 + angle



def calcAngleInDeadzone(optimalAngle, windAngle):
    sailingCloseHauled = False  # CloseHauled -> 45 graden aan de wind
    closeHauledSide = ""

    angleLeftToDeadzone = (windAngle - 45) % 360
    angleRightToDeadzone = (windAngle + 45) % 360
    deltaAngles = getNearestAngleD(optimalAngle, angleLeftToDeadzone, angleRightToDeadzone)

    # First check if tacking maneuver is needed.
    if deltaAngles["L"] <= 5:
        sailingCloseHauled, closeHauledSide = True, "L"
        return angleLeftToDeadzone
    if deltaAngles["R"] <= 5:
        sailingCloseHauled, closeHauledSide = True, "R"
        return angleRightToDeadzone

    # Check if course was already closeHauled and continue direction. TODO: When to allow the boat to perform tack?
    if sailingCloseHauled:
        if closeHauledSide == "L":
            return angleLeftToDeadzone
        return angleRightToDeadzone

    if deltaAngles["L"] <= deltaAngles["R"]:
        return angleLeftToDeadzone
    return angleRightToDeadzone


print(calcAngleInDeadzone(90, 110))


#print(hypotenuseAngleToWaypoint(Coordinate(6, 7), Coordinate(3, 10)))

#print(getNearestAngleD(135, 45, 135))
