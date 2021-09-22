from wind import *
from gyroscope import *
from coordinate import *
from route import *

class CentralData:

	def __init__(self):
		self.rudderAngle = None,
		self.sailAngle = None,
		self.wind = Wind(),
		self.route = Route(		# TODO: Start en finish coördinaten moeten via een verbinding aanpasbaar zijn
			(Coordinate(48.0, -47.0), Coordinate(45.5, -47.0)),	# Coördinaten startlijn tussen Line-0 en Line-1
			(Coordinate(55.0, -16.0), Coordinate(51.0, -16.0))  # Coördinaten finishlijn tussen Line-0 en Line-1
		),
		self.gyroscope = Gyroscope(),
		self.currentCoordinate = Coordinate(),
		self.compass = None,
		self.movementOnSonar = False,
		self.powerStateAis = "Off"


	def set_movementOnSonar(self, movement: bool):
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


	def set_currentCoordinate(self, latitude: float, longitude: float):
		self.currentCoordinate.latitude = latitude
		self.currentCoordinate.longitude = longitude


	def set_powerStateAis(self, powerState: str):
		self.powerStateAis = powerState
