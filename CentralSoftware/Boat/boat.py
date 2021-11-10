import time
import threading
from Communication.communication import Communication
from Helpers.sailHelper import SailHelper
from Route.route import Route
from SensorData.sensor_data import SensorData
from Helpers.rudderHelper import RudderHelper
from Course.course import Course

class Boat:
    def __init__(self):
        self.controlMode = 3                            # 0: remote-control / 1: semi-autonoom / 2: autonoom / 3: simulatie
        self.communication = Communication(self)        # Communication handler
        self.sensorData = SensorData()                  # Data object in which every datapoint is stored
        self.route = Route(self.sensorData)             # Object in which the route information is stored
        self.course = Course(self.sensorData)           # Object in which the course is calculated and stored
        self.rudderHelper = RudderHelper()              # Contains methods to determine best angle for rudder
        self.sailHelper = SailHelper()                  # Contains methods to determine best sail angle

    def start(self):
        communicationThread = threading.Thread(target=self.communication.configure)
        controlLoopThread = threading.Thread(target=self.run)

        communicationThread.start()
        controlLoopThread.start()

    def run(self):
        while True:

            # Only go through the control loop if data requirements are satisfied
            if self.sensorData.hasRequiredData() and self.route.hasNextWaypoint():

                # Checks/updates to the Route
                routeChanged = False
                if self.route.checkThreatDetection():
                    self.route.findWayAroundObstacles()
                    routeChanged = True
                elif self.route.checkWaypointReached():
                    self.route.updateToNextWaypoint()
                    routeChanged = True

                # Checks/updates to the Course
                if self.course.wantedAngle is None or routeChanged:
                    self.sensorData.makeImage()
                    self.course.forgetCloseHauledCourse()
                    self.course.updateWantedAngle(self.route.currentWaypoint, self.route.boarders)

                # Checks/updates the rudder
                if self.course.isOffTrack():
                    rudderAngle = self.rudderHelper.getNewBestAngle(self.course.wantedAngle, self.sensorData.compass.angle)
                    self.communication.sendRudderAngle(rudderAngle)

                # Checks/updates the sail
                if self.sensorData.checkChangesInWind():
                    sailAngle = self.sailHelper.getNewBestAngle(self.sensorData.wind.angle)
                    self.communication.sendSailAngle(sailAngle)

                print("CONTROL - Control loop executed -")
                time.sleep(5)

            else:
                print("CONTROL - Not enough data to sail -")
                time.sleep(3)