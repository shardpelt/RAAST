import math
from Helpers.angleHelper import AngleHelper
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
        self.radiusOfTheEarth = 6378.1
        self.waypointMargin = 0.0003 # 11 meter
        self.obstacleMarginKm = 2

    @property
    def currentWaypoint(self) -> Coordinate:
        return self.waypoints[0]

    def addWaypoint(self, waypoint: Coordinate):
        # TODO: Func to add a waypoint as next one
        pass

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

    def circumnavigateSonar(self) -> None:
        """
            # TODO: Testing
            Creates an new waypoint which course to sail at lays out of object's field
        """
        bearing = AngleHelper.toRadians(self.data.compass.angle)

        currLat = AngleHelper.toRadians(self.data.currentCoordinate.latitude)
        currLong = AngleHelper.toRadians(self.data.currentCoordinate.longitude)

        waypointLat = math.asin(math.sin(currLat) * math.cos(self.obstacleMarginKm / self.radiusOfTheEarth) +
                         math.cos(currLat) * math.sin(self.obstacleMarginKm / self.radiusOfTheEarth) * math.cos(bearing))

        waypointLong = currLong + math.atan2(math.sin(bearing) * math.sin(self.obstacleMarginKm / self.radiusOfTheEarth) * math.cos(currLat),
                                 math.cos(self.obstacleMarginKm / self.radiusOfTheEarth) - math.sin(currLat) * math.sin(waypointLat))

        self.addWaypoint(Coordinate(AngleHelper.toDegrees(waypointLat), AngleHelper.toDegrees(waypointLong)))


    def circumnavigateAis(self) -> None:
        pass

# r = Route(SensorData())
# r.circumnavigateSonar()