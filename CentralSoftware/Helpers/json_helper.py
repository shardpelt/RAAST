import sys
sys.path.append("..")

import json as js
import Route.boarders as bo
import Route.coordinate as co
import Route.waypoint as wp
import Enums.waypoint_type_enum as wt
import Helpers.obj_to_dict_helper as od

class JsonHelper:

    @staticmethod
    def setupRoute(file):
        waypoints = []
        with open(file) as routeFile:
            routeFileObj = js.load(routeFile)

            # Loading waypoints
            for waypoint in routeFileObj["waypoints"]:
                coordinate = co.Coordinate(waypoint["latitude"], waypoint["longitude"])
                waypoints.append(wp.Waypoint(coordinate, wt.WpType.Predefined))

            # Loading finish
            finishCoordinate = routeFileObj["finish"]
            waypoints.append(wp.Waypoint(co.Coordinate(finishCoordinate["latitude"], finishCoordinate["longitude"]), wt.WpType.Finish))

            # Loading boarders
            boarders = bo.Boarders(routeFileObj["boarders"]["top"], routeFileObj["boarders"]["down"], routeFileObj["boarders"]["left"], routeFileObj["boarders"]["right"])

        return waypoints, boarders

    @staticmethod
    def makePackage(header, payload):
        package = js.dumps({header: od.DictSerializer.getDict(payload)})
        return package