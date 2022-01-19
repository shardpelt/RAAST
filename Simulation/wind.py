import simpylc as sp

class Wind (sp.Module):
    def __init__(self):
        sp.Module.__init__(self)

        self.page('wind physics')

        self.group('wind direction', True)
        self.wind_direction = sp.Register(180)
        self.relative_direction = sp.Register(0)
        self.wind_scalar = sp.Register(15)
        
    def sweep(self):
        self.wind_direction.set(self.wind_direction % 360)
        self.setRelativeWindAngle()

    def setRelativeWindAngle(self):
        self.relative_direction.set((sp.world.sailboat.sailboat_rotation - self.wind_direction) % 360)
