# TODO: Refactor and document
# Wat is de hoek van de wind ten opzichten van de x-as, tegen de klok is positief
# Wat is de gewenste koershoek
# Wat is het hoekverschil tussen de gewenste koershoek en de windhoek
# Wat is de zeilstand (helft van stap 3)
# Wat is de component van de wind die effect heeft op het zeil
# loodrecht = totale windkracht * sin (alpha)
# voorwaards = loodrecht * cos (beta)
# beta = 90 - hoek van het zeil met de boot

from pid import *
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


def optimal_sailing_angle(sailboat_rotation,
                          wind_direction):
    distance = distance_between_angles((sailboat_rotation + 180) % 360, wind_direction)

    if distance > 180:
        distance = (360 - distance) % 360

    # If wind blows from starboard
    if is_between_angles((sailboat_rotation - 180) % 360,
                         sailboat_rotation,
                         sp.world.wind.wind_direction):
        distance = -distance

    return distance / 2


def angle_to_waypoint(delta_x, delta_y):
    return sp.tan(delta_x / delta_y) * 1000


def distance_between_waypoint(delta_x, delta_y):
    return sp.sqrt(delta_x * delta_x + delta_y * delta_y)


class Sailboat (sp.Module):
    def __init__(self):
        sp.Module.__init__(self)

        self.page('sailboat')

        self.group('transform', True)
        self.position_x = sp.Register()
        self.position_y = sp.Register()
        self.position_z = sp.Register()
        self.sailboat_rotation = sp.Register()

        self.group('body')
        self.mass = sp.Register(20)

        self._waypoints = []

        self.group('velocity')
        self.drag = sp.Register()
        self.acceleration = sp.Register()
        self.forward_velocity = sp.Register()
        self.horizontal_velocity = sp.Register()
        self.vertical_velocity = sp.Register()

        self.group('sail')
        self.target_sail_angle = sp.Register()
        self.local_sail_angle = sp.Register()
        self.global_sail_angle = sp.Register()
        self.sail_alpha = sp.Register()
        self.perpendicular_sail_force = sp.Register()
        self.forward_sail_force = sp.Register()
        
        self.group('rudder')
        self.target_gimbal_rudder_angle = sp.Register(0)
        self.gimbal_rudder_angle = sp.Register(0)
        self.rotation_speed = sp.Register()
        self.rudder_pid = Pid()
        self.passed_first_waypoint = sp.Register(False)

    def input(self):
        self.part('target sail angle')
        self.target_sail_angle.set(sp.world.control.target_sail_angle)
        
        self.part('gimbal rudder angle')
        self.target_gimbal_rudder_angle.set(sp.world.control.target_gimbal_rudder_angle)

    def sweep(self):
        if distance_between_waypoint(sp.abs(self.position_x - sp.world.waypoint._waywaypointypointy[0][0]),
                                      sp.abs(self.position_y - sp.world.waypoint._waywaypointypointy[0][1])) < 1:
            self.passed_first_waypoint.set(True)

        if not self.passed_first_waypoint:
            alpha = angle_to_waypoint(sp.abs(self.position_x - sp.world.waypoint._waywaypointypointy[0][0]),
                                      sp.abs(self.position_y - sp.world.waypoint._waywaypointypointy[0][1]))

        else:
            alpha = angle_to_waypoint(sp.abs(self.position_x - sp.world.waypoint._waywaypointypointy[1][0]),
                                      sp.abs(self.position_y - sp.world.waypoint._waywaypointypointy[1][1]))
            sp.world.waypoint._waywaypointypointy[0] = [5,-5,0]

        self.target_sail_angle.set(optimal_sailing_angle(self.sailboat_rotation,
                                                         sp.world.wind.wind_direction), 90)

        self.local_sail_angle.set(self.local_sail_angle - 1, self.local_sail_angle > self.target_sail_angle)
        self.local_sail_angle.set(self.local_sail_angle + 1, self.local_sail_angle < self.target_sail_angle)
        self.global_sail_angle.set((self.sailboat_rotation + self.local_sail_angle + 180) % 360)

        self.gimbal_rudder_angle.set(self.gimbal_rudder_angle - 1,
                                     self.gimbal_rudder_angle > self.target_gimbal_rudder_angle)
        self.gimbal_rudder_angle.set(self.gimbal_rudder_angle + 1,
                                     self.gimbal_rudder_angle < self.target_gimbal_rudder_angle)

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

        self.rudder_pid.control(alpha, sp.world.period)
        self.rudder_pid.setKp(0.5)
        self.rudder_pid.setKi(0.2)
        self.rudder_pid.setKd(0.0005)
