import json
from boat import Boat

class CanIO:
    def __init__(self, boat: Boat):
        #self.bus = can.interface.Bus() # TODO: Bustype?
        self.boat = boat
        self.moduleId = None
        self.loadModuleIds("Recources/sensorId.json") # TODO: Elke module een Id toewijzen

    def loadModuleIds(self, fileName):
        with open(fileName) as moduleIdJson:
            self.moduleId = json.load(moduleIdJson)

    def start(self):
        if self.boat.controlMode == 3:
            pass

    def setRudder(self, angle):
        pass

    def setSail(self, angle):
        pass
