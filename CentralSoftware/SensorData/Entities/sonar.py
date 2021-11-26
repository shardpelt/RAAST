class Sonar:
    def __init__(self):
        self.scannedObject = False
        self.totalScanAngle = 30

    def checkThreat(self):
        return self.scannedObject

    # def getScanAnalysis(self, sonar) -> tuple:
    #     i = 0 - self.totalScanAngle / 2
    #     firstAngle = self.infinity
    #     lastAngle = self.infinity
    #     smallestDistance = self.infinity
    #
    #     while i < self.totalScanAngle / 2:
    #         if sonar[i] < self.infinity:
    #             if sonar[i] < smallestDistance:
    #                 smallestDistance = sonar[i]
    #             if firstAngle == self.infinity:
    #                 firstAngle = i
    #             else:
    #                 lastAngle = i
    #
    #         i = i + 1
    #
    #     return firstAngle, lastAngle, smallestDistance