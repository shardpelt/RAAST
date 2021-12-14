import Route.coordinate as co

class BaseIO:
    def __init__(self, boat):
        self._boat = boat
        self._sensorMap = {1: self.setWind, 2: self.setGps, 3: self.setCompass}
        self._instructionMap = {1: self.setSailRudder, 2: self.setCourse, 3: self.setWaypoint, 4: self.setControlMode, 5: self.setControlParameters}

    def processIncommingMsg(self, msg):
        for i in msg:
            if msg[i]["type"] == "instruction":
                self._instructionMap[msg[i]["id"]](msg[i]["body"])
            elif msg[i]["type"] == "sensor":
                self._sensorMap[msg[i]["id"]](msg[i]["body"])

    def setSailRudder(self, body):
        try:
            self._boat.sailHelper.shouldUpdate = self._boat.rudderHelper.shouldUpdate = self._boat.course.shouldUpdate = False
            self._boat.communication.sendRudderAngle(body["rudderAngle"])
            self._boat.communication.sendSailAngle(body["sailAngle"])
        except Exception as e:
            print(e)

    def setCourse(self, body):
        try:
            self._boat.sailHelper.shouldUpdate = self._boat.rudderHelper.shouldUpdate = True
            self._boat.course.shouldUpdate = False
            self._boat.course.wantedAngle = body["courseAngle"]
        except Exception as e:
            print(e)

    def setWaypoint(self, body):
        try:
            self._boat.sailHelper.shouldUpdate = self._boat.rudderHelper.shouldUpdate = self._boat.course.shouldUpdate = True
            self._boat.route.addWaypoint(co.Coordinate(body["latitude"], body["longitude"]))
        except Exception as e:
            print(e)

    def setControlMode(self, body):
        try:
            self._boat.controlMode = body["controlMode"]
        except Exception as e:
            print(e)

    def setControlParameters(self, body):
        #TODO: define which control parameters should be adjustable from wall
        pass

    def setWind(self, body):
        try:
            self._boat.data.set_wind(body["value"], None)
        except Exception as e:
            print(e)

    def setGps(self, body):
        try:
            self._boat.data.currentCoordinate.latitude = body["value"][0]
            self._boat.data.currentCoordinate.longitude = body["value"][1]
        except Exception as e:
            print(e)

    def setCompass(self, body):
        try:
            self._boat.data.compass.angle = body["value"]
        except Exception as e:
            print(e)