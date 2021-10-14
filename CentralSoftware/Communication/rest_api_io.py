from threading import Thread
from control_system import ControlSystem

class RestApiIO(Thread):
    def __init__(self, controlSystem: ControlSystem):
        super().__init__()
        self.controlSystem = controlSystem

    def run(self) -> None:
        # TODO: Add rest api functionality to communicatie with satellite
        pass

    def changeControlLevel(self, mode):
        self.controlSystem.updateControlLevel(mode)

    def changeMode(self, mode):
        pass