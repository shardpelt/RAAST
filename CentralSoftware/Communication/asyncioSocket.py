import json
import socket
import asyncio

class AsyncIOSocket:
    def __init__(self):
        self.started = False
        self.simulationSocket = None
        self.simulationAddress = None
        self.loop = None

    async def configure(self):
        self.started = True
        self.loop = asyncio.get_event_loop()

        boatServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        boatServer.bind(("127.0.0.1", 5678))
        boatServer.listen(1)
        print("waiting for connection")
        self.simulationSocket, self.simulationAddress = await self.loop.sock_accept(boatServer)
        print("client connected", self.simulationAddress)

        self.loop.create_task(self.receive())

    async def receive(self):
        while self.started:
            data = await self.loop.sock_recv(self.simulationSocket, 1024)
            simuBoatData = json.loads(data.decode("utf-8"))
            print("Received from simulation: ", simuBoatData)

    async def send(self, data):
        await self.loop.sock_sendall(bytes(data, "utf-8"))

    def start(self):
        asyncio.run(self.configure())

    def stop(self):
        self.started = False

s = AsyncIOSocket()
s.start()
