import sys
import math
sys.path.append("..")

import Helpers.angle_helper as ah
import Route.coordinate as co
import Route.waypoint as wp
import Enums.waypoint_type_enum as wt
import Helpers.json_helper as jh
import Helpers.collision_helper as ch

class Route:
    def __init__(self, boat):
        self._boat = boat
        self._angleHelper = ah.AngleHelper()
        self._collisionHelper = ch.CollisionHelper()
        self.isUpdatable = True
        self.waypointMargin = 0.5 # Te bepalen afstand in real-world
        self.obstacleMarginKm = 2
        self.waypoints, self.boarders = jh.JsonHelper.setupRoute("Recources/route.json")
        self._radiusOfTheEarth = 6378.1

    @property
    def currentWaypoint(self) -> wp.Waypoint:
        return self.waypoints[0]

    def hasNextWaypoint(self) -> bool:
        return len(self.waypoints) != 0

    def addWaypoint(self, waypoint: wp.Waypoint) -> None:
        self.waypoints.insert(0, waypoint)

    def updateToNextWaypoint(self) -> None:
        if self.waypoints:
            self.waypoints.pop(0)

    def calculateCoordinateAtDistance(self, currCoordinate, angle, distance) -> co.Coordinate:
        """
            :arg currCoordinate: The starting coordinates
            :arg angle: The angle at which the new coordinate is calculated
            :arg distance: The distance in Kilometers from the currCoordinate at which the new Coordinate is calculated
        """
        currLat = self._angleHelper.toRadians(currCoordinate.latitude)
        currLong = self._angleHelper.toRadians(currCoordinate.longitude)

        waypointLat = math.asin(math.sin(currLat) * math.cos(distance / self._radiusOfTheEarth) +
                                math.cos(currLat) * math.sin(distance / self._radiusOfTheEarth) * math.cos(angle))

        waypointLong = currLong + math.atan2(math.sin(angle) * math.sin(distance / self._radiusOfTheEarth) * math.cos(currLat),
                                             math.cos(distance / self._radiusOfTheEarth) - math.sin(currLat) * math.sin(waypointLat))

        return co.Coordinate(self._angleHelper.toDegrees(waypointLat), self._angleHelper.toDegrees(waypointLong))

    def checkWaypointReached(self) -> bool:
        """
            Whether the _boat's current coordinate is within the next waypoint's coordinate +/- margin
            :returns: True if _boat has reached the current waypoint zone, False if not
        """
        if self._boat.sensors.gps.hasData() and self.hasNextWaypoint():
            if (self.currentWaypoint.coordinate.latitude - self.waypointMargin) <= self._boat.sensors.gps.coordinate.latitude <= (self.currentWaypoint.coordinate.latitude + self.waypointMargin) \
                    and (self.currentWaypoint.coordinate.longitude - self.waypointMargin) <= self._boat.sensors.gps.coordinate.longitude <= (self.currentWaypoint.coordinate.longitude + self.waypointMargin):
                return True

        return False

    def circumnavigateSonar(self) -> None:
        """
            TODO: Testing
            Creates an new waypoint which course to sail lays out of object's field
        """
        if 0 <= self._boat.data.wind.relative <= 180: # Boat traverses left from object so can't choose an course to the right side.
            traversedCourseAngle = (self._boat.data.compass.angle - 90) % 360
            self._boat.course.cantChooseSide = "right"
        else:
            traversedCourseAngle = (self._boat.data.compass.angle + 90) % 360
            self._boat.course.cantChooseSide = "left"

        coordinate = self.calculateCoordinateAtDistance(self._boat.data.currentCoordinate, self._angleHelper.toRadians(traversedCourseAngle), self.obstacleMarginKm)
        newWaypoint = wp.Waypoint(coordinate, wt.WpType.SonarAvoidance)
        self.addWaypoint(newWaypoint)

        self._boat.sensors.ais.nearbyShips = None

    def circumnavigateAis(self) -> None:
        """
            TODO: Testing
            This function is called when there is any new information from the AIS module in the _boat
            It goes through an ordered (by distance) list of the scanned ships and checks if an traverse is needed
            If the ship has course code 511 it does not move, in that case we check if that ship is in our way
            If the ship has an active heading(course) we check if it's path has any intersection with ours
            If one of these cases is applicable, we make a new waypoint at the ships coordinate according to a marge
        """
        distanceOrderedAis = self._boat.data.ais.getAisOrderedByDistance(self._boat.data.currentCoordinate)

        traversedCoordinates = []
        for ship in distanceOrderedAis:
            shipCoordinate = co.Coordinate(ship[0], ship[1])
            currCr = self._boat.data.currentCoordinate if len(traversedCoordinates) == 0 else traversedCoordinates[0]
            if ship[2] != 511:
                currWp = self.currentWaypoint
                ds = self.calculateCoordinateAtDistance(shipCoordinate, self._angleHelper.toRadians(ship[2]), self._boat.data.ais.reach)
                if self._collisionHelper.lineLineIntersection(currCr, currWp.coordinate, shipCoordinate, ds):
                    reversedShipsCourse = (ship[2] - 180) % 360
                    traversedCoordinate = self.calculateCoordinateAtDistance(currCr, reversedShipsCourse, self.obstacleMarginKm)
                    traversedCoordinates.append(traversedCoordinate)
            else:
                shipToWaypointAngle = self._angleHelper.calcAngleBetweenCoordinates(shipCoordinate, self.currentWaypoint.coordinate)
                _boatToWaypointAngle = self._angleHelper.calcAngleBetweenCoordinates(currCr, self.currentWaypoint.coordinate)
                if self._angleHelper.angleIsBetweenAngles(_boatToWaypointAngle, shipToWaypointAngle - 5, shipToWaypointAngle + 5):
                    traversedCoordinate = self.calculateCoordinateAtDistance(shipCoordinate, 90, self.obstacleMarginKm)
                    traversedCoordinates.append(traversedCoordinate)

        for coordinate in traversedCoordinates:
            self.addWaypoint(wp.Waypoint(coordinate, wt.WpType.AisAvoidance))