import json
import socket
import asyncio
from threading import Thread
from Communication.base_io import BaseIO

class SocketIO(BaseIO):
    def __init__(self, boat):
        super().__init__(boat)
        self.started = False
        self.simulationSocket = None
        self.simulationAddress = None
        self.threadForIncommingData = Thread(target=self.receive)

    def serverSetup(self):
        boatServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        boatServer.bind((self.ipAddress, self.portNumber))
        boatServer.listen(1)
        self.simulationSocket, self.simulationAddress = boatServer.accept()

        self.threadForIncommingData.start()

    def receive(self):
        while self.started:
            simuBoatData = json.loads(self.simulationSocket.recv(1048).decode("utf-8"))
            print(simuBoatData)
            #self.updateBoatData(simuBoatData)

    def send(self, data):
        self.simulationSocket.send(bytes(data, "utf-8"))

    def start(self):
        self.started = True
        self.serverSetup()

    def stop(self):
        self.started = False
        self.threadForIncommingData.join()