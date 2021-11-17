import time
import threading
from Communication.communication import Communication
from Helpers.angleHelper import AngleHelper
from Helpers.sailHelper import SailHelper
from Route.route import Route
from SensorData.sensor_data import SensorData
from Helpers.rudderHelper import RudderHelper
from Course.course import Course

"""
The boat can only sail when 
    - Required data from the sensors is available (gyroscope, gps, wind, compass)
    - Next waypoint is known
Control Loop flow:
    - Possible threat detection from sensors and checking if waypoint is reached
    - If there is not yet an wantedCourseAngle or the route has been changed, we set up an fresh course
    - If there is already an course, but the boat is not sailing at right angle, we adjust the rudder through PID control
    - If there are any changes in the wind angle, according to the wind angle we set the sail to last time, the sail is updated as well. 
    - After each loop we wait for an chosen amount of time
"""

class Boat:
    def __init__(self):
        self.controlMode = 3                                # 0: remote-control / 1: semi-autonoom / 2: autonoom / 3: simulatie
        self.controlSleep = 5                               # The sleep time which sets in after each control loop
        self.communication = Communication(self)            # Communication handler
        self.data = SensorData()                            # Data object in which every datapoint is stored
        self.route = Route(self.data)                       # Object in which the route information is stored
        self.course = Course(self.data)                     # Object in which the course is calculated and stored
        self.rudderHelper = RudderHelper(self.controlSleep) # Contains methods to determine best angle for rudder
        self.sailHelper = SailHelper()                      # Contains methods to determine best sail angle

    def start(self):
        communicationThread = threading.Thread(target=self.communication.configure)
        controlLoopThread = threading.Thread(target=self.run)

        communicationThread.start()
        controlLoopThread.start()

    def run(self):
        while True:
            if self.data.hasRequiredData() and self.route.hasNextWaypoint():

                routeChanged = False
                if self.route.checkThreatDetection():
                    self.route.findWayAroundObstacles()
                    routeChanged = True
                elif self.route.checkWaypointReached():
                    self.route.updateToNextWaypoint()
                    routeChanged = True

                if self.course.wantedAngle is None or routeChanged:
                    self.data.makeImage()
                    self.course.forgetCloseHauledCourse()
                    self.course.updateWantedAngle(self.route.currentWaypoint, self.route.boarders)

                if self.course.isOffTrack():
                    rudderAngle = self.rudderHelper.getNewBestAngle(self.data.compass.angle, self.course.wantedAngle)
                    #self.communication.sendRudderAngle(rudderAngle)
                    print(AngleHelper.toDegrees(rudderAngle))
                else:
                    self.rudderHelper.pid.reset()

                if self.data.checkChangesInWind():
                    sailAngle = self.sailHelper.getNewBestAngle(self.data.compass.angle, self.data.wind.angle)
                    #self.communication.sendSailAngle(sailAngle)

                print("CONTROL - Control loop executed -")

            else:
                print("CONTROL - Not enough data to sail -")

            time.sleep(self.controlSleep)
