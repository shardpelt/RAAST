import sys
sys.path.append("..")

import Helpers.helper_base as hb
import Helpers.interpolator as ip

class Sail(hb.HelperBase):
    def __init__(self):
        super().__init__()
        self.isUpdatable = True
        self.wantedAngle = 0
        self.windRightToSail = [{"wind": 0, "sail": -10, "interpolate": False}, {"wind": 90, "sail": -10, "interpolate": True}, {"wind": 135, "sail": -45, "interpolate": True}, {"wind": 180, "sail": -90, "interpolate": None}]
        self.windLeftToSail = [{"wind": 180, "sail": 90, "interpolate": True}, {"wind": 225, "sail": 45, "interpolate": True}, {"wind": 270, "sail": 10, "interpolate": False}, {"wind": 360, "sail": 10, "interpolate": None}]

    def setNewBestAngle(self, relativeWindAngle):
        """
            Needs the boatAngle to calculate the absolute angle of the wind
            The difference of the boatAngle according to the absolute wind angle is divided by 2 to find the ideal sail angle
        """
        relativeWindAngle = self.reduceAngles(relativeWindAngle)

        if relativeWindAngle <= 180:
            self.wantedAngle = -(relativeWindAngle / 2)
        else:
            self.wantedAngle = 90 - (relativeWindAngle / 2) % 90


    # Wind according to the boat's angle
    def getNewBestAngleInterpolated(self, relativeWindAngle):
        windToSail = self.windRightToSail if 0 <= relativeWindAngle <= 180 else self.windLeftToSail
        for i, windSail in enumerate(windToSail):
            if windSail["wind"] <= relativeWindAngle <= windToSail[i + 1]["wind"]:
                if windSail["interpolate"]:
                    return ip.Interpolator.getSail(windSail, windToSail[i + 1], relativeWindAngle)
                return windSail["sail"]