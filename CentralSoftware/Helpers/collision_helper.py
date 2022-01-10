import sys
sys.path.append("..")

import Route.coordinate as co

class CollisionHelper:
    def lineLineIntersection(self, A: co.Coordinate, B: co.Coordinate, C: co.Coordinate, D: co.Coordinate) -> bool:
        """
        :param A: Current coordinate of boat
        :param B: Headed coordinate of boat
        :param C: Current coordinate of ais-ship
        :param D: Headed coordinate of ais-ship
        :return: bool -> Whether the two route lines of the boat and the ais-ship collide
        """
        return self.counterClockwiseOrder(A, C, D) != self.counterClockwiseOrder(B, C, D) and self.counterClockwiseOrder(A, B, C) != self.counterClockwiseOrder(A, B, D)

    @staticmethod
    def counterClockwiseOrder(A: co.Coordinate, B: co.Coordinate, C: co.Coordinate) -> bool:
        return (C.latitude - A.latitude) * (B.longitude - A.longitude) > (B.latitude - A.latitude) * (C.longitude - A.longitude)