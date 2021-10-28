class BaseIO:
    def __init__(self, boat):
        self.boat = boat
        self.ipAddress = '127.0.0.1'
        self.portNumber = 5678

    def updateBoatData(self, updatedBoat):
        self.boat = updatedBoat