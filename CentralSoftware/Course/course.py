import sys
sys.path.append("..")

import Route.boarders as bo
import Route.coordinate as co
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
        self.tacking = ta.Tacking(self.sailingToTheWind)
        self.boarderMarge = 0

        self.angleLeftToDead = None
        self.angleRightToDead = None
        self.deltaL = None
        self.deltaR = None

    def isOffTrack(self) -> bool:
        return not self._angleHelper.angleIsBetweenAngles(self._boat.sensors.compass.angle, self.wantedCourseAngle - self.wantedCourseAngleMarge, self.wantedCourseAngle + self.wantedCourseAngleMarge)

    def forgetDeadzoneFlags(self) -> None:
        self.sailingToTheWind = None
        self.cantChooseSide = None
        self.tacking.stopManeuver()

    def updateWantedAngle(self, waypoint: wp.Waypoint, boarders: bo.Boarders) -> None:
        """
            :arg waypoint: The current waypoint
            :arg boarders: The absolute boarders in which the _boat should stay during the trip
            :returns: The best course angle to set, according to the wind and the current waypoint
        """
        # TODO: Functionaliteit inbouwen voor wanneer tacking niet slaagt

        self.checkTackingManeuver()

        self.optimalCourseAngle = self._angleHelper.calcAngleBetweenCoordinates(self._boat.sensors.gps.coordinate, waypoint.coordinate)

        # TODO: Coordinaten upgraden met noord oost zuid west, voor meer functionaliteit
        # if self.boatAtBoarders(self._boat.sensors.gps.coordinate, boarders) and not self.tacking.inManeuver:
        #     self.forgetDeadzoneFlags()
        #     self.tacking.startManeuver()

        # If wind blows from deadzone choose shortest side to sail at
        if self._angleHelper.windFromDeadzone(self.optimalCourseAngle, self._boat.sensors.wind):
            self.wantedCourseAngle = self.calcBestAngleWindFromDeadzone(self.optimalCourseAngle)
        else:
            # If boat was sailing to the wind, then a tacking maneuver is tried to achieve the fastest path
            if self.sailingToTheWind:
                self.forgetDeadzoneFlags()
                self.tacking.startManeuver()

            # If the boat was not previously sailing to the wind, a tacking maneuver is not tried
            self.wantedCourseAngle = self.optimalCourseAngle

    def checkTackingManeuver(self) -> None:
        if self.tacking.inManeuver:
            if self.tacking.isCompleted(self._boat.sensors.compass.angle, self.wantedCourseAngle):
                self.tacking.stopManeuver()
            elif self.tacking.passedTimeLimit():
                self.tacking.stopManeuver()

    def calcBestAngleWindFromDeadzone(self, optimalCourseAngle: float) -> float:
        self.angleLeftToDead = (self._boat.sensors.wind.toNorth - 45) % 360
        self.angleRightToDead = (self._boat.sensors.wind.toNorth + 45) % 360

        deltaAngles = self._angleHelper.getDeltaLeftAndRightToAngle(optimalCourseAngle, self.angleLeftToDead, self.angleRightToDead)

        self.deltaL = deltaAngles["left"]
        self.deltaR = deltaAngles["right"]

        # If already sailing to the wind continue chosen side, this disables continuous switching of sailingToTheWind side
        if self.sailingToTheWind is not None:

            if self.sailingToTheWind == se.Side.Left:
                return self.angleLeftToDead
            else:
                return self.angleRightToDead

            # if deltaAngles["left"] <= self.tackingAngleMarge:
            #     self.sailingToTheWind = "left"
            #     return angleLeftToDeadzone
            # elif deltaAngles["right"] <= self.tackingAngleMarge:
            #     self.sailingToTheWind = "right"
            #     return angleRightToDeadzone
            # else:
            #     if self.sailingToTheWind == "left":
            #         return angleLeftToDeadzone
            #     return angleRightToDeadzone

        # If not already sailing to the wind, check which angle from deadzone is best to sail at.
        else:
            if deltaAngles["left"] <= deltaAngles["right"]:
                self.sailingToTheWind = se.Side.Left
                return self.angleLeftToDead
            else:
                self.sailingToTheWind = se.Side.Right
                return self.angleRightToDead


    def boatAtBoarders(self, currCoordinate: co.Coordinate, boarders: bo.Boarders) -> bool:
        if currCoordinate.latitude <= (boarders.down + self.boarderMarge):
            return True
        elif currCoordinate.latitude >= (boarders.top - self.boarderMarge):
            return True
        elif currCoordinate.longitude <= (boarders.left + self.boarderMarge):
            return True
        elif currCoordinate.longitude >= (boarders.right - self.boarderMarge):
            return True

        return False