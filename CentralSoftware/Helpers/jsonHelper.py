import sys
sys.path.append("..")

import json
import Route.boarders as bo
import Route.finish as fi
import Route.coordinate as co
import Route.waypoint as wp

class JsonHelper:

    @staticmethod
    def setupRoute(file):
        waypoints = []
        with open(file) as routeFile:
            routeFileObj = json.load(routeFile)

            # Loading waypoints
            for waypoint in routeFileObj["waypoints"]:
                coordinate = co.Coordinate(waypoint["latitude"], waypoint["longitude"])
                waypoints.append(wp.Waypoint(coordinate, wp.WpType.Predefined))

            # Loading finish
            coordinateOne = routeFileObj["finish"]["coordinateOne"]
            coordinateTwo = routeFileObj["finish"]["coordinateOne"]
            finish = fi.Finish(co.Coordinate(coordinateOne["latitude"], coordinateOne["longitude"]), co.Coordinate(coordinateTwo["latitude"], coordinateTwo["longitude"]))

            # Loading boarders
            boarders = bo.Boarders(routeFileObj["boarders"]["top"], routeFileObj["boarders"]["down"], routeFileObj["boarders"]["left"], routeFileObj["boarders"]["right"])

        return waypoints, finish, boarders