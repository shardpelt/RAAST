from Helpers.jsonHelper import JsonHelper
from Route.coordinate import Coordinate

class Route:

    def __init__(self):
        # TODO: JSON coördinaten moeten via een verbinding aanpasbaar zijn
        self.finish = JsonHelper.setupFinish("Recources/finish.json")
        self.waypoints = JsonHelper.setupWaypoints("Recources/waypoints.json")
        self.boarders = JsonHelper.setupBoarders("Recources/boarders.json")
        self.waypointMargin = 0.0003 # 11 meter per 0.0001

    @property
    def currentWaypoint(self) -> Coordinate:
        return self.waypoints[0]

    def checkWaypointReached(self, currCoordinate: Coordinate) -> bool:
        """
            Wheter the boat's current coordinate is within the next waypoint's coordinate +/- margin
            :param currCoordinate: The current coordinate the boat is at
            :returns: Boolean (True if boat has reached current sailWayPoint, False if not)
        """
        if (self.currentWaypoint.latitude - self.waypointMargin) <= currCoordinate.latitude <= (self.currentWaypoint.latitude + self.waypointMargin) \
                and (self.currentWaypoint.longitude - self.waypointMargin) <= currCoordinate.longitude <= (self.currentWaypoint.longitude + self.waypointMargin):
            return True

        return False

    def updateToNextWaypoint(self) -> None:
        self.waypoints.pop(0)


    def findWayAroundObstacle(self, coordinate: Coordinate, distance: float, angle: float) -> None:
        """
            Function should have input on where obstacle is and navigate around is
        """

