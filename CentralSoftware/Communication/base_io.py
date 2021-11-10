from Route.coordinate import Coordinate
from Helpers.helperBase import HelperBase

class BaseIO:
    def __init__(self, boat):
        self.boat = boat
        self.ipAddress = '127.0.0.1'
        self.portNumber = 5678

    def updateBoatData(self, message: dict):
        #for item in message:
        if message["sensor"] == "wind":
            self.boat.sensorData.wind.angle = HelperBase.toRadians(int(message["value"]))
        elif message["sensor"] == "gps":
            self.boat.sensorData.currentCoordinate.latitude = HelperBase.toRadians(message["latitude"])
            self.boat.sensorData.currentCoordinate.longitude = HelperBase.toRadians(message["longitude"])
        elif message["sensor"] == "compass":
            self.boat.sensorData.compass.angle = HelperBase.toRadians(int(message["value"]))