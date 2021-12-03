#shamelessly copied from max and his communication.py
import simpylc as sp
import json
import socket
import time

class SocketIO:
    def __init__(self):
        self._address = '127.0.0.1'
        self._port = 5678
        self._socket = None
        self._relativeSailAngle = 0
        self._relativeRudderAngle = 0
        self._wayPoints = []

    def socketSetup(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._address,self._port))
        self.receive()

    def receive(self):
        while True:
            time.sleep(0.5)
            try:
                print("waiting for message")
                message = json.loads(self._socket.recv(8192).decode("utf-8"))
                self.updateData(message)
            except socket.error:
                print(error)
                #break

    def send(self, data):
        try:
            self._socket.send(bytes(json.dumps(data), "utf-8"))
            print(f'sent: {json.dumps(data)}')
        except socket.error as error:
            print(error)

    def updateWaypoints(self,waypointsDict):
        #reset waypoints list in self.
        self._wayPoints = []

        #make a list out of each waypoints coordinates and append to
        #waypoints list in self.
        for waypDict in waypointsDict:
            xCoordinate = waypDict['longitude']
            yCoordinate = waypDict['latitude']
            wayp = [xCoordinate,yCoordinate,0]
            self._wayPoints.append(wayp)

        print(self._wayPoints)
        print()

    def updateSensorData(self,sensorDataDict):
        self._relativeRudderAngle = sensorDataDict['rudderAngle']
        self._relativeSailAngle = sensorDataDict['sailAngle']

        print(f'self._rudderAngle = {self._relativeRudderAngle}, self._sailAngle = {self._relativeSailAngle}')

    def updateData(self, message):
        print(f"received message: {message}")
        print()

        dataDict = message[1]
        sensorDataDict = dataDict['boat']['sensorData']
        self.updateSensorData(sensorDataDict)

        #update self._wayPoints.
        waypointsDict = dataDict['boat']['route']['waypoints']
        self.updateWaypoints(waypointsDict)

        #TODO read what data it is, and call:
        #self.local_sail_andle_set()
        #self.global_sail_angle_set()
        #self.gimbal_rudder_angle_set()

#        received message: ['update', {'boat': {'controlMode': 3, 'communication': {'activeCommunications': ['SocketIO'], 'msgInterval': 10}, 'sensorData': {'rudderAngle': None, 'sailAngle': None, 'gyroscope': {'xPos': None, 'yPos': None, 'zPos': None}, 'currentCoordinate': {'latitude': None, 'longitude': None}, 'compass': {'angle': None}, 'wind': {'angle': None, 'speed': None}, 'sonar': {'scannedObject': False, 'totalScanAngle': 30}, 'ais': {'nearbyShips': [{'latitude': 10, 'longitude': 90}]}}, 'route': {'shouldUpdate': True, 'finish': {'top': {'latitude': 55.0, 'longitude': -16.0}, 'bottom': {'latitude': 51.0, 'longitude': -16.0}}, 'waypoints': [{'latitude': 55.0, 'longitude': -14.0}, {'latitude': 54.0, 'longitude': -12.0}, {'latitude': 53.0, 'longitude': -10.0}], 'boarders': {'top': 55.0, 'down': -16.0, 'left': 51.0, 'right': -16.0}, 'waypointMargin': 0.0003}, 'course': {'shouldUpdate': True, 'wantedAngle': None, 'wantedAngleMarge': 5, 'wantedSailMarge': 5, 'closeHauled': {'flag': False, 'chosenSide': '', 'forbiddenSide': ''}, 'tackingAngleMarge': 5, 'boarderMarge': 0.005}}}]


    def sendWindAngle(self, angle):
        angle = int(angle)
        self._socket.send(bytes(json.dumps({"type": "sensor", "id": 1, "body": {"value": angle}}), "utf-8"))

    def sendCoordinates(self, x, y):
        self._socket.send(bytes(json.dumps({"type": "sensor", "id": 2, "body": {"value": (y, x)}}), "utf-8"))

    def sendCompassAngle(self, angle):
        angle = int(angle)
        self._socket.send(bytes(json.dumps({"type": "sensor", "id": 3, "body": {"value": angle}}), "utf-8")) 

    def start(self):
        self.socketSetup()

        while True:
            self.receive()

        self.socket.close()
        print(f"socket has closed")



