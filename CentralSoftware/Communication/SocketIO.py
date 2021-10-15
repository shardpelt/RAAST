import socket
from Communication.base_io import BaseIO
from boat import Boat

class SocketIO(BaseIO):
    def __init__(self, boat: Boat):
        super().__init__(boat)

    def receive(self):
        pass

    def send(self):
        pass

    def start(self):
        pass
