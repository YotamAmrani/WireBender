import sys
import math
import pygame
from pygame.locals import *

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GREY = (125, 125, 125)
LIGHT_GREY = (200, 200, 200)

# screen
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_COLOR = WHITE
fps = 60.0

# line and spinner
LINE_WIDTH = 20
SPINNER_DISTANCE = 100
SPINNER_SPEED = 1
LEFT_MAX_VALUE = 120
RIGHT_MIN_VALUE = -120
spinner_image_path = "spinner_medium.png"

# global variables
line_length = SPINNER_DISTANCE
total_length = 0
angle = 0
points = []
polar_points = []
key_0_pressed = False
key_1_pressed = False
