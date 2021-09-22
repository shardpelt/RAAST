
class Route:

    def __init__(self, start: tuple, finish: tuple):
        self.waypoints = [start, finish]

    def addWaypoint(self, coordinates: tuple):
        self.waypoints.insert(1, coordinates)
        # TODO: Delete previous waypoint and store in database?