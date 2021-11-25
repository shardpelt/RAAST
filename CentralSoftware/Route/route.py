from copy import copy
from SensorData.sensor_data import SensorData
from Route.coordinate import Coordinate
from Helpers.jsonHelper import JsonHelper

class Route:
    def __init__(self, sensorData: SensorData):
        self.shouldUpdate = True
        self.data = sensorData
        self.finish = JsonHelper.setupFinish("Recources/finish.json")
        self.waypoints = JsonHelper.setupWaypoints("Recources/waypoints.json")
        self.boarders = JsonHelper.setupBoarders("Recources/boarders.json")
        self.waypointMargin = 0.0003 # 11 meter per 0.0001

    def addWaypoint(self, waypoint: Coordinate):
        # TODO: Func to add a waypoint as next one
        pass

    def getDict(self):
        d = vars(copy(self))
        del d["data"]

        for k, v in d.items():
            if k == "waypoints":
                d[k] = [vars(wp) for wp in v]
            elif k == "finish":
                x = vars(copy(v))
                for k2, v2 in x.items():
                    x[k2] = vars(v2)
                d[k] = x
            elif k == "boarders":
                d[k] = vars(v)

        return d

    @property
    def currentWaypoint(self) -> Coordinate:
        return self.waypoints[0]

    def hasNextWaypoint(self) -> bool:
        return self.currentWaypoint is not None

    def checkWaypointReached(self) -> bool:
        """
            Whether the boat's current coordinate is within the next waypoint's coordinate +/- margin
            :returns: True if boat has reached the current waypoint zone, False if not
        """
        if self.data.currentCoordinate is not None:
            if (self.currentWaypoint.latitude - self.waypointMargin) <= self.data.currentCoordinate.latitude <= (self.currentWaypoint.latitude + self.waypointMargin) \
                    and (self.currentWaypoint.longitude - self.waypointMargin) <= self.data.currentCoordinate.longitude <= (self.currentWaypoint.longitude + self.waypointMargin):
                return True

        return False

    def updateToNextWaypoint(self) -> None:
        self.waypoints.pop(0)

    def findWayAroundObstacles(self) -> None:
        scanAnalysis = self.data.sonar.getScanAnalysis()

    def checkThreatDetection(self) -> bool:
        return self.data.sonar.hasData()