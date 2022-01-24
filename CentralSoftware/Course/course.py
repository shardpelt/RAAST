import sys
sys.path.append("..")

import Route.boarders as bo
import Route.waypoint as wp
import Course.tacking as ta
import Enums.course_sides_enum as se
import Helpers.angle_helper as ah

"""
    The course class is used to calculate the best angle to set sail at.
    This is done according to the current waypoint, wind angle and setted route boarders
    
    First the optimalCourseAngle is calculated, this angle is the fastest/direct angle to the current waypoint
    Then we check if this optimalCourseAngle lies between the sailing deadzone (wind +- 45 degrees)
        - If not then the optimalCourseAngle is set as the wantedCourseAngle 
        - If it lies in the deadzone the side which lies closest to the optimalCourseAngle is chosen as wantedCourseAngle
            - Then this side of sailingToTheWind course is hold until the current waypoint lies out of the deadzone which goes by traversing the side until the angle 
               to the waypoint is 90 degrees (The optimalCourseAngle is then chosen by itself because the boat traversed out of the deadzone)
"""

class Course:
    def __init__(self, boat):
        self._boat = boat
        self._angleHelper = ah.AngleHelper()
        self.isUpdatable = True
        self.optimalCourseAngle = None
        self.wantedCourseAngle = None
        self.wantedCourseAngleMarge = 0
        self.sailingToTheWind = None
        self.cantChooseSide = None
        self.wasAcrossBoarders = False
        self.tacking = ta.Tacking(self.sailingToTheWind)

    def isOffTrack(self) -> bool:
        return not self._angleHelper.angleIsBetweenAngles(self._boat.sensors.compass.angle, self.wantedCourseAngle - self.wantedCourseAngleMarge, self.wantedCourseAngle + self.wantedCourseAngleMarge)

    def forgetDeadzoneFlags(self) -> None:
        self.sailingToTheWind = None
        self.cantChooseSide = None
        self.tacking.stopManeuver()

    def updateWantedAngle(self, waypoint: wp.Waypoint) -> None:
        """
            arg waypoint: The current waypoint
            :returns: The best course angle to set, according to the wind and the current waypoint
        """
        self.optimalCourseAngle = self._angleHelper.calcAngleBetweenCoordinates(self._boat.sensors.gps.coordinate, waypoint.coordinate)

        if self.boatAcrossBoarders(self._boat.route.boarders) and not self.wasAcrossBoarders:
            self.forgetDeadzoneFlags()
            self.tacking.startManeuver()
            self.wasAcrossBoarders = True
        else:
            self.wasAcrossBoarders = False

        # If wind blows from deadzone choose the shortest side to sail at
        if self._angleHelper.windFromDeadzone(self.optimalCourseAngle, self._boat.sensors.wind):
            self.wantedCourseAngle = self.calcBestAngleWindFromDeadzone(self.optimalCourseAngle)
        else:
            # If the boat was not previously sailing to the wind, a tacking maneuver is not tried
            self.wantedCourseAngle = self.optimalCourseAngle

            # If boat was sailing to the wind, then a tacking maneuver is tried to achieve the fastest path
            if self.sailingToTheWind:
                self.forgetDeadzoneFlags()
                self.tacking.startManeuver()

        self.checkTackingManeuver()

    def checkTackingManeuver(self) -> None:
        if self.tacking.inManeuver:
            if self.tacking.isCompleted(self._boat.sensors.compass.angle, self.wantedCourseAngle):
                self.tacking.stopManeuver()
            elif self.tacking.passedTimeLimit():
                self.tacking.stopManeuver()

    def calcBestAngleWindFromDeadzone(self, optimalCourseAngle: float) -> float:
        angleLeftToDeadzone = (self._boat.sensors.wind.toNorth - 45) % 360
        angleRightToDeadzone = (self._boat.sensors.wind.toNorth + 45) % 360

        deltaAngles = self._angleHelper.getDeltaLeftAndRightToAngle(optimalCourseAngle, angleLeftToDeadzone, angleRightToDeadzone)

        # If already sailing to the wind continue chosen side, this disables continuous switching of sailingToTheWind side
        if self.sailingToTheWind is not None:

            if self.sailingToTheWind == se.Side.Left:
                return angleLeftToDeadzone
            else:
                return angleRightToDeadzone

        # If not already sailing to the wind, check which angle from deadzone is best to sail at.
        else:
            if deltaAngles["left"] <= deltaAngles["right"]:
                self.sailingToTheWind = se.Side.Left
                return angleLeftToDeadzone
            else:
                self.sailingToTheWind = se.Side.Right
                return angleRightToDeadzone

    def boatAcrossBoarders(self, boarders: bo.Boarders) -> bool:
        if boarders.down < self._boat.sensors.gps.coordinate.latitude < boarders.top and boarders.left < self._boat.sensors.gps.coordinate.longitude < boarders.right:
            return False
        return True