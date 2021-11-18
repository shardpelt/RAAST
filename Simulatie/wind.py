from simpylc import *


class Wind (Module):
    def __init__(self):
        Module.__init__(self)

        self.page('wind physics')

        self.group('wind direction', True)
        self.wind_direction = Register(270)
        self.wind_scalar = Register(15)

    def sweep(self):
        #self.wind_direction.set(self.wind_direction + random.uniform(-1, 1))
        self.wind_direction.set(self.wind_direction % 360)
