import sys
sys.path.append("..")

import Helpers.objectToDictHelper as ds

class Compass(ds.DictSerializer):
    def __init__(self):
        self.angle = None

    def hasData(self):
        return self.angle is not None