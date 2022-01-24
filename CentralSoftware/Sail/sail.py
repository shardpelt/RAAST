import sys
sys.path.append("..")

import Helpers.helper_base as hb

class Sail:
    def __init__(self):
        self._helperBase = hb.HelperBase()
        self.isUpdatable = True
        self.isControllable = True
        self.wantedAngle = 0

    def setNewBestAngle(self, relativeWindAngle):
        """
            Needs the boatAngle to calculate the absolute angle of the wind
            The difference of the boatAngle according to the absolute wind angle is divided by 2 to find the ideal sail angle
        """
        relativeWindAngle = self._helperBase.reduceAngles(relativeWindAngle)

        if relativeWindAngle <= 180:
            self.wantedAngle = -(relativeWindAngle / 2)
        else:
            self.wantedAngle = 90 - (relativeWindAngle / 2) % 90