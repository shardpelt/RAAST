from copy import copy
from Route.coordinate import Coordinate
import socket as sc

class BaseIO:
    def __init__(self, boat):
        self.boat = boat
        self.sensorMap = {1: self.setWind, 2: self.setGps, 3: self.setCompass}
        self.instructionMap = {1: self.setSailRudder, 2: self.setCourse, 3: self.setWaypoint, 4: self.setControlMode, 5: self.setControlParameters}

    def getDict(self):
        return type(copy(self)).__name__

    def processIncommingMsg(self, msg):
        print(f"Msg from simulation: {msg}")

        for i in msg:
            print(f"item: {i}")
            if msg[i]["type"] == "instruction":
                self.instructionMap[msg[i]["id"]](msg[i]["body"])
            elif msg[i]["type"] == "sensor":
                self.sensorMap[msg[i]["id"]](msg[i]["body"])

    def setSailRudder(self, body):
        try:
            self.boat.sailHelper.shouldUpdate = self.boat.rudderHelper.shouldUpdate = self.boat.course.shouldUpdate = False
            self.boat.communication.sendRudderAngle(body["rudderAngle"])
            self.boat.communication.sendSailAngle(body["sailAngle"])
        except Exception as e:
            print(e)

    def setCourse(self, body):
        try:
            self.boat.sailHelper.shouldUpdate = self.boat.rudderHelper.shouldUpdate = True
            self.boat.course.shouldUpdate = False
            self.boat.course.wantedAngle = body["courseAngle"]
        except Exception as e:
            print(e)

    def setWaypoint(self, body):
        try:
            self.boat.sailHelper.shouldUpdate = self.boat.rudderHelper.shouldUpdate = self.boat.course.shouldUpdate = True
            self.boat.route.addWaypoint(Coordinate(body["latitude"], body["longitude"]))
        except Exception as e:
            print(e)

    def setControlMode(self, body):
        try:
            self.boat.controlMode = body["controlMode"]
        except Exception as e:
            print(e)

    def setControlParameters(self, body):
        #TODO: define which control parameters should be adjustable from wall
        pass

    def setWind(self, body):
        try:
            self.boat.data.set_wind(body["value"], None)
        except Exception as e:
            print(e)

    def setGps(self, body):
        try:
            self.boat.data.currentCoordinate.latitude = body["value"][0]
            self.boat.data.currentCoordinate.longitude = body["value"][1]
        except Exception as e:
            print(e)

    def setCompass(self, body):
        try:
            self.boat.data.compass.angle = body["value"]
        except Exception as e:
            print(e)