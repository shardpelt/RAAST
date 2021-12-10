class Wind:
	def __init__(self):
		self.angle = None # Relative wind angle according to the boat
		self.speed = None

	def hasData(self):
		return self.angle is not None