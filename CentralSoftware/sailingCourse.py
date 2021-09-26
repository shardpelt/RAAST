from Helpers.jsonHelper import JsonHelper
from coordinate import Coordinate

class SailingCourse:

    def __init__(self):
        # TODO: JSON coördinaten moeten via een verbinding aanpasbaar zijn
        self.finish = JsonHelper.setupFinish("Recources/finish.json")
        self.waypoints = JsonHelper.setupWaypoints("Recources/waypoints.json")
        self.waypointMargin = 0.0003 # 11 meter per 0.0001

    @property
    def currWaypoint(self) -> Coordinate:
        return self.waypoints[0]


    def calculateBestCourse(self):
        """
            Calculates the best sailing course to the next waypoint
        """


    def checkWaypointReached(self, currCoordinate: Coordinate) -> bool:
        """
            Wheter the boat's current coordinate is within the next waypoint's coordinate +/- margin
            :param currCoordinate: The current coordinate the boat is at
            :returns: Boolean (True if boat has reached current sailWayPoint, False if not)
        """
        if (self.currWaypoint.latitude - self.waypointMargin) <= currCoordinate.latitude <= (self.currWaypoint.latitude + self.waypointMargin) \
                and (self.currWaypoint.longitude - self.waypointMargin) <= currCoordinate.longitude <= (self.currWaypoint.longitude + self.waypointMargin):
            return True

        return False



    def circumnavigateObstacle(self):
        """
            Function should have input on where obstacle is and navigate around is
        """
        pass
