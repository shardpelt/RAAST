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
import json as js
import simpylc as sp
import lidar_pilot_base as lb

class LidarSocketpilotServer (LidarSocketPilotBase):
    def __init__ (self):
        with sc.socket (*self.socketType) as serverSocket:
            serverSocket.bind (self.address)
            serverSocket.listen (self.maxNrOfConnectionRequests)

            while True:
                self.clientSocket, address = serverSocket.accept ()

                with self.clientSocket:
                    while True:
                        sensors = {
                            'lidarDistances': sp.world.visualisation.lidar.distances,
                            'lidarHalfApertureAngle': sp.world.visualisation.lidar.halfApertureAngle
                        }
                        self.send (sensors)

                        tm.sleep (0.02)

                        actuators = self.recv ()
                        sp.world.physics.steeringAngle.set (actuators ['steeringAngle'])
                        sp.world.physics.targetVelocity.set (actuators ['targetVelocity'])
