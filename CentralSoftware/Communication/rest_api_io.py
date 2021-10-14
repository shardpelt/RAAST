from threading import Thread
from CentralData.central_data import CentralData

class RestApiIO(Thread):
    def __init__(self, centralData: CentralData):
        super().__init__()
        self.data = centralData

    def run(self) -> None:
        # TODO: Add rest api functionality to communicatie with satellite
        pass
