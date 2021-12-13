import sys
sys.path.append("../PID")

import Helpers.helperBase as hb
import Helpers.objectToDictHelper as ds
import PID.pid_controller as pc

class RudderHelper(hb.HelperBase, ds.DictSerializer):
    def __init__(self):
        super().__init__()
        self.shouldUpdate = True
        self.pid = pc.PidController(0.5, 0.02, 0.0005)
        self.maxWantedAngle = 35

    def getNewBestAngle(self, currentAngle, wantedAngle):
        newRudderAngle = self.pid.calcNewAngle(currentAngle, wantedAngle)

        if newRudderAngle > self.maxWantedAngle:
            newRudderAngle = self.maxWantedAngle
        elif newRudderAngle < -self.maxWantedAngle:
            newRudderAngle = -self.maxWantedAngle

        return newRudderAngle