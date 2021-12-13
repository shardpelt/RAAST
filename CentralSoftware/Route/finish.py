import sys
sys.path.append("..")

import Helpers.objectToDictHelper as ds

class Finish(ds.DictSerializer):
    def __init__(self, coordinateOne, coordinateTwo):
        self.coordinateOne = coordinateOne
        self.coordinateTwo = coordinateTwo
