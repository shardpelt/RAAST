import sys
sys.path.append("..")

import time
import Helpers.objectToDictHelper as ds


class PidController(ds.DictSerializer):
    def __init__(self, p, i, d):
        self.p = p
        self.i = i
        self.d = d
        self.yI = 0                 # startwaarde (integrerende component)
        self.errorOld = 0           # om de toename te benaderen
        self.prevTime = None

    def calcNewAngle(self, actual, setpoint):
        deltaT = self.getDeltaT(time.time())

        error = self.calcError(actual, setpoint)

        yP = self.p * error

        # Hoe langer de koers niet klopt des te meer de yI gaat spelen -> reageert pas na lange tijd
        self.yI += self.i * error * deltaT

        # Zorgt voor een snelle aanpassing van de koers (misschien dus laag houden)
        yD = self.d * (error - self.errorOld) / deltaT
        self.errorOld = error

        angle = yP + self.yI + yD

        return angle

    def getDeltaT(self, currTime):
        if self.prevTime is None:
            return 0.001

        deltaT = currTime - self.prevTime
        self.prevTime = currTime
        return deltaT

    @staticmethod
    def calcError(actual, setpoint):
        if abs(setpoint - actual) > 180:
            if actual < setpoint:
                error = (0 - actual) - (360 - setpoint)
            else:
                error = (360 - actual) + setpoint
        else:
            error = setpoint - actual

        return error

    def reset(self):
        self.yI = None
        self.errorOld = None
        self.prevTime = None