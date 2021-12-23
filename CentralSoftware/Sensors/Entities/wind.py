import sys
sys.path.append("..")

class Wind:
	def __init__(self):
		self.relative = None  # Relative wind angle according to the boat
		self.toNorth = None   # Wind angle according to North through boats compass
		self.speed = None

	def hasData(self):
		return self.relative is not None