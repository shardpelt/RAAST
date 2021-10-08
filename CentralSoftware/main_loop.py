from Route.route import Route
from central_data import CentralData
from pid_controller import PID
from Communication.can_io import CannIO
from Communication.satellite_io import SatelliteIO
from course import Course

class Main:
    def __init__(self):
        self.centralData = CentralData()
        self.canIo = CannIO(self.centralData)
        self.satelliteIo = SatelliteIO(self.centralData)
        self.route = Route(self.centralData)
        self.course = Course(self.centralData)
        self.pid = PID()
        self.controlMode = 2

    def start(self):
        while True:
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
                self.course.forgetWantedCourse()
                self.course.update(self.route.currentWaypoint, self.route.boarders)

            # Updates the boat's mechanical
            if self.course.checkCurrentCourse():
                self.pid.Work()
