import math 
import sys
sys.path.append("../..")
import Helpers.helperBase as hb

helper = hb.HelperBase()
inputDeg = [10,20,30,40,50]
outputRad = [0.174,0.349,0.523,0.698,0.872]
inputAngles = [-10,370,50]
succes1 = 0
succes2 = 0
n = 30
left = 360
right = 60
optimal = 180-46
wind = 0

def near (a,b,delta=5e-3):
    return (2 * abs (a-b) / (a+b)) < delta

#Degree to radian
i = 0
while i < len(inputDeg):
    result = helper.toRadians(inputDeg[i])
        
    if near(result,outputRad[i]):
        succes1 += 1 
    
    i += 1
    
print ('succesRateDegreeToRadian', succes1)


#Radian to degree
i = 0
while i < len(outputRad):
    result2 = helper.toDegrees(outputRad[i])
      
    if near(result2,inputDeg[i]):
        succes2 += 1 
    
    i += 1
   
print ('succesRateRadianToDegree', succes2)


#Reduce angles
result3 = helper.reduceAngles(*inputAngles)
print ('The angles are:',result3)


#AngleIsBetweenAngles
result4 = helper.angleIsBetweenAngles(n, left, right)
print ('The angle is between the left and right side:', result4)


#WindFromDeadzone
result5 = helper.windFromDeadzone(optimal, wind)
print ('Sailing in the deadzone:', result5)


#WindFromBehind
result5 = helper.windFromBehind(optimal, wind)
print ('The wind is coming form behind:', result5)