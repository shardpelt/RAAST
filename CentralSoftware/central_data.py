from wind import *
from gyroscope import *
from coordinates import *

# CentralData
class CentralData:

	def __init__(self):
		self.sonarDetection = False,
		self.gyroscope = Gyroscope(),
		self.wind = Wind(),
		self.coordinates = Coordinates(),
		self.rudderPos = None,
		self.sailPos = None,
		self.compass = None,
		self.powerAis = False


	def set_sonarDetection(self, value):
		pass
		# TODO: - Krijgen we een boolean of zit hier metadata zoals afstand en hoek bij?
		#		- Krijgen we data bij detectie of constant?


	def set_gyroscope(self, value):
		pass
		# TODO: - Welke data krijgen we van de gyroscoop sensor?
		#		- Krijgen we data bij omslag of constant?


	def set_wind(self, speed, direction):
		self.wind.set_speed(speed)
		self.wind.set_direction(direction)
		# TODO: - Vanuit welke hoek krijgen we de direction?


	# value -> degrees
	def set_rudderPos(self, value):
		self.rudderPos = value


	# value -> degrees
	def set_sailPos(self, value):
		self.rudderPos = value


	def set_compass(self, value):
		self.compass = value


	def set_gps(self):
		pass
		# TODO: - Welke format krijgen we GPS binnen?


	def set_ais(self, value):
		self.powerAis = value
