import sys
sys.path.append("..")

import Helpers.objectToDictHelper as ds

class Coordinate(ds.DictSerializer):
    def __init__(self, latitude = None, longitude = None):
        self.latitude = latitude
        self.longitude = longitude

    def hasData(self) -> bool:
        return self.latitude is not None and self.longitude is not None