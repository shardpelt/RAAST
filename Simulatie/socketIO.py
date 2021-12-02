#shamelessly copied from max and his communication.py
import simpylc as sp
import json
import socket

class SocketIO (sp.Module):
    def __init__(self):
        sp.Module.__init__(self)

        self.page('socketIO')
        self.group('fields', True)

        self._Address = '127.0.0.1'
        self._port = '4444'
        self._socket = None
        self._relativeWindAngle = 0
        self._relativeRudderAngle = 0

    def socketSetup(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive(self):
        while True:
            try:
                message = json.loads(self._socket.recv(8192).decode("utf-8"))
                self.updateData(message)
            except socket.error:
                print(error)
                #break

    def send(self, data):
        while True:
            try:
                self._socket.send(bytes(json.dumps(data), "utf-8"))
            except socket.error as error:
                print(error)

    def sendWindAngle(self, angle):
        angle = int(angle)
        self._socket.send(bytes(json.dumps({"type": "sensor", "id": 1, "body": {"value": angle}}), "utf-8"))

    def sendCoordinates(self, x, y):
        self._socket.send(bytes(json.dumps({"type": "sensor", "id": 2, "body": {"value": (y, x)}}), "utf-8"))

    def sendCompassAngle(self, angle):
        angle = int(angle)
        self._socket.send(bytes(json.dumps({"type": "sensor", "id": 3, "body": {"value": angle}}), "utf-8")) 

    def updateData(self, message):
        print(f"received message: {message}")
        #TODO read what data it is, and call:
        #self.local_sail_andle_set()
        #self.global_sail_angle_set()
        #self.gimbal_rudder_angle_set()

    def start(self):
        self.socketSetup()

        while True:
            self.receive()

        self.socket.close()
        print(f"socket has closed")



