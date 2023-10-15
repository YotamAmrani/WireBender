from pygame.locals import *

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GREY = (125, 125, 125)
GREY = (128, 128, 128)
LIGHT_GREY = (200, 200, 200)


# Serial
BAUD_RATE = 9600
PIXEL_TO_MM = 5

# line and spinner
LINE_WIDTH = 20
LINE_COLOR = GREY
SPINNER_DISTANCE = 100
SPINNER_SPEED = 1
LEFT_MAX_VALUE = 135
RIGHT_MIN_VALUE = -135

LINE_MAX_LENGTH = 150*PIXEL_TO_MM # 1000/5 = 250mm




# screen
# infoObject = pygame.display.Info()
# SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900
# print("screen width: ", infoObject.current_w)
# print("screen height: ", infoObject.current_h)
# SCREEN_WIDTH = infoObject.current_w
# SCREEN_HEIGHT = infoObject.current_h
SCREEN_COLOR = WHITE
fps = 60.0

# global variables
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

# Alarms
ALARM_SIZE = (400, 50)
ALARM_POSITION = (SCREEN_WIDTH//2 - 400/2, SCREEN_HEIGHT //2 - 50//2)

# ALARM EVENTS
ALARM_TIMER = 1
ROTATE_RIGHT_ALARM = USEREVENT + 1
ROTATE_LEFT_ALARM = USEREVENT + 2
SEGMENT_OUT_OF_BOUNDARY = USEREVENT + 3
SEGMENT_TOO_LONG = USEREVENT + 4




# buttons colors
buttonInactiveColour = GREY
buttonHoverColour = GREY
buttonPressedColour = LIGHT_GREY

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
SPINNER_IMAGE = "pictures/spinner_medium.png"
EXTRUDE_IDLE_IMAGE_PATH = "pictures/extrude_button_0.jpg"
EXTRUDE_HOVER_IMAGE_PATH = "pictures/extrude_button_1.png"
EXTRUDE_CLICK_IMAGE_PATH = "pictures/extrude_button_2.jpg"
REVERT_IDLE_IMAGE_PATH = "pictures/revert_button_0.jpg"
REVERT_HOVER_IMAGE_PATH = "pictures/revert_button_1.png"
REVERT_CLICK_IMAGE_PATH = "pictures/revert_button_2.jpg"
ROTATE_RIGHT_IDLE_IMAGE_PATH = "pictures/rotr_button_0.jpg"
ROTATE_RIGHT_HOVER_IMAGE_PATH = "pictures/rotr_button_1.png"
ROTATE_RIGHT_CLICK_IMAGE_PATH = "pictures/rotr_button_2.jpg"
ROTATE_LEFT_IDLE_IMAGE_PATH = "pictures/rotl_button_0.jpg"
ROTATE_LEFT_HOVER_IMAGE_PATH = "pictures/rotl_button_1.png"
ROTATE_LEFT_CLICK_IMAGE_PATH = "pictures/rotl_button_2.jpg"
ADD_SEGMENT_IDLE_IMAGE_PATH = "pictures/add_segment_button_0.jpg"
ADD_SEGMENT_HOVER_IMAGE_PATH = "pictures/add_segment_button_1.png"
ADD_SEGMENT_CLICK_IMAGE_PATH = "pictures/add_segment_button_2.jpg"
FINISH_IDLE_IMAGE_PATH = "pictures/finish_button_0.jpg"
FINISH_HOVER_IMAGE_PATH = "pictures/finish_button_1.png"
FINISH_CLICK_IMAGE_PATH = "pictures/finish_button_2.jpg"
TOO_LONG_ALARM_PATH = "pictures/too long.png"
LEFT_ALARM_PATH = "pictures/left.png"
RIGHT_ALARM_PATH = "pictures/right.png"
