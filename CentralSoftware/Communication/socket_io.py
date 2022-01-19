import Communication.base_io as bs
import socket as sc
import json as js
import time as tm

class SocketIO(bs.BaseIO):
    def __init__(self, boat):
        super().__init__(boat)
        self.started = False
        self.alive = False
        self.simuSocket = None
        self.socketWrapper = None
        self.serverAddress = ('127.0.0.1', 5678)
        self.socketType = sc.AF_INET, sc.SOCK_STREAM

    def receive(self):
        if self.alive:
            try:
                message = self.socketWrapper.recv()
                self.processIncommingMsg(message)
            except sc.error as error:
                print(f"COMMUNICATION - {error}")
                self.reset()

    def send(self, jsonData):
        if self.alive:
            try:
                self.socketWrapper.send(jsonData)
            except sc.error as error:
                print(f"COMMUNICATION - {error}")
                self.reset()

    def start(self):
        self.simuSocket = sc.socket(*self.socketType)

        print("COMMUNICATION - Trying to start session with simulation")
        while True:
            try:
                self.simuSocket.connect(self.serverAddress)
            except sc.error:
                tm.sleep(2)
                continue
            print(f"COMMUNICATION - Connection established with simulation {self.simuSocket}")
            break

        self.socketWrapper = SocketWrapper(self.simuSocket)
        self.alive = True
        self.started = True

    def reset(self):
        self.alive = False
        self.start()

    def stop(self):
        self.started = False

class SocketWrapper:
    def __init__(self, clientSocket):
        self.clientSocket = clientSocket
        self.maxMessageLength = 5000

    def send(self, anObject):
        buffer = bytes(f'{anObject:<{self.maxMessageLength}}', 'ascii')

        totalNrOfSentBytes = 0

        while totalNrOfSentBytes < self.maxMessageLength:
            nrOfSentBytes = self.clientSocket.send(buffer[totalNrOfSentBytes:])

            if not nrOfSentBytes:
                self.raiseConnectionError()

            totalNrOfSentBytes += nrOfSentBytes

    def recv(self):
        totalNrOfReceivedBytes = 0
        receivedChunks = []

        while totalNrOfReceivedBytes < self.maxMessageLength:
            receivedChunk = self.clientSocket.recv(self.maxMessageLength - totalNrOfReceivedBytes)

            if not receivedChunk:
                self.raiseConnectionError()

            receivedChunks.append(receivedChunk)
            totalNrOfReceivedBytes += len(receivedChunk)

        return js.loads(b''.join(receivedChunks).decode('ascii'))

    def raiseConnectionError(self):
        raise RuntimeError('Socket connection broken')

