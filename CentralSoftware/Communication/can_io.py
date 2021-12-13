import json as js
import Communication.base_io as bs

class CanIO(bs.BaseIO):
    # TODO: asyncio
    def __init__(self, boat):
        super().__init__(boat)
        #self.bus = can.interface.Bus() # TODO: Bustype?
        self.boat = boat
        self.moduleId = None
        self.loadModuleIds("Recources/sensorId.json") # TODO: Elke module een Id toewijzen

    def loadModuleIds(self, fileName):
        with open(fileName) as moduleIdJson:
            self.moduleId = js.load(moduleIdJson)

    def start(self):
        if self.boat.controlMode == 3:
            pass

    def stop(self):
        pass

    def send(self):
        pass