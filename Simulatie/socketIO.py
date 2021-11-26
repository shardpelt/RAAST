#shamelessly copied from max and his communication.py
import simpylc as sp
import json
import socket

class SocketIO():
    def __init__(self):
        self.Address = '127.0.0.1'
        self.port = '4444'
        self.socket = None

    def socketSetup(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive(self):
        while True:
            try:
                message = json.loads(self.socket.recv(1048).decode("utf-8"))
                self.updateData(message)
            except socket.error:
                print(error)
                #break

    def send(self, data):
        tru:
            self.socket.send(bytes(json.dumps(data). "utf-8"))
        except socket.error as error:
            print(error)

    def sendWindAngle(angle):
        angle = int(angle)
        socket.send(bytes(json.dumps({"type": "sensor", "id": 1, "body": {"value": angle}}), "utf-8"))

    def sendCoordinates(x,y):
        socket.send(bytes(json.dumps({"type": "sensor", "id": 2, "body": {"value": (y, x)}}), "utf-8"))

    def sendCompassAngle(angle):
        angle = int(angle)
        socket.send(bytes(json.dumps({"type": "sensor", "id": 3, "body": {"value": angle}}), "utf-8")) 

    def updateData(message):
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



