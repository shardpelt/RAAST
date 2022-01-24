import Route.coordinate as co

class BaseIO:
    def __init__(self, boat):
        self._boat = boat
        self._sensorMap = {1: self.setWind, 2: self.setGps, 3: self.setCompass}
        self._instructionMap = {1: self.setSailRudder, 2: self.setCourse, 3: self.setWaypoint, 4: self.setControlMode, 5: self.setControlParameters}

    def processIncommingMsg(self, msg):
        for oneMsg in msg:
            if oneMsg["type"] == "instruction":
                self._instructionMap[oneMsg["id"]](oneMsg["body"])
            elif oneMsg["type"] == "sensor":
                self._sensorMap[oneMsg["id"]](oneMsg["body"])

    def setSailRudder(self, body):
        try:
            self._boat.sail.isUpdatable = self._boat.rudder.isUpdatable = self._boat.course.isUpdatable = False
            self._boat.communication.sendRudderAngle(body["rudderAngle"])
            self._boat.communication.sendSailAngle(body["sailAngle"])
        except Exception as e:
            print(e)

    def setCourse(self, body):
        try:
            self._boat.sail.isUpdatable = self._boat.rudder.isUpdatable = True
            self._boat.course.isUpdatable = False
            self._boat.course.wantedAngle = body["courseAngle"]
        except Exception as e:
            print(e)

    def setWaypoint(self, body):
        try:
            self._boat.sail.isUpdatable = self._boat.rudder.isUpdatable = self._boat.course.isUpdatable = True
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
            self._boat.sensors.set_wind(body["value"])
        except Exception as e:
            print(e)

    def setGps(self, body):
        try:
            self._boat.sensors.set_gps(body["value"][0], body["value"][1])
        except Exception as e:
            print(e)

    def setCompass(self, body):
        try:
            self._boat.sensors.set_compassAngle(body["value"])
        except Exception as e:
            print(e)

    def receive(self):
        raise NotImplementedError("Communication interface should implement this!..")

    def send(self, jsonData):
        raise NotImplementedError("Communication interface should implement this!..")

    def start(self):
        raise NotImplementedError("Communication interface should implement this!..")

    def reset(self):
        raise NotImplementedError("Communication interface should implement this!..")

    def stop(self):
        raise NotImplementedError("Communication interface should implement this!..")