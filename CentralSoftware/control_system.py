from CentralData.central_data_image import CentralDataImage
from Route.route import Route
from CentralData.central_data import CentralData
from pid_controller import PidController
from Communication.can_io import CannIO
from Communication.rest_api_io import RestApiIO
from course import Course

class ControlSystem:
    def __init__(self):
        self.centralData = CentralData()                # Data object in which every datapoint is stored
        self.centralDataImage = CentralDataImage()      # Storing important last used data for calculations
        self.canIo = CannIO(self.centralData)           # Communication with CAN-bus handler
        self.restApiIo = RestApiIO(self)                # Communication with API handler
        self.route = Route(self.centralData)            # Object in which the route information is stored
        self.course = Course(self.centralData)          # Object in which the course is calculated and stored
        self.pid = PidController(0.5, 0.02, 0.005)      # PID-controller which calculates best sail/rudder output

    def start(self):
        self.canIo.start()
        self.restApiIo.start()

        while True:
            self.sail()

    def updateControlLevel(self, mode):
        self.canIo.changeMode(mode)
        self.restApiIo.changeMode(mode)

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
        if self.centralData.checkCriticalDataChanges(self.centralDataImage) or routeChanged:
            self.centralDataImage.loadInCopy(self.centralData)
            self.course.forgetWantedCourse()
            self.course.update(self.route.currentWaypoint, self.route.boarders)

        # Updates the boat's mechanical
        if self.course.checkCurrentCourse():
            pidOutput = self.pid.getOutput(self.course.wantedAngle, self.centralData.compass.angle)
            self.canIo.setRudder(pidOutput)
