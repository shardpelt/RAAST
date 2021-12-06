import sys
sys.path.append("..")

import math
import Helpers.angleHelper as ah
import Route.coordinate as co
import Helpers.jsonHelper as jh

class Route:
    def __init__(self, boat):
        self.shouldUpdate = True
        self.boat = boat
        self.finish = jh.JsonHelper.setupFinish("Recources/finish.json")
        self.waypoints = jh.JsonHelper.setupWaypoints("Recources/waypoints.json")
        self.boarders = jh.JsonHelper.setupBoarders("Recources/boarders.json")
        self.radiusOfTheEarth = 6378.1
        self.waypointMargin = 0.0003 # 11 meter
        self.obstacleMarginKm = 2

    @property
    def currentWaypoint(self) -> co.Coordinate:
        return self.waypoints[0]

    def addWaypoint(self, waypoint: co.Coordinate):
        self.waypoints.insert(0, waypoint)

    def calculateCoordinateAtDistance(self, currCoordinate, angle, distance):
        """
            :arg currCoordinate: The starting coordinates
            :arg angle: The angle at which the new coordinate is calculated
            :arg distance: The distance in Kilometers from the currCoordinate at which the new Coordinate is calculated
        """
        currLat = ah.AngleHelper.toRadians(currCoordinate.latitude)
        currLong = ah.AngleHelper.toRadians(currCoordinate.longitude)

        waypointLat = math.asin(math.sin(currLat) * math.cos(distance / self.radiusOfTheEarth) +
                                math.cos(currLat) * math.sin(distance / self.radiusOfTheEarth) * math.cos(angle))

        waypointLong = currLong + math.atan2(math.sin(angle) * math.sin(distance / self.radiusOfTheEarth) * math.cos(currLat),
                                             math.cos(distance / self.radiusOfTheEarth) - math.sin(currLat) * math.sin(waypointLat))

        return co.Coordinate(ah.AngleHelper.toDegrees(waypointLat), ah.AngleHelper.toDegrees(waypointLong))

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

        newWaypoint = self.calculateCoordinateAtDistance(self.boat.data.currentCoordinate, ah.AngleHelper.toRadians(traversedCourseAngle), self.obstacleMarginKm)

        self.addWaypoint(newWaypoint)

    def circumnavigateAis(self) -> None:
        # Vaart een schip van je af -> doe niks
        # Vaart een schip door onze koerslijn heen? -> Vaar naar coordinaten van dat schip +/- marge
        # angle = helper.calcAngleBetweenCoordinates(self.boat.data.currentCoordinate, co.Coordinate(ship["latitude"], ship["longitude"]))

        distanceOrderedAis = self.boat.data.ais.getAisOrderedByDistance(self.boat.data.currentCoordinate)

        traversedWaypoints = []
        for ship in distanceOrderedAis:
            if ship[2] != 511:
                a = self.boat.data.currentCoordinate if len(traversedWaypoints) == 0 else traversedWaypoints[0]
                b = self.currentWaypoint
                c = co.Coordinate(ship[0], ship[1])
                d = self.calculateCoordinateAtDistance(c, ah.AngleHelper.toRadians(ship[2]), self.boat.data.ais.reach)
                if self.intersect(a, b, c, d):
                    # TODO: Maak een nieuw coordinaat aan op ship coordinates +/- marge
                    pass
            else:
                # TODO: Check of het schip in onze koers ligt, anders boeie!
                pass

    # Return true if line segments AB and CD intersect
    def intersect(self, A, B, C, D) -> bool:
        """
        :param A: Current coordinate of boat
        :param B: Headed coordinate of boat
        :param C: Current coordinate of ais ship
        :param D: Headed coordinate of ais ship
        :return: bool -> Whether the two route lines of the boat and the ais ship collide
        """
        return self.ccw(A, C, D) != self.ccw(B, C, D) and self.ccw(A, B, C) != self.ccw(A, B, D)

    def ccw(self, A, B, C) -> bool:
        return (C.latitude - A.latitude) * (B.longitude - A.longitude) > (B.latitude - A.latitude) * (C.longitude - A.longitude)


