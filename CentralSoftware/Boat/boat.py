from Communication.communication import Communication
from Route.route import Route
from SensorData.sensor_data import SensorData
from Helpers.rudderHelper import RudderHelper
from Course.course import Course
from Helpers.sailHelper import SailHelper

class Boat:
    def __init__(self):
        self.controlMode = 3                            # 0: remote-control / 1: semi-autonoom / 2: autonoom / 3: simulatie
        self.communication = Communication(self)        # Communication handler
        self.sensorData = SensorData()                  # Data object in which every datapoint is stored
        self.route = Route(self.sensorData)             # Object in which the route information is stored
        self.course = Course(self.sensorData)           # Object in which the course is calculated and stored
        self.rudderHelper = RudderHelper()              # Contains methods to determine best angle for rudder
        #self.sailHelper = SailHelper()                 # May be needed when the sail is programmable

    def start(self):
        self.communication.configure()

        while True:
            self.run()

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
        if self.sensorData.checkCriticalDataChanges() or routeChanged:
            self.sensorData.makeImage()
            self.course.forgetCloseHauledCourse()
            self.course.updateWantedAngle(self.route.currentWaypoint, self.route.boarders)

        # Updates to the rudder
        if self.course.isOffTrack():
            angle = self.rudderHelper.getNewBestAngle(self.course.wantedAngle, self.sensorData.compass.angle)
            self.communication.sendRudderAngle(angle)