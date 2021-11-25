import socket
import json
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("127.0.0.1", 5678))
print("--- CONNECTED TO BOAT ---")

def receive():
    while True:
        print("From boat: ", json.loads(server.recv(5000).decode("utf-8")))

receiveThread = threading.Thread(target=receive)
receiveThread.start()

while True:
    sort = input("[1: Coast instruction, 2: Sensor input] -> ")
    if sort == "1":
        instruction = input("1: setSailRudder, 2: setCourse, 3: setWaypoint, 4: setControlMode, 5: setControlParameters")
        if instruction == "1":
            s = int(input("sailAngle: "))
            r = int(input("rudderAngle: "))
            server.send(bytes(json.dumps({"type": "instruction", "id": 1, "body": {"sailAngle": s, "rudderAngle": r}}), "utf-8"))
        if instruction == "2":
            ca = float(input("courseAngle: "))
            server.send(bytes(json.dumps({"type": "instruction", "id": 2, "body": {"courseAngle": ca}}), "utf-8"))
        if instruction == "3":
            lat = float(input("latitude: "))
            lon = float(input("longitude: "))
            server.send(bytes(json.dumps({"type": "instruction", "id": 3, "body": {"latitude": lat, "longitude": lon}}), "utf-8"))
        if instruction == "4":
            cm = float(input("controlMode: "))
            server.send(bytes(json.dumps({"type": "instruction", "id": 4, "body": {"controlMode": cm}}), "utf-8"))
    elif sort == "2":
        sensor = input("[1: Wind, 2: Gps, 3: Compass] -> ")
        if sensor == "1":
            v = int(input("windAngle: "))
            server.send(bytes(json.dumps({"type": "sensor", "id": 1, "body": {"value": v}}), "utf-8"))
        if sensor == "2":
            lat = float(input("latitude: "))
            lon = float(input("longitude: "))
            server.send(bytes(json.dumps({"type": "sensor", "id": 2, "body": {"value": (lat, lon)}}), "utf-8"))
        if sensor == "3":
            v = int(input("compassAngle: "))
            server.send(bytes(json.dumps({"type": "sensor", "id": 3, "body": {"value": v}}), "utf-8"))