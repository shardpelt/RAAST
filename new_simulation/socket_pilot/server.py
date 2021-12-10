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
import socket_wrapper as sw

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
                        windAngle = sp.evaluate(sp.world.sailboat._relativeWindAngle)
                        compassAngle = sp.evaluate(sp.world.sailboat._compassAngle)
                        x = sp.world.sailboat._x
                        y = sp.world.sailboat._y
                        
                        sensors = self.getData(windAngle, compassAngle, x, y)

                        self.socketWrapper.send (sensors)

                        tm.sleep (0.02)

                        message = self.socketWrapper.recv ()
                        #sp.world.physics.steeringAngle.set (actuators ['steeringAngle'])
                        print(message)

    def getData(self,relativeWindAngle,compassAngle,x,y):
        sensorData = {
                1: {"type": "sensor", "id": 1, "body": {"value": relativeWindAngle}},
                2: {"type": "sensor", "id": 2, "body": {"value": (y, x)}},
                3: {"type": "sensor", "id": 3, "body": {"value": compassAngle}}
                }
        return sensorData

    '''
    def getData(self,relativeWindAngle,compassAngle,x,y):
        sensorData = {'sensorData':{ 
                {"type": "sensor", "id": 1, "body": {"value": relativeWindAngle}},
                {"type": "sensor", "id": 2, "body": {"value": (y, x)}},
                {"type": "sensor", "id": 3, "body": {"value": compassAngle}}}
                }
        return sensorData
    '''


    def updateWaypoints(self,waypointsDict):
        #reset waypoints list in self.
        sp.world.sailboat._waypoints = []

        #make a list out of each waypoints coordinates and append to
        #waypoints list in self.
        for waypDict in waypointsDict:
            xCoordinate = waypDict['longitude']
            yCoordinate = waypDict['latitude']
            wayp = [xCoordinate,yCoordinate,0]
            sp.world.sailboat._waypoints.append(wayp)

    def updateSensorData(self,sensorDataDict):
        sp.world.sailboat._relativeRudderAngle = sensorDataDict['rudderAngle']
        sp.world.sailboat._relativeSailAngle = sensorDataDict['sailAngle']

    def updateData(self, message):
        dataDict = message[1]
        sensorDataDict = dataDict['boat']['sensorData']
        self.updateSensorData(sensorDataDict)

        #update self._wayPoints.
        waypointsDict = dataDict['boat']['route']['waypoints']
        self.updateWaypoints(waypointsDict)
