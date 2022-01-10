# TODO: Refactor and document
# Wat is de hoek van de wind ten opzichten van de x-as, tegen de klok is positief
# Wat is de gewenste koershoek
# Wat is het hoekverschil tussen de gewenste koershoek en de windhoek
# Wat is de zeilstand (helft van stap 3)
# Wat is de component van de wind die effect heeft op het zeil
# loodrecht = totale windkracht * sin (alpha)
# voorwaards = loodrecht * cos (beta)
# beta = 90 - hoek van het zeil met de boot

import simpylc as sp

def is_sailing_against_wind(min_threshold,
                            max_threshold,
                            local_sail_angle,
                            global_sail_angle,
                            wind_direction):
    if local_sail_angle < 0 and \
            global_sail_angle < min_threshold and not \
            is_between_angles(global_sail_angle, min_threshold, wind_direction):
        return True

    if local_sail_angle < 0 and \
            global_sail_angle > min_threshold and \
            is_between_angles(min_threshold, global_sail_angle, wind_direction):
        return True

    if local_sail_angle > 0 and \
            global_sail_angle < max_threshold and \
            is_between_angles(global_sail_angle, max_threshold, wind_direction):
        return True

    if local_sail_angle > 0 and \
            global_sail_angle > max_threshold and not \
            is_between_angles(max_threshold, global_sail_angle, wind_direction):
        return True

    return False


def is_between_angles(n, alpha, beta):
    if alpha < beta:
        return alpha <= n <= beta
    return alpha <= n or n <= beta


def distance_between_angles(alpha, beta):
    phi = abs(beta - alpha) % 360
    distance = (180 - phi) % 360 if phi > 90 else phi
    return distance

def angle_to_waypoint(delta_x, delta_y):
    return sp.tan(delta_x / delta_y) * 1000


def distance_between_waypoint(delta_x, delta_y):
    return sp.sqrt(delta_x * delta_x + delta_y * delta_y)


class Sailboat (sp.Module):
    def __init__(self):
        sp.Module.__init__(self)

        self.page('sailboat')

        self.group('Simulation boat', True)
        self.position_x = sp.Register() # x waarde stijgt in hoogte de + in, dus -> latitude
        self.position_y = sp.Register(3) # y waarde stijg naar links de + in, dus -> longitude
        self.sailboat_rotation = sp.Register(90)
        self.gimbal_rudder_angle = sp.Register(0.1)
        self.local_sail_angle = sp.Register(0.1)

        # Private variables which are updated from the transat.
        self._rudderAngle = 0.0
        self._sailAngle = 0.0

        self.group('Transat boat')
        self.latitude = sp.Register()
        self.longitude = sp.Register()
        self.compassAngle = sp.Register()
        self.wantedAngle = sp.Register()
        self.optimalAngle = sp.Register()
        self.toTheWind = sp.Register()
        self.cantChooseSide = sp.Register()

        self.group('Overig')
        self.position_z = sp.Register()
        self.mass = sp.Register(20)
        self.drag = sp.Register()
        self.acceleration = sp.Register()
        self.forward_velocity = sp.Register()
        self.horizontal_velocity = sp.Register()
        self.vertical_velocity = sp.Register()
        self.target_sail_angle = sp.Register()
        self.global_sail_angle = sp.Register()
        self.sail_alpha = sp.Register()
        self.perpendicular_sail_force = sp.Register()
        self.forward_sail_force = sp.Register()
        self.target_gimbal_rudder_angle = sp.Register(0)
        self.rotation_speed = sp.Register()
        self.passed_first_waypoint = sp.Register(False)


    def getCompassAngle(self):
        boatAngle = 360 - ((self.sailboat_rotation - 90) % 360)
        return 0 if boatAngle == 360 else boatAngle

    def sweep(self):
        # Update rudder and sail and waypoints to values received from transat boat.
        self.local_sail_angle.set(self._sailAngle)
        self.gimbal_rudder_angle.set(self._rudderAngle)
        #sp.world.waypoint._waywaypointypointy = self._waypoints

        # Update other used variables
        self.global_sail_angle.set((self.sailboat_rotation + self.local_sail_angle + 180) % 360)
        self.compassAngle.set(round(self.getCompassAngle(), 2))

        # Calculate forward force in N based on the angle between the sail and the wind
        self.sail_alpha.set(distance_between_angles(sp.world.wind.wind_direction, self.global_sail_angle))
        self.perpendicular_sail_force.set(sp.world.wind.wind_scalar * sp.sin(self.sail_alpha))
        self.forward_sail_force.set(self.perpendicular_sail_force * sp.sin(self.local_sail_angle))
        self.forward_sail_force.set(sp.abs(self.forward_sail_force))

        # Sailing against wind
        min_threshold = (self.global_sail_angle - 180) % 360
        max_threshold = (self.global_sail_angle + 180) % 360
        self.forward_sail_force.set(0,
                                    is_sailing_against_wind(min_threshold,
                                                            max_threshold,
                                                            self.local_sail_angle,
                                                            self.global_sail_angle,
                                                            sp.world.wind.wind_direction))

        # Newton's second law
        self.drag.set(self.forward_velocity * 0.05)
        self.acceleration.set(self.forward_sail_force / self.mass - self.drag)
        self.forward_velocity.set(sp.limit(self.forward_velocity + self.acceleration * sp.world.period, 8))

        # Splitting forward velocity vector into vertical and horizontal components
        self.vertical_velocity.set(sp.cos(self.sailboat_rotation) * self.forward_velocity)
        self.horizontal_velocity.set(sp.sin(self.sailboat_rotation) * self.forward_velocity)

        self.position_x.set(self.position_x + self.horizontal_velocity * 0.001)
        self.position_y.set(self.position_y - self.vertical_velocity * 0.001)
        self.rotation_speed.set(0.001 * self.gimbal_rudder_angle * self.forward_velocity)
        self.sailboat_rotation.set((self.sailboat_rotation - self.rotation_speed) % 360)

