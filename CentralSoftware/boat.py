from Communication.communication import Communication
from Route.route import Route
from CentralData.central_data import CentralData
from pid_controller import PidController
from course import Course

class Boat:
    def __init__(self):
        self.controlMode = 3                            # 0: remote-control / 1: semi-autonoom / 2: autonoom / 3: simulatie
        self.centralData = CentralData()                # Data object in which every datapoint is stored
        self.communication = Communication(self)        # Communication handler
        self.route = Route(self.centralData)            # Object in which the route information is stored
        self.course = Course(self.centralData)          # Object in which the course is calculated and stored
        self.pid = PidController(0.5, 0.02, 0.005)      # PID-controller which calculates best sail/rudder output

    def start(self):
        self.communication.configure()

        while True:
            self.sail()

    def sail(self):
        # Checks/updates to the Route
        routeChanged = False
        if self.route.checkThreatDetection():
            self.route.findWayAroundObstacles()
            routeChanged = True
        elif self.route.checkWaypointReached():
            self.route.updateToNextWaypoint()
            routeChanged = True

        # Checks/updates to the Course
        if self.centralData.checkCriticalDataChanges() or routeChanged:
            self.centralData.makeImage()
            self.course.forgetCloseHauledCourse()
            self.course.updateWantedAngle(self.route.currentWaypoint, self.route.boarders)

        # Updates the boat's mechanical
        if not self.course.isOnTrack():
            angle = self.pid.getBestNextAngle(self.course.wantedAngle, self.centralData.compass.angle)
            self.communication.sendRudderAngle(angle)
