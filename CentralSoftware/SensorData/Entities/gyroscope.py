import sys
sys.path.append("..")

import Helpers.objectToDictHelper as ds

class Gyroscope(ds.DictSerializer):
    def __init__(self):
        self.xPos = None
        self.yPos = None
        self.zPos = None

    # TODO: With 3? given inputs define whether the boat is up right or not
    def isUpRight(self):
        return True