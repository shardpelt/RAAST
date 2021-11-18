from simpylc import *


class Waypoint (Module):
    def __init__(self):
        Module.__init__(self)

        self.page('waypoint')

        self.group('waypoints', True)

        self.waypointX = Register(0)
        self.waypointY = Register(0)
        self.waypointZ = Register(0)

        self._waywaypointypointy = [[2,-2,0],[3,-3,0],[4,-4,0]]

    def setWay(self,index):
        self.waypointX = Register(self._waywaypointypointy[index][0])
        self.waypointY = Register(self._waywaypointypointy[index][1])
        self.waypointZ = Register(self._waywaypointypointy[index][2])

