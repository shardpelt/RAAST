import json
import time
import Communication.socket_io as so
import Communication.can_io as ca
import Communication.http_io as ht
import Helpers.objectToDictHelper as ds

class Communication(ds.DictSerializer):
    def __init__(self, boat):
        self._boat = boat
        self._can = ca.CanIO(boat)
        self._http = ht.HttpIO(boat)
        self._socket = so.SocketIO(boat)
        self.allCommunications = [self._socket]
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
        if self._boat.controlMode == 0:                          # Controller
            self.activeCommunications = []
        elif self._boat.controlMode == 1:                        # Semi-autonomous
            self.activeCommunications = [self._can, self._http]
        elif self._boat.controlMode == 2:                        # Full-autonomous
            self.activeCommunications = [self._can, self._http]
            self.msgInterval = 60 * 60 * 6
        elif self._boat.controlMode == 3:                        # Simulation
            self.activeCommunications = [self._socket]

    def receive(self):
        for medium in self.activeCommunications:
            if medium.alive:
                medium.receive()

    def send(self, data, mediums):
        for medium in mediums:
            if medium in self.activeCommunications and medium.alive:
                medium.send(data)

    def sendRudderAngle(self, angle: int):
        data = ["rudderAngle", angle]
        self.send(json.dumps(data), [self._can, self._socket])

    def sendSailAngle(self, angle: int):
        data = ["sailAngle", angle]
        self.send(json.dumps(data), [self._can, self._socket])

    def sendWaypoints(self):
        data = ["waypoints", [vars(wp) for wp in self._boat.route.waypoints]]
        self.send(json.dumps(data), [self._socket])

    def sendUpdate(self):
        boatDict = self._boat.getDict()
        data = {"update": boatDict}
        self.send(json.dumps(data), [self._socket, self._http])

    def shouldGiveUpdate(self) -> bool:
        currTime = time.time()

        update = False
        if self.prevUpdateTime == -1 or (currTime - self.prevUpdateTime) > self.msgInterval:
            update = True
            self.prevUpdateTime = currTime

        return update