from CentralData.central_data import CentralData
import copy

class CentralDataImage:
    def __init__(self):
        self.wind = None

    def loadInCopy(self, centralData : CentralData):
        self.wind = copy.deepcopy(centralData.wind)