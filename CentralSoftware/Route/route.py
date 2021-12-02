import math
from Helpers.angleHelper import AngleHelper
from Route.coordinate import Coordinate
from Helpers.jsonHelper import JsonHelper

class Route:
    def __init__(self, boat):
        self.shouldUpdate = True
        self.boat = boat
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
        self.waypoints.insert(0, waypoint)

    def calculateCoordinateAtDistance(self, currCoordinate, angle, distance):
        """
            :arg currCoordinate: The starting coordinates
            :arg angle: The angle at which the new coordinate is calculated
            :arg distance: The distance in Kilometers from the currCoordinate at which the new Coordinate is calculated
        """
        currLat = AngleHelper.toRadians(currCoordinate.latitude)
        currLong = AngleHelper.toRadians(currCoordinate.longitude)

        waypointLat = math.asin(math.sin(currLat) * math.cos(distance / self.radiusOfTheEarth) +
                                math.cos(currLat) * math.sin(distance / self.radiusOfTheEarth) * math.cos(angle))

        waypointLong = currLong + math.atan2(math.sin(angle) * math.sin(distance / self.radiusOfTheEarth) * math.cos(currLat),
                                             math.cos(distance / self.radiusOfTheEarth) - math.sin(currLat) * math.sin(waypointLat))

        return Coordinate(AngleHelper.toDegrees(waypointLat), AngleHelper.toDegrees(waypointLong))

    def hasNextWaypoint(self) -> bool:
        return self.currentWaypoint is not None

    def checkWaypointReached(self) -> bool:
        """
            Whether the boat's current coordinate is within the next waypoint's coordinate +/- margin
            :returns: True if boat has reached the current waypoint zone, False if not
        """
        if self.boat.data.currentCoordinate is not None:
            if (self.currentWaypoint.latitude - self.waypointMargin) <= self.boat.data.currentCoordinate.latitude <= (self.currentWaypoint.latitude + self.waypointMargin) \
                    and (self.currentWaypoint.longitude - self.waypointMargin) <= self.boat.data.currentCoordinate.longitude <= (self.currentWaypoint.longitude + self.waypointMargin):
                return True

        return False

    def updateToNextWaypoint(self) -> None:
        self.waypoints.pop(0)

    def circumnavigateSonar(self) -> None:
        """
            # TODO: Testing
            Creates an new waypoint which course to sail lays out of object's field
        """
        if 0 <= self.boat.data.wind.angle <= 180: # Boat traverses left from object so can't choose an course to the right side.
            traversedCourseAngle = (self.boat.data.compass.angle - 90) % 360
            self.boat.course.cantChooseSide = "right"
        else:
            traversedCourseAngle = (self.boat.data.compass.angle + 90) % 360
            self.boat.course.cantChooseSide = "left"

        newCoordinate = self.calculateCoordinateAtDistance(self.boat.data.currentCoordinate, AngleHelper.toRadians(traversedCourseAngle), self.obstacleMarginKm)

        self.addWaypoint(newCoordinate)

    def circumnavigateAis(self) -> None:
        # TODO

        ah = AngleHelper()

        for ship in self.boat.data.ais.nearbyShips:

            distance = math.sqrt((ship["latitude"] - self.boat.data.currentCoordinate.latitude)**2 + (ship["longitude"] - self.boat.data.currentCoordinate.longitude)**2)
            angle = ah.calcAngleBetweenCoordinates(self.boat.data.currentCoordinate, Coordinate(ship["latitude"], ship["longitude"]))




# r = Route(SensorData())
# r.circumnavigateSonar()