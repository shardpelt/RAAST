import sys
import math
sys.path.append("..")

import Helpers.angleHelper as ah
import Route.coordinate as co
import Route.waypoint as wp
import Helpers.jsonHelper as jh

class Route:
    def __init__(self, boat):
        self.shouldUpdate = True
        self._boat = boat
        self._angleHelper = ah.AngleHelper()
        self.waypoints, self.finish, self.boarders = jh.JsonHelper.setupRoute("Recources/route.json")
        self._radiusOfTheEarth = 6378.1
        self.waypointMargin = 0.5 # 55 meter TODO: adjust to 55 meters
        self.obstacleMarginKm = 2

    @property
    def currentWaypoint(self) -> wp.Waypoint:
        if not self.waypoints:
            return self.getBestWaypointOnFinishLine()
        else:
            return self.waypoints[0]

    def addWaypoint(self, waypoint: wp.Waypoint):
        self.waypoints.insert(0, waypoint)

    def getBestWaypointOnFinishLine(self) -> wp.Waypoint:
        """
            TODO
            Calculates the best waypoint to sail at between te finish line according to the _boat's angle and wind angle
        """
        angleToCoorOne = self._angleHelper.calcAngleBetweenCoordinates(self._boat.data.currentCoordinate, self.finish.coordinateOne)
        angleToCoorTwo = self._angleHelper.calcAngleBetweenCoordinates(self._boat.data.currentCoordinate, self.finish.coordinateTwo)

        return wp.Waypoint()


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

    def hasNextWaypoint(self) -> bool:
        return self.currentWaypoint is not None

    def checkWaypointReached(self) -> bool:
        """
            Whether the _boat's current coordinate is within the next waypoint's coordinate +/- margin
            :returns: True if _boat has reached the current waypoint zone, False if not
        """
        if self._boat.data.currentCoordinate is not None:
            if (self.currentWaypoint.coordinate.latitude - self.waypointMargin) <= self._boat.data.currentCoordinate.latitude <= (self.currentWaypoint.coordinate.latitude + self.waypointMargin) \
                    and (self.currentWaypoint.coordinate.longitude - self.waypointMargin) <= self._boat.data.currentCoordinate.longitude <= (self.currentWaypoint.coordinate.longitude + self.waypointMargin):
                return True

        return False

    def updateToNextWaypoint(self) -> None:
        self.waypoints.pop(0)

    def circumnavigateSonar(self) -> None:
        """
            TODO: Testing
            Creates an new waypoint which course to sail lays out of object's field
        """
        if 0 <= self._boat.data.wind.angle <= 180: # _Boat traverses left from object so can't choose an course to the right side.
            traversedCourseAngle = (self._boat.data.compass.angle - 90) % 360
            self._boat.course.cantChooseSide = "right"
        else:
            traversedCourseAngle = (self._boat.data.compass.angle + 90) % 360
            self._boat.course.cantChooseSide = "left"

        coordinate = self.calculateCoordinateAtDistance(self._boat.data.currentCoordinate, self._angleHelper.toRadians(traversedCourseAngle), self.obstacleMarginKm)
        newWaypoint = wp.Waypoint(coordinate, wp.WpType.SonarAvoidance)
        self.addWaypoint(newWaypoint)

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
                if self.intersect(currCr, currWp.coordinate, shipCoordinate, ds):
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
            self.addWaypoint(wp.Waypoint(coordinate, wp.WpType.AisAvoidance))


    def intersect(self, A, B, C, D) -> bool:
        """
        :param A: Current coordinate of _boat
        :param B: Headed coordinate of _boat
        :param C: Current coordinate of ais ship
        :param D: Headed coordinate of ais ship
        :return: bool -> Whether the two route lines of the _boat and the ais ship collide
        """
        return self.ccw(A, C, D) != self.ccw(B, C, D) and self.ccw(A, B, C) != self.ccw(A, B, D)

    def ccw(self, A, B, C) -> bool:
        return (C.latitude - A.latitude) * (B.longitude - A.longitude) > (B.latitude - A.latitude) * (C.longitude - A.longitude)