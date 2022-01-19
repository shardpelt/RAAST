from simpylc import *


class Waypoint (Module):
    def __init__(self):
        Module.__init__(self)

        self.page('waypoint')

        self.group('waypoints', True)

        self.waypointX = Register(0)
        self.waypointY = Register(0)
        self.waypointZ = Register(0)

        self._waypoints = [[10, 10], [11, 11]] # Must contain one, otherwise weird error..

    def setWaypoint(self, index):
        self.waypointX.set(self._waypoints[index][0])
        self.waypointY.set(self._waypoints[index][1])

