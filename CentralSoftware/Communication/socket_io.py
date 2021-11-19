import json
import socket
from Communication.base_io import BaseIO

class SocketIO(BaseIO):
    def __init__(self, boat):
        super().__init__(boat)
        self.started = False
        self.boatServer = None
        self.simulationSocket = None
        self.simulationAddress = None

    @property
    def alive(self):
        return self.simulationSocket is not None

    def serverSetup(self):
        self.boatServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.boatServer.bind((self.ipAddress, self.portNumber))
        self.boatServer.listen(1)

    def waitForConnection(self):
        print("COMMUNICATION - SocketIO waiting for simulation to connect")
        self.simulationSocket, self.simulationAddress = self.boatServer.accept()
        print(f"COMMUNICATION - SOCKETIO accepted simulation at address {self.simulationAddress}")

    def receive(self):
        while self.started and self.alive:
            try:
                message = json.loads(self.simulationSocket.recv(1048).decode("utf-8"))
                print(f"COMMUNICATION - Received from simulation: {message}")
                self.updateBoatData(message)
            except socket.error:
                self.resetSocket()

    def send(self, jsonData):
        try:
            self.simulationSocket.send(bytes(jsonData, "utf-8"))
        except socket.error:
            self.resetSocket()

    def start(self):
        self.started = True
        self.serverSetup()

        while self.started:
            self.waitForConnection()
            self.receive()

    def stop(self):
        self.started = False

    def resetSocket(self):
        self.simulationSocket, self.simulationAddress = None, None