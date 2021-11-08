class Wind:
	# TODO: Define whether this wind angle is relative to north or to axis of boat
	def __init__(self):
		self.angle = None
		self.speed = None

	def set_angle(self, value):
		self.angle = value

	def set_speed(self, value):
		self.speed = value
