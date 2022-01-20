import sys
sys.path.append("..")

class Gyroscope:
    def __init__(self):
        self.pitch = None
        self.roll = None

    def isUpRight(self):
        if self.pitch is None and self.roll is None:
            return True
        else:
            # TODO: With pitch and roll define whether the boat is up right enough to sail
            return True