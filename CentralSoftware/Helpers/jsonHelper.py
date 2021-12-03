import sys
sys.path.append("..")

import json
import Route.boarders as bo
import Route.finish as fi
import Route.coordinate as co

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

            return fi.Finish(co.Coordinate(topCoor["latitude"], topCoor["longitude"]), co.Coordinate(bottomCoor["latitude"], bottomCoor["longitude"]))

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
                waypoints.append(co.Coordinate(waypoint["latitude"], waypoint["longitude"]))

        return waypoints

    @staticmethod
    def setupBoarders(file):
        with open(file) as boardersJson:
            boarders = json.load(boardersJson)

        return bo.Boarders(boarders["top"], boarders["down"], boarders["left"], boarders["right"])