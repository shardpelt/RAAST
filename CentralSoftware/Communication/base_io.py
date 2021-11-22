from Route.coordinate import Coordinate

class BaseIO:
    def __init__(self, boat):
        self.boat = boat
        self.ipAddress = '127.0.0.1'
        self.portNumber = 5678
        self.instructionMap = {1: self.setSailRudder, 2: self.setCourse, 3: self.setWaypoint, 4: self.setControlMode, 5: self.setControlParameters}

    def processIncommingMsg(self, msg):
        self.instructionMap[msg["instructionId"]](msg["body"])

    def setSailRudder(self, body):
        try:
            self.boat.sailHelper.shouldUpdate = self.boat.rudderHelper.shouldUpdate = self.boat.course.shouldUpdate = False
            self.boat.communication.sendRudderAngle(body["rudderAngle"])
            self.boat.communication.sendSailAngle(body["sailAngle"])
        except Exception as e:
            return e

    def setCourse(self, body):
        try:
            self.boat.sailHelper.shouldUpdate = self.boat.rudderHelper.shouldUpdate = True
            self.boat.course.shouldUpdate = False
            self.boat.course.wantedAngle = body["courseAngle"]
        except Exception as e:
            return e

    def setWaypoint(self, body):
        try:
            self.boat.sailHelper.shouldUpdate = self.boat.rudderHelper.shouldUpdate = self.boat.course.shouldUpdate = True
            self.boat.route.addWaypoint(Coordinate(body["latitude"], body["longitude"]))
        except Exception as e:
            return e

    def setControlMode(self, body):
        try:
            self.boat.controlMode = body["controlMode"]
        except Exception as e:
            return e

    def setControlParameters(self, body):
        #TODO: define which control parameters should be adjustable from wall
        pass

    def updateBoatData(self, message: dict):
        if message["sensor"] == "wind":
            self.boat.data.wind.angle = int(message["value"])
        elif message["sensor"] == "gps":
            self.boat.data.currentCoordinate.latitude = float(message["latitude"])
            self.boat.data.currentCoordinate.longitude = float(message["longitude"])
        elif message["sensor"] == "compass":
            self.boat.data.compass.angle = int(message["value"])