from CentralData.central_data_image import CentralDataImage
from Route.route import Route
from CentralData.central_data import CentralData
from pid_controller import PID
from Communication.can_io import CannIO
from Communication.rest_api_io import RestApiIO
from course import Course

class Main:
    def __init__(self):
        self.centralData = CentralData()
        self.centralDataImage = CentralDataImage() # Storing last used central data object used for calculations
        self.canIo = CannIO(self.centralData)
        self.restApiIo = RestApiIO(self.centralData)
        self.route = Route(self.centralData)
        self.course = Course(self.centralData)
        self.pid = PID()


    def start(self):
        self.canIo.start()
        self.restApiIo.start()

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
        if self.centralData.checkCriticalDataChanges(self.centralDataImage) or routeChanged:
            self.centralDataImage.loadInCopy(self.centralData)
            self.course.forgetWantedCourse()
            self.course.update(self.route.currentWaypoint, self.route.boarders)

        # Updates the boat's mechanical
        if self.course.checkCurrentCourse():
            self.pid.Work()



