from simpylc import *

normalFloorColor = (0, 0, 1)
collisionFloorColor = (1, 0, 0.3)
nrOfObstacles = 64


class Floor(Beam):
    side = 64
    spacing = 0.6
    halfSteps = round(0.5 * side / spacing)

    class Stripe(Beam):
        def __init__(self, **arguments):
            super().__init__(size=(0.01, Floor.side, 0.01), **arguments)

    def __init__(self, **arguments):
        super().__init__(size=(self.side, self.side, 0.001), color=normalFloorColor)
        self.xStripes = [self.Stripe(center=(0, nr * self.spacing, 0, 0), angle=90, color=(1, 1, 1)) for nr in
                         range(-self.halfSteps, self.halfSteps)]
        self.yStripes = [self.Stripe(center=(nr * self.spacing, 0, 0), color=(0, 0, 0)) for nr in
                         range(-self.halfSteps, self.halfSteps)]

    def __call__(self):
        return super().__call__(color=collisionFloorColor if self.scene.collided else normalFloorColor, parts=lambda:
        sum(xStripe() for xStripe in self.xStripes) +
        sum(yStripe() for yStripe in self.yStripes))


class Visualisation (Scene):
    def __init__(self):
        Scene.__init__(self)

        self.camera = Camera()
        self.floor = Floor(scene=self)

        # Waypoint
        waypoint_color = (1, 0, 0)
        self.waypoint = Beam(size=(0.5, 0.5, 0.5), center=(0, 0, 0), color=waypoint_color)
        
        # Obstacle
        obstacle_color = (1, 0.9, 0.4)
        self.obstacle = Beam(size=(0.5, 0.5, 0.5), center=(0, 0, 0), color=obstacle_color)

        # Hull
        hull_color = (1, 1, 1)
        self.hull = Beam(size=(0.4, 1, 0.15), center=(0, 0, 0), color=hull_color)
        self.nose = Beam(size=(0.275, 0.275, 0.15), center=(0, -0.5, 0), angle=45, color=hull_color)
        self.rear = Cylinder(size=(0.4, 0.4, 0.15), center=(0, 0.5, 0), color=hull_color)
        
        # Rudder
        rudder_color = (1, 1, 1)
        self.rudder = Beam(size=(0.05, 0.4, 1.5), center=(0, 0, -0.77), color=rudder_color)
        self.gimbal_rudder = Ellipsoid(size=3 * (0.05,), center=(0, 0.7, -0.10), pivot=(0, 0, 1), color=rudder_color)

        # Sail
        mast_color = (1, 1, 1)
        sail_color = (1, 0, 0)
        self.mast = Cylinder(size=(0.05, 0.05, 1), center=(0, 0, 0.5), color=mast_color)
        self.gimbal = Ellipsoid(size=3 * (0.05,), center=(0, 0, -0.25), pivot=(0, 0, 1), color=mast_color)
        self.boom = Beam(size=(0.05, 0.5, 0.05), center=(0, 0.25, 0), color=mast_color)
        self.sail = Beam(size=(0.025, 0.4, 0.7), center=(0, 0, 0.4), color=sail_color)

        # Wind vane
        wind_vane_color = (0, 1, 0)
        self.wind_vane = Beam(size=(0.05, 0.5, 0.05), center=(0, 0, 1.25), color=wind_vane_color)
        self.wind_vane_pointer = Cone(size=(0.15, 0.15, 0.15), center=(0, 0.25, 0), axis=(1, 0, 0), angle=-90, color=wind_vane_color)

    def display(self):
        sailboat_position = tEva((world.sailboat.position_x,  world.sailboat.position_y, world.sailboat.position_z + 0.5))

        self.camera(
            position=tEva((world.sailboat.position_x, world.sailboat.position_y, world.sailboat.position_z + 10)),
            focus=tEva((world.sailboat.position_x + 0.00001,  world.sailboat.position_y, world.sailboat.position_z))
        )

        self.floor()

        #display all waypoints in the waypoint list
        count=0
        for way in world.waypoint._waywaypointypointy:
            world.waypoint.setWay(count)
            self.waypoint(
                    position=tEva((world.waypoint.waypointX, world.waypoint.waypointY, world.waypoint.waypointZ))
                    )
            count = count+1

        #display all obstacles  in the obstacle list
        count=0
        for obst in world.obstacle._obstaclesList:
            world.obstacle.setObstacle(count)
            self.obstacle(
                    position=tEva((world.obstacle.obstacleX, world.obstacle.obstacleY, world.obstacle.obstacleZ))
                    )
            count = count+1
        
        self.hull(
            position=sailboat_position,
            rotation=world.sailboat.sailboat_rotation,
            parts=lambda:
                self.nose() +
                self.rear() +
                self.mast(
                    parts=lambda:
                        self.gimbal(
                            rotation=world.sailboat.local_sail_angle,
                            parts=lambda:
                                self.boom(
                                    parts=lambda:
                                        self.sail()
                                )
                        )
                ) +
                self.gimbal_rudder(
                    rotation=world.sailboat.gimbal_rudder_angle,
                    parts=lambda:
                        self.rudder()
                )
        )

        self.wind_vane(
            position=sailboat_position,
            rotation=world.wind.wind_direction,
            parts=lambda:
                self.wind_vane_pointer()
        )
