import sys
sys.path.append("../..")

helper = ah.SailHelper()

relativeWindAngle = 200

result = helper.getNewBestAngle(relativeWindAngle)
print (result)
