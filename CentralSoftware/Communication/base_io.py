from boat import Boat

class BaseIO:
    def __init__(self, boat: Boat):
        self.boat = boat
        self.selfIpAddress = '127.0.0.1'
        self.selfPortNumber = 5678
        self.interval = 1 if boat.controlMode == 3 else (3600 * 6)
