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
        self.communication.configure()

        while True:
            if self.sensorData.gyroscope.isUpRight():   # Only go through the control loop if the boat is up right
                self.run()

    # TODO: Make this loop asyncio
    def run(self):
        # Checks/updates to the Route
        routeChanged = False
        if self.route.checkThreatDetection():
            self.route.findWayAroundObstacles()
            routeChanged = True
        elif self.route.checkWaypointReached():
            self.route.updateToNextWaypoint()
            routeChanged = True

        # Checks/updates to the Course
        if routeChanged:
            self.sensorData.makeImage()
            self.course.forgetCloseHauledCourse()
            self.course.updateWantedAngle(self.route.currentWaypoint, self.route.boarders)

        # Checks/updates the rudder
        if self.course.isOffTrack():
            rudderAngle = self.rudderHelper.getNewBestAngle(self.course.wantedAngle, self.sensorData.compass.angle)
            self.communication.sendRudderAngle(rudderAngle)

        # Checks/updates the sail
        if self.sensorData.checkCriticalDataChanges():
            sailAngle = self.sailHelper.getNewBestAngle(self.sensorData.wind.angle)
            self.communication.sendSailAngle(sailAngle)