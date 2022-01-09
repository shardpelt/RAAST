import sys
sys.path.append("..")

import time as tm
import Helpers.angle_helper as ah
import Enums.course_sides_enum as se

class Tacking:
    def __init__(self, sailingToTheWind):
        self._angleHelper = ah.AngleHelper()
        self.inManeuver = False
        self.timeManeuverStarted = 0
        self.timesManeuverTried = 0
        self.sailingToTheWind = sailingToTheWind
        self.tackingAngleMarge = 0
        self.maxSecondsToTry = 15

    def startManeuver(self) -> None:
        self.stopManeuver()

        self.inManeuver = True
        self.timeManeuverStarted = tm.time()

    def stopManeuver(self) -> None:
        self.inManeuver = False
        self.timeManeuverStarted = 0
        self.timesManeuverTried = 0

    def isCompleted(self, currentAngle, wantedAngle) -> bool:
        if self.sailingToTheWind == se.Side.Left:
            return self._angleHelper.angleIsBetweenAngles(currentAngle, wantedAngle - 10, wantedAngle)
        else:
            return self._angleHelper.angleIsBetweenAngles(currentAngle, wantedAngle, wantedAngle + 10)

    def passedTimeLimit(self) -> bool:
        return (self.timeManeuverStarted + self.maxSecondsToTry) < tm.time()

    def triedManeuver(self) -> None:
        self.timesManeuverTried += 1
        self.timeManeuverStarted = tm.time()