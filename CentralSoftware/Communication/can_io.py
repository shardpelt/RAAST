import json
from central_data import CentralData
import can

class CannIO:
    def __init__(self, centralData: CentralData):
        #self.bus = can.interface.Bus() # TODO: Het bustype is vereist -> wordt bepaald door ander team
        self.centralData = centralData
        self.moduleId = None
        self.loadModuleIds("Recources/sensorId.json") # TODO: Elke module een Id toewijzen

    def loadModuleIds(self, fileName):
        with open(fileName) as moduleIdJson:
            self.moduleId = json.load(moduleIdJson)

    def start(self):
        pass

    # TODO: - Write methods which accept incomming data from CAN
    #       - Save incomming data from CAN to centralData object
    #       - Methods which can write data to the rudder/ (sail)
