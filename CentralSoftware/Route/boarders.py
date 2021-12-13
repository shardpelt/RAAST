import sys
sys.path.append("..")

import Helpers.objectToDictHelper as ds

class Boarders(ds.DictSerializer):
    def __init__(self, top, down, left, right):
        self.top = top
        self.down = down
        self.left = left
        self.right = right