import math 
import sys
sys.path.append("../..")
import Helpers.angleHelper as ah
import Route.coordinate as co

helper = ah.AngleHelper()
input = [[10,350,90],[50,20,90],[90,-10,100],[45,270,50],[200,260,215]]
output = [[80,20],[40,30],[10,100],[5,135],[15,300]]
succes = 0 

#GetDeltaLeftAndRightToAngle
i = 0

while i < len(input):
    result = helper.getDeltaLeftAndRightToAngle(input[i][0],input[i][1],input[i][2])
    #print (result)
    
    if result["right"] == output[i][0] and result ["left"] == output[i][1]:
        succes += 1 
    
    i += 1
    
print ('succesRateDeltaAngle', succes)

print()

#calcAngleBetweenCoordinates
currentCoordinate = co.Coordinate (0, 0)
waypointCoordinate = co.Coordinate (10, 10)

result2 = helper.calcAngleBetweenCoordinates(currentCoordinate, waypointCoordinate)
print ('k=', result2)