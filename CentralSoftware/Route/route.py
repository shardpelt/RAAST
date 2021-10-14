from CentralData.central_data import CentralData
from Route.coordinate import Coordinate

class Route:
    def __init__(self, centralData: CentralData):
        # TODO: JSON coördinaten moeten via een verbinding aanpasbaar zijn
        self.data = centralData
        self.finish = None #JsonHelper.setupFinish("../Recources/finish.json")
        self.waypoints = None #JsonHelper.setupWaypoints("Recources/waypoints.json")
        self.boarders = None #JsonHelper.setupBoarders("Recources/boarders.json")
        self.waypointMargin = 0.0003 # 11 meter per 0.0001

    @property
    def currentWaypoint(self) -> Coordinate:
        return self.waypoints[0]

    def checkWaypointReached(self) -> bool:
        """
            Whether the boat's current coordinate is within the next waypoint's coordinate +/- margin
            :returns: Boolean (True if boat has reached current sailWayPoint, False if not)
        """
        if (self.currentWaypoint.latitude - self.waypointMargin) <= self.data.currentCoordinate.latitude <= (self.currentWaypoint.latitude + self.waypointMargin) \
                and (self.currentWaypoint.longitude - self.waypointMargin) <= self.data.currentCoordinate.longitude <= (self.currentWaypoint.longitude + self.waypointMargin):
            return True

        return False

    def updateToNextWaypoint(self) -> None:
        self.waypoints.pop(0)

    def findWayAroundObstacles(self) -> None:
        """
            Function should have input on where obstacle is and navigate around is
        """
        objects = self.data.sonar.getSeenObjects()

    def checkThreatDetection(self):
        # TODO: Checks if sonar, AIS or storm is
        pass
