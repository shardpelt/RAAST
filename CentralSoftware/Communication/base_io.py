class BaseIO:
    def __init__(self, boat):
        self.boat = boat
        self.ipAddress = '127.0.0.1'
        self.portNumber = 5678

    def updateBoatData(self, message: dict):
        if message["sensor"] == "wind":
            self.boat.sensorData.wind.angle = int(message["value"])
        elif message["sensor"] == "gps":
            self.boat.sensorData.currentCoordinate.latitude = float(message["latitude"])
            self.boat.sensorData.currentCoordinate.longitude = float(message["longitude"])
        elif message["sensor"] == "compass":
            self.boat.sensorData.compass.angle = int(message["value"])