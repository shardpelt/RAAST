from sailboat import *
from visualisation import *
from control import *
from wind import *
from waypoint import *
from obstacle import *
from communication import *

World(Control, Sailboat, Wind, Visualisation, Waypoint, Obstacle, SocketIO)
