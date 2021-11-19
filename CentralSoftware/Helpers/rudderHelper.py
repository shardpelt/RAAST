from Helpers.helperBase import HelperBase
from PID.pid_controller import PidController

class RudderHelper(HelperBase):
    def __init__(self):
        super().__init__()
        self.pid = PidController(0.5, 0.02, 0.0005)
        self.maxWantedAngle = 45

    def getNewBestAngle(self, currentAngle, wantedAngle):
        rudderAngle = self.pid.calcNewAngle(currentAngle, wantedAngle)

        if rudderAngle > self.maxWantedAngle:
            rudderAngle = self.maxWantedAngle
        elif rudderAngle < -self.maxWantedAngle:
            rudderAngle = -self.maxWantedAngle

        return rudderAngle


# h = RudderHelper(5)
# h.getNewBestAngle(179, 0)