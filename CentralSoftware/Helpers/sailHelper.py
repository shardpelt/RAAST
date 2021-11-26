from Helpers.helperBase import HelperBase
from Helpers.interpolator import Interpolator

class SailHelper(HelperBase):
    def __init__(self):
        super().__init__()
        self.shouldUpdate = True
        self.windRightToSail = [{"wind": 0, "sail": -10, "interpolate": False}, {"wind": 90, "sail": -10, "interpolate": True}, {"wind": 135, "sail": -45, "interpolate": True}, {"wind": 180, "sail": -90, "interpolate": None}]
        self.windLeftToSail = [{"wind": 180, "sail": 90, "interpolate": True}, {"wind": 225, "sail": 45, "interpolate": True}, {"wind": 270, "sail": 10, "interpolate": False}, {"wind": 360, "sail": 10, "interpolate": None}]

    @staticmethod
    def getNewBestAngle(boatAngle, relativeWindAngle):
        """
            Needs the boatAngle to calculate the absolute angle of the wind
            The difference of the boatAngle according to the absolute wind angle is divided by 2 to find the ideal sail angle
        """
        absWindAngle = (boatAngle + relativeWindAngle)

        sailAngle = (absWindAngle - boatAngle) / 2
        if relativeWindAngle <= 180:
            return -sailAngle
        else:
            return 90 - sailAngle % 90

    # Wind according to the boat's angle
    def getNewBestAngleInterpolated(self, relativeWindAngle):
        windToSail = self.windRightToSail if 0 <= relativeWindAngle <= 180 else self.windLeftToSail
        for i, windSail in enumerate(windToSail):
            if windSail["wind"] <= relativeWindAngle <= windToSail[i + 1]["wind"]:
                if windSail["interpolate"]:
                    return Interpolator.getSail(windSail, windToSail[i + 1], relativeWindAngle)
                return windSail["sail"]

sh = SailHelper()
print(sh.getNewBestAngle(0, 90))