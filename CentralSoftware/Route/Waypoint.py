import Route.coordinate as co



class Waypoint:
    def __init__(self, coordinate: co.Coordinate, traverse):
        self.coordinate = coordinate
        self.traverse = traverse