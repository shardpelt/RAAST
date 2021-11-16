from Helpers.angleHelper import AngleHelper
import time
from Helpers.helperBase import HelperBase

class PidController:
    def __init__(self, p, i, d, sleepTime):
        self.p = p
        self.i = i
        self.d = d
        self.yI = 0                 # startwaarde (integrerende component)
        self.errorOld = 0           # om de toename te benaderen
        self.prevTime = None
        self.sleepTime = sleepTime

    def calcNewAngle(self, actual, setpoint):
        deltaT = self.getDeltaT(time.time())

        error = self.calcError(actual, setpoint)
        print(f"- error: {AngleHelper.toDegrees(error)}")

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
            self.prevTime = currTime - self.sleepTime

        deltaT = currTime - self.prevTime
        self.prevTime = currTime
        return deltaT

    @staticmethod
    def calcError(actual, setpoint):
        if abs(setpoint - actual) > AngleHelper.toRadians(180):
            if actual < setpoint:
                error = (0 - actual) - (HelperBase.fullRadians - setpoint)
            else:
                error = (HelperBase.fullRadians - actual) + setpoint
        else:
            error = setpoint - actual

        return error

    def reset(self):
        self.yI = None
        self.errorOld = None
        self.prevTime = None


# pid = PidController(0.5, 0.02, 0.0005, 5)
#
# print(pid.calcNewAngle(AngleHelper.toRadians(5), AngleHelper.toRadians(355)))
#

# # err = pid.calcError(AngleHelper.toRadians(5), AngleHelper.toRadians(355))
# # print(AngleHelper.toDegrees(err))