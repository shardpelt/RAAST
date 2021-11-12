import json
import socket
from Communication.base_io import BaseIO

class SocketIO(BaseIO):
    def __init__(self, boat):
        super().__init__(boat)
        self.started = False
        self.simulationSocket = None
        self.simulationAddress = None

    def serverSetup(self):
        boatServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        boatServer.bind((self.ipAddress, self.portNumber))
        boatServer.listen(1)
        print("COMMUNICATION - SocketIO waiting for simulation to connect")
        self.simulationSocket, self.simulationAddress = boatServer.accept()
        print(f"COMMUNICATION - SOCKETIO accepted simulation at address {self.simulationAddress}")
        self.receive() # Start receiving from Simulation

    def receive(self):
        while self.started:
            try:
                message = json.loads(self.simulationSocket.recv(1048).decode("utf-8"))
                print(f"COMMUNICATION - Received from simulation: {message}")
                self.updateBoatData(message)
            except socket.error as error:
                self.closeConnection()
                break

    def send(self, data):
        try:
            self.simulationSocket.send(bytes(data, "utf-8"))
        except socket.error as error:
            print(error)

    def start(self):
        self.started = True
        self.serverSetup()

    def stop(self):
        self.started = False

    def closeConnection(self):
        self.simulationSocket.close()
        self.simulationAddress = None
