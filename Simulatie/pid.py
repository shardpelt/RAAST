import simpylc as sp


def is_between_angles(n, a, b):
    if a < b:
        return a <= n <= b
    return a <= n or n <= b


def calculate_error(current_heading, desired_heading):
    phi = abs(current_heading - desired_heading) % 360
    distance = 360 - phi if phi > 180 else phi

    if is_between_angles(current_heading, (current_heading - 180) % 360, desired_heading):
        return distance
    else:
        return -distance


class Pid(sp.Module):
    def __init__(self):
        sp.Module.__init__(self)

        self.page("test")
        self.group("PID", True)
        self.errorIntegral = sp.Register(0)
        self.outputLimits = sp.Register()
        self.latestInput = sp.Register()
        self.desiredHeading = sp.Register()
        self.currentheading = sp.Register()
        self.dt = sp.Register()
        self.kp = sp.Register(0)
        self.ki = sp.Register(0)
        self.kd = sp.Register(0)
        self.test = sp.Register(2)

    def clamp(self, error, clampOn):
        if self.error < -clampOn:
            self.error = -clampOn
            return self.error
        if self.error > clampOn:
            self.error = clampOn
            return self.error

    def setDesiredHeading(self, incomingHeading):
        self.desiredHeading = incomingHeading

    def setDt(self, dt):
        self.dt = dt

    def setKp(self, kp):
        self.kp = kp

    def setKi(self, ki):
        self.ki = ki

    def setKd(self, kd):
        self.kd = kd

    def control(self, desiredHeading, dt):
        currentHeading = sp.world.sailboat.sailboat_rotation
        clampStatus = None
        integraterStatus = None

        desiredHeading = desiredHeading % 360
        currentHeading = currentHeading % 360

        # error = currentHeading - desiredHeading  # if - turn left, if + turn right
        self.error = calculate_error(currentHeading, desiredHeading)
        self.errorc = calculate_error(currentHeading, desiredHeading)
        self.clamp(self.error, 5)
        if self.error != self.errorc:
            clampStatus = True
        else:
            clampStatus = False

        outputP = self.calculateProportional(self.error)
        outputI = self.calculateIntergrational(dt, self.error)
        outputD = self.calculateDifferentional(currentHeading, dt, self.errorc)
        output = outputP + outputI + outputD

        if (self.error > 0 and output > 0) or (self.error < 0 and output < 0):
            integraterStatus = True
            # integrated still adding
        else:
            integraterStatus = False

        if clampStatus == True and integraterStatus == True:
            self.errorIntegral = 0

        if self.error < 0:
            # turn left
            sp.world.control.target_gimbal_rudder_angle.set(sp.world.sailboat.target_gimbal_rudder_angle - (0.1 * output * abs(self.error)))
            if self.error < self.error - self.test:
                sp.world.control.target_gimbal_rudder_angle.set(sp.world.sailboat.target_gimbal_rudder_angle)
        else:
            # turn right
            sp.world.control.target_gimbal_rudder_angle.set(sp.world.sailboat.target_gimbal_rudder_angle - (0.1 * output * abs(self.error)))
            if self.error > self.error + self.test:
                sp.world.control.target_gimbal_rudder_angle.set(sp.world.sailboat.target_gimbal_rudder_angle)

        if sp.world.control.target_gimbal_rudder_angle > 35:
            sp.world.control.target_gimbal_rudder_angle.set(35)

        if sp.world.control.target_gimbal_rudder_angle < -35:
            sp.world.control.target_gimbal_rudder_angle.set(-35)

    def calculateProportional(self, error):
        return self.kp * error

    def calculateIntergrational(self, dt, error):
        self.errorIntegral += self.ki * error * dt

        return self.errorIntegral

    def calculateDifferentional(self, currentInput, dt, error):
        if error < 0:
            return -self.kd * ((currentInput + error) / dt)
        else:
            return self.kd * ((currentInput - error) / dt)