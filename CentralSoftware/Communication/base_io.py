from Route.coordinate import Coordinate

class BaseIO:
    def __init__(self, boat):
        self.boat = boat
        self.ipAddress = '127.0.0.1'
        self.portNumber = 5678
        self.sensorMap = {1: self.setWind, 2: self.setGps, 3: self.setCompass}
        self.instructionMap = {1: self.setSailRudder, 2: self.setCourse, 3: self.setWaypoint, 4: self.setControlMode, 5: self.setControlParameters}

    def processIncommingMsg(self, msg):
        if msg["type"] == "instruction":
            self.instructionMap[msg["id"]](msg["body"])
        elif msg["type"] == "sensor":
            self.sensorMap[msg["id"]](msg["body"])

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