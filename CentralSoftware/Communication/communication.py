import sys
sys.path.append("..")

import time as ti
import threading as th
import Communication.socket_io as so
import Communication.can_io as ca
import Communication.http_io as ht
import Helpers.json_helper as jh

class Communication:
    def __init__(self, boat):
        self._boat = boat
        self._can = ca.CanIO(boat)
        self._http = ht.HttpIO(boat)
        self._socket = so.SocketIO(boat)
        self.allCommunications = [self._socket]
        self.activeCommunications = []
        self.msgInterval = 10
        self.prevUpdateTime = -1

    def configure(self, threading: bool) -> None:
        print("\nCOMMUNICATION - Configuring communication")
        self.setActiveCommunications()

        for communication in self.allCommunications:
            if communication in self.activeCommunications and not communication.started:
                if threading:
                    communicationThread = th.Thread(target=communication.start)
                    communicationThread.start()
                else:
                    communication.start()
            else:
                communication.stop()

    def setActiveCommunications(self) -> None:
        if self._boat.controlMode == 0:                          # Controller
            self.activeCommunications = []
        elif self._boat.controlMode == 1:                        # Semi-autonomous
            self.activeCommunications = [self._can, self._socket]
        elif self._boat.controlMode == 2:                        # Full-autonomous
            self.activeCommunications = [self._can, self._http]
            self.msgInterval = 60 * 60 * 6
        elif self._boat.controlMode == 3:                        # Simulation
            self.activeCommunications = [self._socket]

    def receive(self) -> None:
        for medium in self.activeCommunications:
            if medium.alive:
                medium.receive()

    def send(self, data, mediums) -> None:
        for medium in mediums:
            if medium in self.activeCommunications and medium.alive:
                medium.send(data)

    def sendSimuUpdate(self) -> None:
        self.send(jh.JsonHelper.makePackage("update", self._boat), [self._socket])

    def sendShoreUpdate(self) -> None:
        # TODO: Bepaal aan de hand van de situatie wat voor soort bericht er moet worden opgesteld om naar de kust te sturen
        self.send(jh.JsonHelper.makePackage("update", self._boat), [self._socket])

    def sendRudderAngle(self, angle: int) -> None:
        self.send(jh.JsonHelper.makePackage("rudderAngle", angle), [self._can])

    def sendSailAngle(self, angle: int) -> None:
        self.send(jh.JsonHelper.makePackage("sailAngle", angle), [self._can])

    def shouldGiveUpdate(self) -> bool:
        currTime = ti.time()

        update = False
        if self.prevUpdateTime == -1 or (currTime - self.prevUpdateTime) > self.msgInterval:
            update = True
            self.prevUpdateTime = currTime

        return update