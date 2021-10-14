import math as m
from threading import Thread
from time import sleep

from Route.coordinate import Coordinate
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

boarderMarge = 10
def boatAtBoarders(currCoordinate, boarders):
    if currCoordinate.latitude <= (boarders["down"] + boarderMarge):
        return True
    elif currCoordinate.latitude >= (boarders["top"] - boarderMarge):
        return True
    elif currCoordinate.longitude <= (boarders["left"] + boarderMarge):
        return True
    elif currCoordinate.longitude >= (boarders["right"] - boarderMarge):
        return True

    return False

    # if currCoordinate.longitude(boarders["down"] + boarderMarge)
    #
    # if (boarders["down"] + boarderMarge) >= currCoordinate.latitude >= (boarders["top"] - boarderMarge) \
    #     or (boarders["left"] + boarderMarge) >= currCoordinate.longitude >= (boarders["right"] - boarderMarge):
    #         return True
    # else:
    #     return False

#print(boatAtBoarders(Coordinate(100, 100), {"top": 111,"down": 0,"left": 50,"right": 120}))


#print(calcAngleInDeadzone(90, 110))
#print(hypotenuseAngleToWaypoint(Coordinate(6, 7), Coordinate(3, 10)))
#print(getNearestAngleD(135, 45, 135))

sonarInfinity = 10
def circumnavigateSonarDetection(sonar):
        i = 0 - int(len(sonar) / 2)
        leftAngle = sonarInfinity
        rightAngle = sonarInfinity
        smallestDistance = sonarInfinity
        
        while i < len(sonar) / 2:
            if sonar[i] < sonarInfinity:
                if sonar [i] < smallestDistance:
                    smallestDistance = sonar[i]
                if leftAngle == sonarInfinity:
                    leftAngle = i
                else:
                    rightAngle = i
                
            i = i + 1
        
        return [leftAngle, rightAngle, smallestDistance]

#print(circumnavigateSonarDetection([10, 10, 10, 5, 10, 3, 10, 10, 10, 10]))

class Main:
    def __init__(self, one, two):
        self.one = one
        self.two = two

    def run(self):
        self.one.start()
        self.two.start()

class One(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            print("one")
            sleep(3)

    def a(self):
        print("done")

class Two(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            print("two")
            sleep(3)

main = Main(One(), Two())
main.run()
sleep(2)
main.one.a()