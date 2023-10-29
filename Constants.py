from pygame.locals import *

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GREY = (125, 125, 125)
GREY = (128, 128, 128)
LIGHT_GREY = (200, 200, 200)
BUFFER_YELLOW = (241, 188, 26)
BUFFER_RED = (198, 32, 47)
SCREEN_COLOR = (226, 233, 241)
# Titles
FONT_PATH = "C:\Windows\Fonts\Assistant-Bold.ttf"

# Serial
BAUD_RATE = 9600
PIXEL_TO_MM = 5

# line and spinner
LINE_WIDTH = 20
LINE_COLOR = GREY
SPINNER_DISTANCE = 260
BUTTONS_PANEL_HEIGHT = 155
SPINNER_SPEED = 1
LEFT_MAX_VALUE = 135
RIGHT_MIN_VALUE = -135

LINE_MAX_LENGTH = 150 * PIXEL_TO_MM  # 1000/5 = 250mm

# Logging
LOGGING_FILE_PATH = "logging.log"

# screen
# infoObject = pygame.display.Info()
# SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900
# print("screen width: ", infoObject.current_w)
# print("screen height: ", infoObject.current_h)
# SCREEN_WIDTH = infoObject.current_w
# SCREEN_HEIGHT = infoObject.current_h
fps = 60.0

# global variables
key_0_pressed = False
key_1_pressed = False
key_2_pressed = False

# Alarms
ALARM_SIZE = (400, 50)
ALARM_POSITION = (SCREEN_WIDTH // 2 - 400 / 2, SCREEN_HEIGHT // 2 - 50 // 2)

# ALARM EVENTS
ALARM_TIMER = 1
ROTATE_RIGHT_ALARM = USEREVENT + 1
ROTATE_LEFT_ALARM = USEREVENT + 2
SEGMENT_OUT_OF_BOUNDARY_ALARM = USEREVENT + 3
SEGMENT_TOO_LONG_ALARM = USEREVENT + 4

# buttons colors
buttonInactiveColour = GREY
buttonHoverColour = GREY
buttonPressedColour = LIGHT_GREY

# buttons sizes
# EXTRUDE_BUTTON_SIZE = (175, 50)
# REVERT_BUTTON_SIZE = (175, 50)
# ROTATE_RIGHT_BUTTON_SIZE = (175, 50)
# ROTATE_LEFT_BUTTON_SIZE = (175, 50)
# ADD_SEGMENT_BUTTON_SIZE = (175, 50)
# FINISH_BUTTON_SIZE = (175, 50)
CONVERSION_FACTOR = 5

EXTRUDE_BUTTON_SIZE = (100, 100)
REVERT_BUTTON_SIZE = (100, 100)
ROTATE_RIGHT_BUTTON_SIZE = (100, 100)
ROTATE_LEFT_BUTTON_SIZE = (100, 100)
ADD_SEGMENT_BUTTON_SIZE = (100, 100)
FINISH_BUTTON_SIZE = (175, 50)

# Buttons positions
SEND_BUTTON_POSITION = (480, SCREEN_HEIGHT - 127)
REVERT_BUTTON_POSITION = (SEND_BUTTON_POSITION[0] + 134 + 34, SCREEN_HEIGHT - 127)
ROTATE_LEFT_BUTTON_POSITION = (REVERT_BUTTON_POSITION[0] + 134 + 34, SCREEN_HEIGHT - 127)
ROTATE_RIGHT_BUTTON_POSITION = (ROTATE_LEFT_BUTTON_POSITION[0] + 134 + 34, SCREEN_HEIGHT - 127)
EXTRUDE_BUTTON_POSITION = (ROTATE_RIGHT_BUTTON_POSITION[0] + 134 + 34, SCREEN_HEIGHT - 127)
INFO_BUTTON_POSITION = (EXTRUDE_BUTTON_POSITION[0] + 134 + 34, SCREEN_HEIGHT - 127)
CLOSE_INFO_BUTTON_POSITION = (SCREEN_WIDTH - 65, -65)

# load images
# SCREEN_IMAGE = "pictures/back_ground_screen.jpg"
SCREEN_IMAGE = "מסכים מוצג כיפוף/מסכים למיצג כיפוף_החופש ליצור30.jpg"
INFO_SCREEN_IMAGE_PATH = "pictures/info_screen.jpg"
SPINNER_IMAGE = "pictures/spinner_medium.png"
# EXTRUDE_HOVER_IMAGE_PATH = "pictures/extrude_button_1.png"
EXTRUDE_IDLE_IMAGE_PATH = "pictures/press_wire_idle.jpg"
EXTRUDE_CLICK_IMAGE_PATH = "pictures/press_wire_click.jpg"
# REVERT_HOVER_IMAGE_PATH = "pictures/revert_button_1.png"
REVERT_IDLE_IMAGE_PATH = "pictures/revert_idle.jpg"
REVERT_CLICK_IMAGE_PATH = "pictures/revert_click.jpg"
# ROTATE_RIGHT_HOVER_IMAGE_PATH = "pictures/rotr_button_1.png"
ROTATE_RIGHT_IDLE_IMAGE_PATH = "pictures/bend_right_idle.jpg"
ROTATE_RIGHT_CLICK_IMAGE_PATH = "pictures/bend_right_click.jpg"
# ROTATE_LEFT_HOVER_IMAGE_PATH = "pictures/rotl_button_1.png"
ROTATE_LEFT_IDLE_IMAGE_PATH = "pictures/bend_left_idle.jpg"
ROTATE_LEFT_CLICK_IMAGE_PATH = "pictures/bend_left_click.jpg"

SEND_IDLE_IMAGE_PATH = "pictures/send_idle.jpg"
SEND_CLICK_IMAGE_PATH = "pictures/send_click.jpg"
INFO_IDLE_IMAGE_PATH = "pictures/info_idle.jpg"
INFO_CLICK_IMAGE_PATH = "pictures/info_click.jpg"
CLOSE_INFO_IDLE_IMAGE_PATH = "pictures/close_info_idle.jpg"
CLOSE_INFO_CLICK_IMAGE_PATH = "pictures/close_info_click.jpg"

CAPACITY_IMAGE_PATH = "pictures/Loading.png"

PLEASE_WAIT_SCREEN_0 = "pictures/please_wait_1.jpg"
PLEASE_WAIT_SCREEN_1 = "pictures/please_wait_2.jpg"

LEFT_ALARM_PATH = "pictures/out_of_boundary_alarm.jpg"
RIGHT_ALARM_PATH = "pictures/out_of_boundary_alarm.jpg"
SEGMENT_OUT_OF_BOUNDARY_PATH = "pictures/out_of_boundary_alarm.jpg"
TOO_LONG_ALARM_PATH = "pictures/max_length_alarm.jpg"
