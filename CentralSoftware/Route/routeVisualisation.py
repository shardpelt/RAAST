import os
import sys
import pygame
sys.path.append("..")
from central_data import CentralData
from Route.coordinate import Coordinate

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill([70, 125, 215])
pygame.display.set_caption("Route visualisator")
pygame.display.flip()

waypoints = [Coordinate(screen_height * 0.8, screen_width / 2 - 50)]
windAngle = 90

cd = CentralData()
print(cd.boat.coordinate)
cd.boat.coordinate.latitude = screen_height / 2
cd.boat.coordinate.latitude = screen_width / 2 + 50

pygame.draw.circle(screen, [255, 0, 0], [cd.boat.coordinate.latitude, cd.boat.coordinate.longitude], 20)
pygame.display.flip()


input("")
