import threading as th
import time
import time as tm
import Communication.communication as co
import Helpers.sailHelper as sh
import Route.route as rt
import SensorData.sensor_data as sd
import Helpers.rudderHelper as rh
import Course.course as cs

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
        self.controlMode = 3                                   # 0: remote-control / 1: semi-autonoom / 2: autonoom / 3: simulatie
        self.route = rt.Route(self)                            # Object in which the route information is stored
        self.communication = co.Communication(self)            # Communication handler
        self.data = sd.SensorData()                            # Data object in which every datapoint is stored
        self.course = cs.Course(self)                          # Object in which the course is calculated and stored
        self.rudderHelper = rh.RudderHelper()                  # Contains methods to determine best angle for rudder
        self.sailHelper = sh.SailHelper()                      # Contains methods to determine best sail angle

    def start(self):
        if self.controlMode == 3: # If simulation mode -> cancel out threading
            self.communication.configure()
            self.run()
        else:
            communicationThread = th.Thread(target=self.communication.configure)
            tm.sleep(1)
            controlLoopThread = th.Thread(target=self.run)

            communicationThread.start()
            controlLoopThread.start()

    def run(self):
        debug_timer = time.time()

        while True:
            tm.sleep(0.2)

            ### Input
            self.communication.receive()
            ###

            ### Sweep
            if self.data.hasRequiredData() and self.route.hasNextWaypoint():
                routeChanged = False
                if self.route.shouldUpdate:
                    if self.data.sonar.checkThreat():
                        self.route.circumnavigateSonar()
                        self.data.sonar.objectDetected = False
                        routeChanged = True
                    elif self.data.ais.checkThreat():
                        self.route.circumnavigateAis()
                        routeChanged = True
                    elif self.route.checkWaypointReached():
                        self.route.updateToNextWaypoint()
                        routeChanged = True

                if self.course.shouldUpdate: #and (self.course.wantedAngle is None or routeChanged):
                    self.data.makeImage()
                    self.course.forgetToTheWindCourse()
                    self.course.updateWantedAngle(self.route.currentWaypoint, self.route.boarders)
                ###

                ### Output
                if self.rudderHelper.shouldUpdate:
                    self.data.rudderAngle = self.rudderHelper.getNewBestAngle(self.data.compass.angle, self.course.wantedAngle)
                    self.communication.sendRudderAngle(self.data.rudderAngle)

                if self.sailHelper.shouldUpdate: #and self.data.checkChangesInWind():
                    self.data.sailAngle = self.sailHelper.getNewBestAngle(self.data.wind.relative)
                    self.communication.sendSailAngle(self.data.sailAngle)

            self.communication.sendUpdate()

            if debug_timer > time.time() - 1:
                coor = (round(self.data.currentCoordinate.latitude, 1), round(self.data.currentCoordinate.longitude, 1))
                #wantedAngle = round(self.course.wantedAngle)
                #sailAngle = round(self.data.sailAngle)
                #rudder = round(self.data.rudderAngle)

                waypoints = []
                for waypoint in self.route.waypoints:
                    waypoints.append((waypoint.coordinate.latitude, waypoint.coordinate.longitude))

                print(f"Coor:{coor}, Waypoints:{waypoints}")
                debug_timer = time.time()
            ###