from boat import Boat

class HttpIO:
    def __init__(self, boat: Boat):
        self.boat = boat

    def run(self) -> None:
        # TODO: Add rest api functionality to communicatie with satellite
        pass

    def changeControlLevel(self, mode):
        self.boat.controlMode = mode

    def changeMode(self, mode):
        pass
