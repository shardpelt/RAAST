import sys
sys.path.append("../..")

import Boat.boat as bt
import Route.waypoint as wp
import Route.coordinate as co

# Test hasNextWaypoint
boat = bt.Boat()

boat.route.waypoints = []
boat.route.hasNextWaypoint()
if boat.route.hasNextWaypoint() == False:
    print ("Test succeeded")
else:
    print ("Test failed")

boat.route.waypoints = [1, 2]
boat.route.hasNextWaypoint()
if boat.route.hasNextWaypoint() == True:
    print ("Test succeeded")
else:
    print ("Test failed")

# Test addWaypoint
coordinate = co.Coordinate(1, 2)
waypoint = wp.Waypoint(coordinate, None)
boat.route.addWaypoint(waypoint)
print (boat.route.waypoints) #other script??

# Test updateToNextWaypoint










