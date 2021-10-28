from Communication.base_io import BaseIO

class HttpIO(BaseIO):
    def __init__(self, boat):
        super().__init__(boat)
        self.boat = boat

    def run(self) -> None:
        # TODO: Add rest api functionality to communicatie with satellite
        pass

    def changeControlLevel(self, mode):
        self.boat.controlMode = mode

    def changeMode(self, mode):
        pass

