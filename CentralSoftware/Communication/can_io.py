import json as js
import Communication.base_io as bs

class CanIO(bs.BaseIO):
    # TODO: Implement
    def __init__(self, boat):
        super().__init__(boat)
        self._boat = boat
        self.moduleIds = None
        self.loadModuleIds("Recources/sensorId.json")

    def loadModuleIds(self, fileName):
        with open(fileName) as moduleIdJson:
            self.moduleIds = js.load(moduleIdJson)

    def start(self):
        pass

    def stop(self):
        pass

    def send(self, jsonData):
        pass

    def reset(self):
        pass

    def receive(self):
        pass