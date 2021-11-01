import time

class PidController:
    def __init__(self, p, i, d):
        self.p = p
        self.i = i
        self.d = d
        self.yI = 0         # startwaarde (integrerende component)
        self.xErrorOld = 0  # om de toename te benaderen
        self.prevTime = time.time()

    def calcNewAngle(self, xSetpoint, xActual):  # setpoint -> wat moet het worden, actual -> wat moet het nu is
        deltaT = self.getDeltaT(time.time())

        xError = xActual - xSetpoint

        yP = self.p * xError

        # Hoe langer de koers niet klopt des te meer de yI gaat spelen -> reageert pas na lange tijd
        self.yI += self.i * xError * deltaT

        # Zorgt voor een snelle aanpassing van de koers (misschien dus laag houden)
        yD = self.d * (xError - self.xErrorOld) / deltaT
        self.xErrorOld = xError

        print(f"error: {xError}, y: {yP + self.yI + yD}, newActual: {xActual - (yP + self.yI + yD)}")
        return yP + self.yI + yD

    def getDeltaT(self, currTime):
        deltaT = currTime - self.prevTime
        self.prevTime = currTime

        return deltaT