from central_data import *
import json
import can

class CannIO:

    def __init__(self):
        #self.bus = can.interface.Bus() # TODO: Het bustype is vereist -> wordt bepaald door ander team
        self.moduleId = None
        self.loadModuleIds("Recources/ModuleId.json") # TODO: Elke module een Id toewijzen en verwerken in json file
        self.centralData = CentralData()

    def loadModuleIds(self, fileName):
        with open(fileName) as moduleIdJson:
            self.moduleId = json.load(moduleIdJson)

    # TODO: - Write methods which accept incomming data from CAN
    #       - Save incomming data from CAN to centralData object
    #       - Methods which can write data to the rudder/ (sail)