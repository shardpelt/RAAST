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

import sys
sys.path.append("..")
sys.path.append("python_client")

import simpylc as sp
import socket_pilot.server as sv
import sailboat as sb
import wind as wn
import waypoint as wp
import obstacle as ob
import visualisation as vs

sp.World (
    sv.Server,
    sb.Sailboat,
    wn.Wind,
    wp.Waypoint,
    ob.Obstacle,
    vs.Visualisation
)
