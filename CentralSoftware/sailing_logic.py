from Sensors.coordinate import Coordinate
from helper import Helper
import math as m

# Logic from framework other group
# //TODO: Check which parts are handy for us

class SailingLogic:
    def __init__(self):
        self.sailInControl = True

    def optimalAngleToWaypoint(self, currCoordinate: Coordinate, waypoint: Coordinate):
        xDelta = waypoint.longitude - currCoordinate.longitude
        yDelta = waypoint.latitude - currCoordinate.latitude

        radians = m.atan(yDelta / xDelta)
        return radians


    def compute_optimal_sailing_angle(self, sailboat_rotation: float, wind_direction: float) -> float:
        if self.sailInControl:

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

        else:
            pass
