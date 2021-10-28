import json
import socket
import asyncio

# testServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# testServer.bind(("127.0.0.1", 5697))
# testServer.listen(1)
# boatSocket, boatAddress = testServer.accept()
#
# print(boatSocket, boatAddress)
#
# while True:
#     boatData = json.loads(boatSocket.recv(1048).decode("utf-8"))
#     print(boatData)

# simulationServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# simulationServer.connect(("localhost", 5678))
#
# input("send?")
# simulationServer.send(bytes(json.dumps([1, 2, 3]), "utf-8"))

class X:
    i = 8
    def __init__(self):
        self.e = 5

    def a(self):
        print(self.i)

x = X()
x.a()


