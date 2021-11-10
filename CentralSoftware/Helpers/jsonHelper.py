import json
from Helpers.angleHelper import AngleHelper as ah
from Route.boarders import Boarders
from Route.finish import Finish
from Route.coordinate import Coordinate

class JsonHelper:

    @staticmethod
    def setupFinish(file):
        """
            This method is only called once at startup
            Sets up the finish coordinates for the race
        """
        with open(file) as finishJson:
            finishObject = json.load(finishJson)
            topCoor = finishObject["topCoordinate"]
            bottomCoor = finishObject["bottomCoordinate"]

            return Finish(Coordinate(ah.toRadians(topCoor["latitude"]), ah.toRadians(topCoor["longitude"])), Coordinate(ah.toRadians(bottomCoor["latitude"]), ah.toRadians(bottomCoor["longitude"])))

    @staticmethod
    def setupWaypoints(file):
        """
            This method is only called once at startup
            Sets up the waypoints for the route to be sailed
        """
        waypoints = []
        with open(file) as waypointsJson:
            waypointsObject = json.load(waypointsJson)

            for waypoint in waypointsObject:
                waypoints.append(Coordinate(ah.toRadians(waypoint["latitude"]), ah.toRadians(waypoint["longitude"])))

        return waypoints

    @staticmethod
    def setupBoarders(file):
        with open(file) as boardersJson:
            boarders = json.load(boardersJson)

        return Boarders(ah.toRadians(boarders["top"]), ah.toRadians(boarders["down"]), ah.toRadians(boarders["left"]), ah.toRadians(boarders["right"]))