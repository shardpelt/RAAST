from wind import *
from gyroscope import *
from coordinates import Coordinates

# CentralData
class CentralData:

	def __init__(self):
		self.gyroscope = Gyroscope(),
		self.wind = Wind(),
		self.coordinates = Coordinates(),
		self.rudderAngle = None,
		self.sailAngle = None,
		self.compass = None,
		self.movementOnSonar = False,
		self.powerStateAis = "Off"


	def set_sonarMovement(self, movement: bool):
		self.movementOnSonar = movement
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


	def set_rudderAngle(self, angle: int):
		self.rudderAngle = angle % 360


	def set_sailAngle(self, angle: int):
		self.rudderAngle = angle % 360


	def set_compassAngle(self, angle: int):
		self.compass = angle % 360


	def set_gpsCoordinates(self, latitude: float, longitude: float):
		self.coordinates.latitude = latitude
		self.coordinates.longitude = longitude


	def set_powerStateAis(self, powerState: str):
		self.powerStateAis = powerState
