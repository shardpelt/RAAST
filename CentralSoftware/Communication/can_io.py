import json
from threading import Thread
from CentralData.central_data import CentralData

class CannIO(Thread):
    def __init__(self, centralData: CentralData):
        super().__init__()
        #self.bus = can.interface.Bus() # TODO: Bustype?
        self.data = centralData
        self.moduleId = None
        self.loadModuleIds("Recources/sensorId.json") # TODO: Elke module een Id toewijzen

    def loadModuleIds(self, fileName):
        with open(fileName) as moduleIdJson:
            self.moduleId = json.load(moduleIdJson)

    def changeMode(self, mode):
        pass

    def run(self):
        while True:
            # TODO: Open ports for incomming can data/ write data to centralData object

            pass

    def setRudder(self, angle):
        pass

    def setSail(self, angle):
        pass
