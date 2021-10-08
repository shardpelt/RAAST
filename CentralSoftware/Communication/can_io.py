import json
from central_data import CentralData
import can

class CannIO:
    def __init__(self, centralData: CentralData):
        #self.bus = can.interface.Bus() # TODO: Het bustype is vereist -> wordt bepaald door ander team
        self.data = centralData
        self.moduleId = None
        self.loadModuleIds("Recources/sensorId.json") # TODO: Elke module een Id toewijzen

    def loadModuleIds(self, fileName):
        with open(fileName) as moduleIdJson:
            self.moduleId = json.load(moduleIdJson)

    def start(self):
        while True:
            # TODO: Open ports for incomming can data/ write data to centralData object

            pass
