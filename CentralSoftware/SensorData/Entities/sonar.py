class Sonar:
    def __init__(self):
        self.scan = []
        self.infinity = 1_000_000

    def getSeenObjects(self, sonar):
        i = 0 - len(sonar) / 2
        leftAngle = self.infinity
        rightAngle = self.infinity
        smallestDistance = self.infinity

        while i < len(sonar) / 2:
            if sonar[i] < self.infinity:
                if sonar[i] < smallestDistance:
                    smallestDistance = sonar[i]
                if leftAngle == self.infinity:
                    leftAngle = i
                else:
                    rightAngle = i

            i = i + 1

        return [leftAngle, rightAngle, smallestDistance]
