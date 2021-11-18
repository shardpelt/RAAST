import json
from Communication.socket_io import SocketIO
from Communication.can_io import CanIO
from Communication.http_io import HttpIO

class Communication:
    def __init__(self, boat):
        self.boat = boat
        self.can = CanIO(boat)
        self.http = HttpIO(boat)
        self.socket = SocketIO(boat)
        self.allCommunications = [self.socket]
        self.activeCommunications = None
        self.messageInterval = 1

    def configure(self):
        print("COMMUNICATION - Configuring communication")
        self.setActiveCommunications()

        for communication in self.allCommunications:
            if communication in self.activeCommunications and not communication.started:
                communication.start()

    def setActiveCommunications(self):
        if self.boat.controlMode == 0:                          # Controller
            self.activeCommunications = []
        elif self.boat.controlMode == 1:                        # Semi-autonomous
            self.activeCommunications = [self.can, self.http]
        elif self.boat.controlMode == 2:                        # Full-autonomous
            self.activeCommunications = [self.can, self.http]
            self.messageInterval = 60 * 60 * 6
        elif self.boat.controlMode == 3:                        # Simulation
            self.activeCommunications = [self.socket]

    def send(self, data, mediums):
        for medium in mediums:
            if medium in self.activeCommunications and medium.alive:
                medium.send(data)

    def sendRudderAngle(self, angle: int):
        data = ["rudderAngle", angle]
        self.send(json.dumps(data), [self.can, self.socket])

    def sendSailAngle(self, angle: int):
        data = ["sailAngle", angle]
        self.send(json.dumps(data), [self.can, self.socket])

    def sendWaypoints(self):
        data = ["waypoints", [wp.__dict__ for wp in self.boat.route.waypoints]]
        self.send(json.dumps(data), [self.socket])

    def sendAllBoatData(self):
        data = ["allBoatData", self.boat]
        self.send(data, [self.socket, self.http])
