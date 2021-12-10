class Compass:
    def __init__(self):
        self.angle = None

    def hasData(self):
        return self.angle is not None