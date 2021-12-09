from sailboat import *
from visualisation import *
from wind import *
from waypoint import *
from obstacle import *
from socketIO import *

World(SocketIO, Sailboat, Wind, Visualisation, Waypoint, Obstacle)
