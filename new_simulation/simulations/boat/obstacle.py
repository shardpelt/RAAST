from simpylc import *


class Obstacle (Module):
    def __init__(self):
        Module.__init__(self)

        self.page('obstacle')

        self.group('obstacles', True)

        self.obstacleX = Register(0)
        self.obstacleY = Register(0)
        self.obstacleZ = Register(0)
        
        self._obstaclesList = [[2,2,0],[3,3,0],[4,4,0]]

    def setObstacle(self,index):
        self.obstacleX = Register(self._obstaclesList[index][0])
        self.obstacleY = Register(self._obstaclesList[index][1])
        self.obstacleZ = Register(self._obstaclesList[index][2])
