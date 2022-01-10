import math 
import sys
sys.path.append("../..")
import Helpers.sailHelper as sh

helper = sh.SailHelper()

relativeWindAngle = 200

result = helper.getNewBestAngle(relativeWindAngle)
print (result)
