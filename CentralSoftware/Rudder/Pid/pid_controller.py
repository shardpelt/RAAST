import sys
sys.path.append("..")

import time as tm
import Helpers.helper_base as hb

class PidController:
    def __init__(self, p, i, d):
        self.p = p
        self.i = i
        self.d = d
        self.yI = 0                 # startwaarde (integrerende component)
        self.errorOld = 0           # om de toename te benaderen
        self.prevTime = None
        self._helperBase = hb.HelperBase()

    def calcNewAngle(self, actual, setpoint, windToNorth, tackingAllowed):
        deltaT = self.getDeltaT(tm.time())

        error = self.calcError(actual, setpoint, windToNorth, tackingAllowed)

        yP = self.p * error

        # Hoe langer de koers niet klopt des te meer de yI gaat spelen -> reageert pas na lange tijd
        self.yI += self.i * error * deltaT

        # Zorgt voor een snelle aanpassing van de koers (misschien dus laag houden)
        yD = self.d * (error - self.errorOld) / deltaT
        self.errorOld = error

        angle = yP + self.yI + yD

        return angle

    def calcError(self, actual, setpoint, windToNorth, tackingAllowed):
        if tackingAllowed:
            if abs(setpoint - actual) > 180:
                if actual < setpoint:
                    error = (0 - actual) - (360 - setpoint)
                else:
                    error = (360 - actual) + setpoint
            else:
                error = setpoint - actual
        else:
            if self._helperBase.angleIsBetweenAngles(windToNorth, actual, setpoint):  # Deadzone kruist aan rechterkant -> traverse links
                if actual < setpoint:
                    error = (0 - actual) - (360 - setpoint)
                else:
                    error = setpoint - actual
            elif self._helperBase.angleIsBetweenAngles(windToNorth, setpoint, actual):  # Deadzone kruist aan linkerkant -> traverse rechts
                if setpoint < actual:
                    error = (360 - actual) + setpoint
                else:
                    error = setpoint - actual

        return error

    def getDeltaT(self, currTime):
        if self.prevTime is None:
            return 0.001

        deltaT = currTime - self.prevTime
        self.prevTime = currTime
        return deltaT