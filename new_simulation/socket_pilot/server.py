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
                        longitude = sp.evaluate(sp.world.sailboat.position_y)
                        sensors = self.toDataPackage(relativeWindAngle, compassAngle, latitude, longitude)

                        self.socketWrapper.send (sensors)

                        tm.sleep (0.02)

                        message = self.socketWrapper.recv ()
                        self.updateData(message)

    def toDataPackage(self, relativeWindAngle, compassAngle, latitude, longitude):
        sensorData = [
                {"type": "sensor", "id": 1, "body": {"value": relativeWindAngle}},
                {"type": "sensor", "id": 2, "body": {"value": (latitude, longitude)}},
                {"type": "sensor", "id": 3, "body": {"value": compassAngle}}
                ]

        return sensorData

    def updateData(self, message):
        dataDict = message['update']

        sensorDataDict = dataDict['data']
        self.updateRudderSail(sensorDataDict)

        waypointsDict = dataDict['route']['waypoints']
        self.updateWaypoints(waypointsDict)

        sp.world.sailboat.latitude = dataDict["data"]["currentCoordinate"]["latitude"]
        sp.world.sailboat.longitude = dataDict["data"]["currentCoordinate"]["longitude"]

    def updateRudderSail(self,sensorDataDict):
        if sensorDataDict['rudderAngle'] is not None:
            sp.world.sailboat._rudderAngle = sensorDataDict['rudderAngle']
        if sensorDataDict['sailAngle'] is not None:
            sp.world.sailboat._sailAngle = sensorDataDict['sailAngle']

    def updateWaypoints(self, waypointsDict):
        # Reset waypoints list in world.sailboat
        sp.world.waypoint._waypoints = []

        # Make a list out of each waypoint coordinate and append to waypoints list in world.sailboat
        for waypDict in waypointsDict:
            xCoordinate = waypDict['coordinate']['latitude']
            yCoordinate = waypDict['coordinate']['longitude']
            waypoint = [xCoordinate, yCoordinate]
            sp.world.waypoint._waypoints.append(waypoint)




    '''
    {"update": {"controlMode": 3, "route": {"shouldUpdate": true, "waypoints": [{"coordinate": {"latitude": 55.0, "longitude": -14.0}, "origin": "Predefined"}, {"coordinate": {"latitude": 54.0, "longitude": -12.0}, "origin": "Predefined"}, {"coordinate": {"latitude": 53.0, "longitude": -10.0}, "origin": "Predefined"}], "finish": {"coordinateOne": {"latitude": 55.0, "longitude": -16.0}, "coordinateTwo": {"latitude": 55.0, "longitude": -16.0}}, "boarders": {"top": 55.0, "down": -16.0, "left": 51.0, "right": -16.0}, "waypointMargin": 0.0005, "obstacleMarginKm": 2}, "communication": {"allCommunications": ["SocketIO"], "activeCommunications": ["SocketIO"], "msgInterval": 10, "prevUpdateTime": -1}, "data": {"rudderAngle": null, "sailAngle": null, "gyroscope": {"xPos": null, "yPos": null, "zPos": null}, "currentCoordinate": {"latitude": null, "longitude": null}, "compass": {"angle": null}, "wind": {"angle": null, "speed": null}, "sonar": {"objectDetected": false, "totalScanAngle": 30}, "ais": {"reach": 30, "nearbyShips": null}}, "course": {"shouldUpdate": true, "wantedAngle": null, "wantedAngleMarge": 5, "wantedSailMarge": 5, "toTheWind": null, "cantChooseSide": null, "tackingAngleMarge": 5, "boarderMarge": 0.005}, "rudderHelper": {"shouldUpdate": true, "pid": {"p": 0.5, "i": 0.02, "d": 0.0005, "yI": 0, "errorOld": 0, "prevTime": null}, "maxWantedAngle": 35}, "sailHelper": {"shouldUpdate": true, "windRightToSail": [{"wind": 0, "sail": -10, "interpolate": false}, {"wind": 90, "sail": -10, "interpolate": true}, {"wind": 135, "sail": -45, "interpolate": true}, {"wind": 180, "sail": -90, "interpolate": null}], "windLeftToSail": [{"wind": 180, "sail": 90, "interpolate": true}, {"wind": 225, "sail": 45, "interpolate": true}, {"wind": 270, "sail": 10, "interpolate": false}, {"wind": 360, "sail": 10, "interpolate": null}]}}}
    '''
