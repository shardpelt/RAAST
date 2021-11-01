from Helpers.helperBase import HelperBase
from PID.pid_controller import PidController

class RudderHelper(HelperBase):
    def __init__(self):
        super().__init__()
        self.pid = PidController(0.5, 0.02, 0.0005)

    def getNewBestAngle(self, wantedAngle, currentAngle):
        return self.pid.calcNewAngle(wantedAngle, currentAngle)
