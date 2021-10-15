import time
from Communication.SocketIO import SocketIO
from Communication.can_io import CanIO
from Communication.http_io import HttpIO
from boat import Boat

class Communication:
    def __init__(self, boat: Boat):
        self.boat = boat
        self.can = CanIO(boat)
        self.http = HttpIO(boat)
        self.socket = SocketIO(boat)



    def start(self):
        self.canIo.start()
        self.restApiIo.start()
