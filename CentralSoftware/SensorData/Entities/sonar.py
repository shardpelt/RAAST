import sys
sys.path.append("..")

import Helpers.objectToDictHelper as ds

class Sonar(ds.DictSerializer):
    def __init__(self):
        self.objectDetected = False
        self.totalScanAngle = 30

    def checkThreat(self):
        return self.objectDetected
