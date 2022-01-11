'''
====== Legal notices

Copyright (C) 2013 - 2021 GEATEC engineering

This program is free software.
You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicense.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY, without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the QQuickLicense for details.

The QQuickLicense can be accessed at: http://www.qquick.org/license.html

__________________________________________________________________________


 THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!

__________________________________________________________________________

It is meant for training purposes only.

Removing this header ends your license.
'''

import socket as sc
import time as tm

import simpylc as sp
import socket_pilot.socket_wrapper as sw

class Server:
    def __init__ (self):
        with sc.socket (*sw.socketType) as serverSocket:
            serverSocket.bind (sw.address)
            serverSocket.listen (sw.maxNrOfConnectionRequests)

            while True:
                self.clientSocket = serverSocket.accept ()[0]
                self.socketWrapper = sw.SocketWrapper (self.clientSocket)

                with self.clientSocket:
                    while True:
                        relativeWindAngle = sp.evaluate(sp.world.wind.relative_direction)
                        compassAngle = sp.evaluate(sp.world.sailboat.compassAngle)
                        latitude = sp.evaluate(sp.world.sailboat.position_x)
                        longitude = sp.evaluate(sp.world.sailboat.position_y) * -1
                        sensors = self.toDataPackage(relativeWindAngle, compassAngle, latitude, longitude)

                        self.socketWrapper.send (sensors)

                        tm.sleep (0.02)

                        message = self.socketWrapper.recv ()
                        self.updateData(message)

    def toDataPackage(self, relativeWindAngle, compassAngle, latitude, longitude):
        sensorData = [
                {"type": "sensor", "id": 3, "body": {"value": compassAngle}},
                {"type": "sensor", "id": 1, "body": {"value": relativeWindAngle}},
                {"type": "sensor", "id": 2, "body": {"value": (latitude, longitude)}},
                ]

        return sensorData

    def updateData(self, message):
        boatDict = message["update"]

        self.updateRudderSail(boatDict)
        self.updateWaypoints(boatDict["route"]["waypoints"])

        sp.world.sailboat.latitude.set(round(boatDict["sensors"]["gps"]["coordinate"]["latitude"], 2))
        sp.world.sailboat.longitude.set(round(boatDict["sensors"]["gps"]["coordinate"]["longitude"], 2))
        sp.world.sailboat.wantedAngle.set(round(boatDict["course"]["wantedCourseAngle"], 5))
        sp.world.sailboat.optimalAngle.set(round(boatDict["course"]["optimalCourseAngle"], 5))
        sp.world.sailboat.toTheWind.set(self.evalSides(boatDict["course"]["sailingToTheWind"]))
        sp.world.sailboat.cantChooseSide.set(self.evalSides(boatDict["course"]["cantChooseSide"]))

    def evalSides(self, side):
        if side is None:
            return -1
        elif side == "Left":
            return 0
        else:
            return 1

    def updateRudderSail(self, boatDict):
        if boatDict["rudder"]["wantedAngle"] is not None:
            sp.world.sailboat._rudderAngle = boatDict["rudder"]["wantedAngle"]
        if boatDict["sail"]["wantedAngle"] is not None:
            sp.world.sailboat._sailAngle = boatDict["sail"]["wantedAngle"]

    def updateWaypoints(self, waypointsDict):
        # Reset waypoints list in world.sailboat
        sp.world.waypoint._waypoints = []

        # Make a list out of each waypoint coordinate and append to waypoints list in world.sailboat
        for waypDict in waypointsDict:
            xCoordinate = waypDict['coordinate']['latitude']
            yCoordinate = waypDict['coordinate']['longitude'] * -1
            waypoint = [xCoordinate, yCoordinate]
            sp.world.waypoint._waypoints.append(waypoint)




'''

{"update": {"controlMode": 3, "rudder": {"isUpdatable": true, "wantedAngle": 0, "pid": {"p": 0.5, "i": 0.02, "d": 0.0005, "yI": 0, "errorOld": 0, "prevTime": null}, "maxWantedAngle": 35}, "sail": {"isUpdatable": true, "wantedAngle": 0, "windRightToSail": [{"wind": 0, "sail": -10, "interpolate": false}, {"wind": 90, "sail": -10, "interpolate": true}, {"wind": 135, "sail": -45, "interpolate": true}, {"wind": 180, "sail": -90, "interpolate": null}], "windLeftToSail": [{"wind": 180, "sail": 90, "interpolate": true}, {"wind": 225, "sail": 45, "interpolate": true}, {"wind": 270, "sail": 10, "interpolate": false}, {"wind": 360, "sail": 10, "interpolate": null}]}, "sensors": {"gyroscope": {"xPos": null, "yPos": null, "zPos": null}, "gps": {"coordinate": {"latitude": null, "longitude": null}}, "compass": {"angle": null}, "wind": {"relative": null, "toNorth": null, "speed": null}, "sonar": {"objectDetected": false, "totalScanAngle": 30}, "ais": {"reach": 30, "nearbyShips": null}, "rudderAngle": null, "sailAngle": null}, "route": {"isUpdatable": true, "waypoints": [{"coordinate": {"latitude": 1.0, "longitude": 5.0}, "origin": "Predefined"}, {"coordinate": {"latitude": 7.0, "longitude": 5.0}, "origin": "Predefined"}, {"coordinate": {"latitude": 15.0, "longitude": 5.0}, "origin": "Finish"}], "boarders": {"top": 50.0, "down": -50.0, "left": 50.0, "right": -50.0}, "waypointMargin": 0.5, "obstacleMarginKm": 2}, "course": {"isUpdatable": true, "optimalAngle": null, "wantedAngle": null, "wantedAngleMarge": 5, "wantedSailMarge": 5, "toTheWind": null, "cantChooseSide": null, "tackingAngleMarge": 0, "boarderMarge": 0.005, "angleLeftToDead": null, "angleRightToDead": null, "deltaL": null, "deltaR": null}, "communication": {"allCommunications": ["SocketIO"], "activeCommunications": ["SocketIO"], "msgInterval": 10, "prevUpdateTime": -1}}}

'''