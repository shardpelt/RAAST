import sys
sys.path.append("../..")

helper = sh.SailHelper()

relativeWindAngle = 200

result = helper.getNewBestAngle(relativeWindAngle)
print (result)
