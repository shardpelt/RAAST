import json

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
            top = finishObject["topCoordinate"]
            bottom = finishObject["bottomCoordinate"]

            return Finish(Coordinate(top["latitude"], top[["longitude"]]), Coordinate(bottom["latitude"], bottom[["longitude"]]))

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
                waypoints.append(Coordinate(waypoint["latitude"], waypoint["longitude"]))

        return waypoints

    @staticmethod
    def setupBoarders(file):
        with open(file) as boardersJson:
            boarders = json.load(boardersJson)

        return Boarders(boarders["top"], boarders["down"], boarders["left"], boarders["right"])