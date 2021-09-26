from coordinate import Coordinate
from Helpers.helperFromFramework import Helper
import math as m

class SailingLogic:

    @staticmethod
    def optimalAngleToWaypoint(currCoordinate: Coordinate, waypoint: Coordinate):
        """
            Calculates the angle to the next waypoint which is, without any other inputs like wind etc, the most optimal.
            :arg currCoordinate: The current coordinate of the boat
            :arg waypoint: The waypoint which the boat is headed
            :returns: The most optimal angle in radians to next waypoint, without taking into account the wind etc.
        """
        xDelta = waypoint.longitude - currCoordinate.longitude
        yDelta = waypoint.latitude - currCoordinate.latitude

        radians = m.atan(yDelta / xDelta)
        return radians


    @staticmethod
    def optimalSailingAngle(optimalAngle: float, windAngle: float):
        # TODO: Calculate optimal line and look at which zone the wind is comming
        
        pass





    ## Method from framework --
    def compute_optimal_sailing_angle(self, sailboat_rotation: float, wind_direction: float) -> float:

        # If wind is coming straight from behind
        if Helper.is_between_angles((sailboat_rotation + 180) % 360,
                                    (wind_direction - 45) % 360,
                                    (wind_direction + 45) % 360):
            return Helper.distance_between_angles((sailboat_rotation + 90) % 360, wind_direction)
        else:
            distance = Helper.distance_between_angles((sailboat_rotation + 180) % 360, wind_direction)

            if distance > 180:
                distance = (360 - distance) % 360

            # If wind blows from starboard
            if Helper.is_between_angles((sailboat_rotation - 180) % 360,
                                        sailboat_rotation,
                                        wind_direction):
                distance = -distance

            return distance / 2

