import threading as th
import time as tm
import Communication.communication as co
import Sail.sail as sh
import Route.route as rt
import Sensors.sensors as se
import Rudder.rudder as rh
import Course.course as cs

"""
The boat can only sail when 
    - Required sensors from the sensors is available (gyroscope, gps, wind, compass) 
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
        self.rudder = rh.Rudder()                              # Contains methods to determine best angle for rudder
        self.sail = sh.Sail()                                  # Contains methods to determine best sail angle
        self.sensors = se.Sensors()                            # sensors object in which all the incomming sensors from the sensors is stored
        self.route = rt.Route(self)                            # Object in which the route information is stored
        self.course = cs.Course(self)                          # Object in which the course is calculated and stored
        self.communication = co.Communication(self)            # Communication handler

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
        debug_timer = tm.time()

        while True:
            tm.sleep(0.2)

            ### Input
            self.communication.receive()
            ### Input

            ### Sweep
            if self.sensors.gyroscope.isUpRight() and self.sensors.enoughDataToSail():

                # Updating route if needed
                if self.route.isUpdatable:
                    routeChanged = False
                    if self.sensors.sonar.checkThreat():
                        self.route.circumnavigateSonar()
                        routeChanged = True
                    if self.sensors.ais.checkThreat():
                        self.route.circumnavigateAis()
                        routeChanged = True
                    if self.route.checkWaypointReached():
                        self.route.updateToNextWaypoint()
                        routeChanged = True
                    if routeChanged:
                        self.course.forgetDeadzoneFlags()

                # Updating course if needed
                if self.route.hasNextWaypoint():
                    if self.course.isUpdatable:
                        self.sensors.makeImage()
                        self.course.updateWantedAngle(self.route.currentWaypoint, self.route.boarders)

                    if self.rudder.isUpdatable:
                        self.rudder.setNewBestAngle(self.sensors.compass.angle, self.course.wantedCourseAngle, self.course.tacking, self.sensors.wind)
                        self.communication.sendRudderAngle(self.rudder.wantedAngle)

                    if self.sail.isUpdatable:
                        self.sail.setNewBestAngle(self.sensors.wind.relative)
                        self.communication.sendSailAngle(self.sensors.sailAngle)
            ### Sweep

            ### Output
            self.communication.sendUpdate()
            ### Output

            ### Debug
            if debug_timer > tm.time() - 1:
                coor = (round(self.sensors.gps.coordinate.latitude, 1), round(self.sensors.gps.coordinate.longitude, 1))
                altdz = self.course.angleLeftToDead
                artdz = self.course.angleRightToDead

                #print(f"Coor:{coor}, AnglesOutOfDeadzone:{altdz, artdz}, deltasToDeadzone: {self.course.deltaL, self.course.deltaR}")
                print(f"toTheWind:{self.course.sailingToTheWind}, tacking:{self.course.tacking.inManeuver}, time:{tm.time() - self.course.tacking.timeManeuverStarted}")

                debug_timer = tm.time()
            ###