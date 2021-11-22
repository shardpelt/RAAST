from Helpers.helperBase import HelperBase
from PID.pid_controller import PidController

class RudderHelper(HelperBase):
    def __init__(self):
        super().__init__()
        self.shouldUpdate = True
        self.pid = PidController(0.5, 0.02, 0.0005)
        self.maxWantedAngle = 45

    def getNewBestAngle(self, currentAngle, wantedAngle):
        newRudderAngle = self.pid.calcNewAngle(currentAngle, wantedAngle)

        if newRudderAngle > self.maxWantedAngle:
            newRudderAngle = self.maxWantedAngle
        elif newRudderAngle < -self.maxWantedAngle:
            newRudderAngle = -self.maxWantedAngle

        return newRudderAngle


# h = RudderHelper(5)
# h.getNewBestAngle(179, 0)