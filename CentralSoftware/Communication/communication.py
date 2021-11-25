import json
import time
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
        self.msgInterval = 10
        self.prevUpdateTime = -1

    def configure(self):
        print("COMMUNICATION - Configuring communication")
        self.setActiveCommunications()

        for communication in self.allCommunications:
            if communication in self.activeCommunications and not communication.started:
                communication.start()
            else:
                communication.stop()

    def setActiveCommunications(self):
        if self.boat.controlMode == 0:                          # Controller
            self.activeCommunications = []
        elif self.boat.controlMode == 1:                        # Semi-autonomous
            self.activeCommunications = [self.can, self.http]
        elif self.boat.controlMode == 2:                        # Full-autonomous
            self.activeCommunications = [self.can, self.http]
            self.msgInterval = 60 * 60 * 6
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
        data = ["waypoints", [vars(wp) for wp in self.boat.route.waypoints]]
        self.send(json.dumps(data), [self.socket])

    def sendUpdate(self):
        update = {"boat":
                {
                    "controlMode": self.boat.controlMode,
                    "communication": {"activeCommunications": [type(c).__name__ for c in self.activeCommunications], "msgInterval": self.msgInterval},
                    "sensorData": self.boat.data.getDict(),
                    "route": self.boat.route.getDict(),
                    "course": self.boat.course.getDict()
                }
            }

        data = ["update", update]
        self.send(json.dumps(data), [self.socket, self.http])

    def shouldGiveUpdate(self) -> bool:
        currTime = time.time()

        update = False
        if self.prevUpdateTime == -1 or (currTime - self.prevUpdateTime) > self.msgInterval:
            update = True
            self.prevUpdateTime = currTime

        return update
