import sys
import math
import pygame
from pygame.locals import *
import serial

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GREY = (125, 125, 125)
GREY = (128, 128, 128)
LIGHT_GREY = (200, 200, 200)

# line and spinner
LINE_WIDTH = 20
LINE_COLOR = GREY
SPINNER_DISTANCE = 100
SPINNER_SPEED = 1
LEFT_MAX_VALUE = 135
RIGHT_MIN_VALUE = -135

# Serial
BAUD_RATE = 9600
PIXEL_TO_MM = 5
ser = serial.Serial('COM3', baudrate=BAUD_RATE, timeout=1)


# screen
pygame.init()
infoObject = pygame.display.Info()
# SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
print("screen width: ", infoObject.current_w)
print("screen height: ", infoObject.current_h)
SCREEN_WIDTH = infoObject.current_w
SCREEN_HEIGHT = infoObject.current_h
SCREEN_COLOR = WHITE
fps = 60.0

# global variables
line_length = SPINNER_DISTANCE
total_length = 0
angle = 0
points = []
polar_points = []
key_0_pressed = False
key_1_pressed = False
key_2_pressed = False


# buttons sizes
EXTRUDE_BUTTON_SIZE = (175, 50)
REVERT_BUTTON_SIZE = (175, 50)
ROTATE_RIGHT_BUTTON_SIZE = (175, 50)
ROTATE_LEFT_BUTTON_SIZE = (175, 50)
ADD_SEGMENT_BUTTON_SIZE = (175, 50)
FINISH_BUTTON_SIZE = (175, 50)

# buttons colors
buttonInactiveColour=GREY
buttonHoverColour=GREY
buttonPressedColour=LIGHT_GREY

# buttons positions make sure they are in the same row and not overlapping
EXTRUDE_BUTTON_POSITION = (SCREEN_WIDTH - EXTRUDE_BUTTON_SIZE[0] - 10, 10)
ROTATE_RIGHT_BUTTON_POSITION = (EXTRUDE_BUTTON_POSITION[0] - ROTATE_RIGHT_BUTTON_SIZE[0] - 10, 10)
ROTATE_LEFT_BUTTON_POSITION = (ROTATE_RIGHT_BUTTON_POSITION[0] - ROTATE_LEFT_BUTTON_SIZE[0] - 10, 10)
ADD_SEGMENT_BUTTON_POSITION = (ROTATE_LEFT_BUTTON_POSITION[0] - ADD_SEGMENT_BUTTON_SIZE[0] - 10, 10)
# REVERT_BUTTON_POSITION = (ADD_SEGMENT_BUTTON_POSITION[0] - REVERT_BUTTON_SIZE[0] - 10, 10)
# FINISH_BUTTON_POSITION = (REVERT_BUTTON_POSITION[0] - FINISH_BUTTON_SIZE[0] - 10, 10)
FINISH_BUTTON_POSITION = (10, 10)
REVERT_BUTTON_POSITION = (FINISH_BUTTON_POSITION[0] + FINISH_BUTTON_SIZE[0] + 10, 10)

# load images
spinner = pygame.image.load("pictures/spinner_medium.png")
pic_extrude_button = pygame.image.load("pictures/extrude_button_0.jpg")
pic_extrude_button_hover = pygame.image.load("pictures/extrude_button_1.png")
pic_extrude_button_pressed = pygame.image.load("pictures/extrude_button_2.jpg")
pic_revert_button = pygame.image.load("pictures/revert_button_0.jpg")
pic_revert_button_hover = pygame.image.load("pictures/revert_button_1.png")
pic_revert_button_pressed = pygame.image.load("pictures/revert_button_2.jpg")
pic_rotate_right_button = pygame.image.load("pictures/rotr_button_0.jpg")
pic_rotate_right_button_hover = pygame.image.load("pictures/rotr_button_1.png")
pic_rotate_right_button_pressed = pygame.image.load("pictures/rotr_button_2.jpg")
pic_rotate_left_button = pygame.image.load("pictures/rotl_button_0.jpg")
pic_rotate_left_button_hover = pygame.image.load("pictures/rotl_button_1.png")
pic_rotate_left_button_pressed = pygame.image.load("pictures/rotl_button_2.jpg")
pic_add_segment_button = pygame.image.load("pictures/add_segment_button_0.jpg")
pic_add_segment_button_hover = pygame.image.load("pictures/add_segment_button_1.png")
pic_add_segment_button_pressed = pygame.image.load("pictures/add_segment_button_2.jpg")
pic_finish_button = pygame.image.load("pictures/finish_button_0.jpg")
pic_finish_button_hover = pygame.image.load("pictures/finish_button_1.png")
pic_finish_button_pressed = pygame.image.load("pictures/finish_button_2.jpg")

# resize images
pic_extrude_button = pygame.transform.scale(pic_extrude_button, EXTRUDE_BUTTON_SIZE)
pic_extrude_button_hover = pygame.transform.scale(pic_extrude_button_hover, EXTRUDE_BUTTON_SIZE)
pic_extrude_button_pressed = pygame.transform.scale(pic_extrude_button_pressed, EXTRUDE_BUTTON_SIZE)
pic_revert_button = pygame.transform.scale(pic_revert_button, REVERT_BUTTON_SIZE)
pic_revert_button_hover = pygame.transform.scale(pic_revert_button_hover, REVERT_BUTTON_SIZE)
pic_revert_button_pressed = pygame.transform.scale(pic_revert_button_pressed, REVERT_BUTTON_SIZE)
pic_rotate_right_button = pygame.transform.scale(pic_rotate_right_button, ROTATE_RIGHT_BUTTON_SIZE)
pic_rotate_right_button_hover = pygame.transform.scale(pic_rotate_right_button_hover, ROTATE_RIGHT_BUTTON_SIZE)
pic_rotate_right_button_pressed = pygame.transform.scale(pic_rotate_right_button_pressed, ROTATE_RIGHT_BUTTON_SIZE)
pic_rotate_left_button = pygame.transform.scale(pic_rotate_left_button, ROTATE_LEFT_BUTTON_SIZE)
pic_rotate_left_button_hover = pygame.transform.scale(pic_rotate_left_button_hover, ROTATE_LEFT_BUTTON_SIZE)
pic_rotate_left_button_pressed = pygame.transform.scale(pic_rotate_left_button_pressed, ROTATE_LEFT_BUTTON_SIZE)
pic_add_segment_button = pygame.transform.scale(pic_add_segment_button, ADD_SEGMENT_BUTTON_SIZE)
pic_add_segment_button_hover = pygame.transform.scale(pic_add_segment_button_hover, ADD_SEGMENT_BUTTON_SIZE)
pic_add_segment_button_pressed = pygame.transform.scale(pic_add_segment_button_pressed, ADD_SEGMENT_BUTTON_SIZE)
pic_finish_button = pygame.transform.scale(pic_finish_button, FINISH_BUTTON_SIZE)
pic_finish_button_hover = pygame.transform.scale(pic_finish_button_hover, FINISH_BUTTON_SIZE)
pic_finish_button_pressed = pygame.transform.scale(pic_finish_button_pressed, FINISH_BUTTON_SIZE)

