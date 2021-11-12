from Helpers.angleHelper import AngleHelper
from Helpers.helperBase import HelperBase
from PID.pid_controller import PidController

class RudderHelper(HelperBase):
    # TODO: Actuator scalen naar maximale hoeken? Wat is de maximale hoek waar je je roer in wilt hebben
    def __init__(self):
        super().__init__()
        self.actuatorAngleRange = AngleHelper.toRadians(180)
        self.pid = PidController(0.5, 0.02, 0.0005)

    def getNewBestAngle(self, currentAngle, wantedAngle):
        rudderAngle = self.pid.calcNewAngle(currentAngle, wantedAngle)
        print(f"- rudderAngle: {AngleHelper.toDegrees(rudderAngle)}")

        # Calculate the angle of the actuator -> 0 degrees is fully right and totalMovementAngel is fully left
        if rudderAngle <= 0:
            actuatorAngle = self.actuatorAngleRange / 2 + abs(rudderAngle)
        else:
            actuatorAngle = self.actuatorAngleRange / 2 - abs(rudderAngle)

        print(f"- actuatorAngle: {AngleHelper.toDegrees(actuatorAngle)}")
        return actuatorAngle

# h = RudderHelper()
# h.getNewBestAngle(AngleHelper.toRadians(0), AngleHelper.toRadians(181))