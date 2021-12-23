import sys
sys.path.append("..")

import Helpers.helper_base as hb
import Rudder.Pid.pid_controller as pc

class Rudder(hb.HelperBase):
    def __init__(self):
        super().__init__()
        self.isUpdatable = True
        self.wantedAngle = 0
        self.pid = pc.PidController(0.5, 0.02, 0.0005)
        self.maxWantedAngle = 35

    def setNewBestAngle(self, currentAngle, wantedAngle) -> None:
        newRudderAngle = self.pid.calcNewAngle(currentAngle, wantedAngle)

        if newRudderAngle > self.maxWantedAngle:
            newRudderAngle = self.maxWantedAngle
        elif newRudderAngle < -self.maxWantedAngle:
            newRudderAngle = -self.maxWantedAngle

        self.wantedAngle = newRudderAngle