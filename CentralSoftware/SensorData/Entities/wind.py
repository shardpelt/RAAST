class Wind:
	# TODO: Define whether this wind angle is relative to north or to axis of boat
	def __init__(self):
		self.angle = None
		self.speed = None

	def hasData(self):
		return self.angle is not None