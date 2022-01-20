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
        self.controlMode = 3                               # 0: remote-control / 1: semi-autonoom / 2: autonoom / 3: simulatie
        self.rudder = rh.Rudder()                          # Contains methods to determine best angle for rudder
        self.sail = sh.Sail()                              # Contains methods to determine best sail angle
        self.sensors = se.Sensors()                        # sensors object in which all the incomming sensors from the sensors is stored
        self.route = rt.Route(self)                        # Object in which the route information is stored
        self.course = cs.Course(self)                      # Object in which the course is calculated and stored
        self.communication = co.Communication(self)        # Communication handler

    def start(self):
        if self.controlMode == 3:
            self.communication.configure(threading = False)
            self.control(threading = False)
        else:
            self.communication.configure(threading = True)
            self.control(threading = False)

    def control(self, threading: bool):
        while True:

            ### Input
            if not threading:
                self.communication.receive()
            ### Input

            ### Sweep
            if self.sensors.enoughDataToSail():

                # Updating route
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

                # If a next waypoint is available to set sail at the course is updated
                if self.route.hasNextWaypoint():

                    # Updating course
                    if self.course.isUpdatable:
                        self.course.updateWantedAngle(self.route.currentWaypoint, self.route.boarders)

                    # Updating rudder and sail
                    if self.rudder.isUpdatable:
                        self.rudder.setNewBestAngle(self.sensors.compass.angle, self.course.wantedCourseAngle, self.course.tacking, self.sensors.wind)

                    if self.sail.isUpdatable and self.sail.isControllable:
                        self.sail.setNewBestAngle(self.sensors.wind.relative)
            ### Sweep

            ### Output
            if threading:
                if self.sensors.gyroscope.isUpRight():
                    if self.rudder.isUpdatable:
                        self.communication.sendRudderAngle(self.rudder.wantedAngle)
                    if self.sail.isUpdatable and self.sail.isControllable:
                        self.communication.sendSailAngle(self.sensors.sailAngle)
                if self.communication.shouldGiveUpdate():
                    self.communication.sendShoreUpdate()
            else:
                self.communication.sendSimuUpdate()
            ### Output