import json
from Sensors.coordinate import Coordinate

class SailingCourse:

    def __init__(self):
        self.finish = None
        self.waypoints = []  # TODO: JSON coördinaten moeten via een verbinding aanpasbaar zijn
        self.setupMainWaypoints()
        self.mainWaypointsJson = "Recources/waypoints.json"
        self.sailWayPoints = []
        self.waypointMargin = 0.0003 # 11 meter per 0.0001

    @property
    def currSailWayPoint(self) -> Coordinate:
        return self.sailWayPoints[0]

    @property
    def currMainWayPoint(self) -> Coordinate:
        return self.waypoints[0]


    def setupMainWaypoints(self):
        """
            This method is only called once at startup
            Sets up the main waypoints for the route to be sailed
        """
        with open(self.mainWaypointsJson) as mainWaypointsJson:
            mainWaypointsObject = json.load(mainWaypointsJson)
            for waypoint in mainWaypointsObject:
                self.waypoints.append(Coordinate(waypoint["latitude"], waypoint["longitude"]))

        # TODO: Calculate extra mainWayPoints (on what basis? length etc)


    def calcSailingWaypoints(self):
        """
            Calculates the best sailing route to the next mainWayPoint
        """


    def checkWaypointReached(self, currCoordinate: Coordinate) -> bool:
        """
            Wheter the boat's current coordinate is within the next waypoint's coordinate +/- margin
            :param currCoordinate: The current coordinate the boat is at
            :returns: Boolean (True if boat has reached current sailWayPoint, False if not)
        """
        if (self.currSailWayPoint.latitude - self.waypointMargin) <= currCoordinate.latitude <= (self.currSailWayPoint.latitude + self.waypointMargin) \
                and (self.currSailWayPoint.longitude - self.waypointMargin) <= currCoordinate.longitude <= (self.currSailWayPoint.longitude + self.waypointMargin):
            return True

        return False


    def update(self):
        pass

