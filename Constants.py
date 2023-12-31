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
BAUD_RATE = 115200
PIXEL_TO_MM = 5
PIXEL_PER_PRESS = 1
LAST_SEGMENT_COMMAND = -1
CUT_COMMAND = -2

# line and spinner
LINE_WIDTH = 15
LINE_COLOR = GREY
SPINNER_DISTANCE = 260
BUTTONS_PANEL_HEIGHT = 186
SPINNER_SPEED = 1
LEFT_MAX_VALUE = 135
RIGHT_MIN_VALUE = -135

MINIMAL_SEGMENT_LENGTH = 40

LINE_MAX_LENGTH = 150 * PIXEL_TO_MM  # 1000/5 = 250mm


# screen
# infoObject = pygame.display.Info()
# SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
# SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
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
CONVERSION_FACTOR = 0.24


EXTRUDE_BUTTON_SIZE = (100, 100)
REVERT_BUTTON_SIZE = (100, 100)
ROTATE_RIGHT_BUTTON_SIZE = (100, 100)
ROTATE_LEFT_BUTTON_SIZE = (100, 100)
ADD_SEGMENT_BUTTON_SIZE = (100, 100)
FINISH_BUTTON_SIZE = (175, 50)

# Buttons positions
button_w = 161
button_top = 142
button_margin = 41
SEND_BUTTON_POSITION = (465, SCREEN_HEIGHT - button_top)
REVERT_BUTTON_POSITION = (700, SCREEN_HEIGHT - button_top)
ROTATE_LEFT_BUTTON_POSITION = (900, SCREEN_HEIGHT - button_top)
ROTATE_RIGHT_BUTTON_POSITION = (1100, SCREEN_HEIGHT - button_top)
CLEAR_BUTTON_POSITION = (1300, SCREEN_HEIGHT - button_top)
EXTRUDE_BUTTON_POSITION = (1500, SCREEN_HEIGHT - button_top)
INFO_BUTTON_POSITION = (1735, SCREEN_HEIGHT - button_top)

CLOSE_INFO_BUTTON_POSITION = (SCREEN_WIDTH - 66, -30)
NEXT_BUTTON_POSITION = (80,253)

# load images
SCREEN_IMAGE = "pictures/BG.jpg"
INFO_SCREEN_0_IMAGE_PATH = "pictures/info_modal_0.jpg"
INFO_SCREEN_1_IMAGE_PATH = "pictures/info_modal_1.jpg"

SPINNER_IMAGE = "pictures/spinner_medium.png"
EXTRUDE_IDLE_IMAGE_PATH = "pictures/press_wire_idle.jpg"
EXTRUDE_CLICK_IMAGE_PATH = "pictures/press_wire_click.jpg"
REVERT_IDLE_IMAGE_PATH = "pictures/revert_idle.jpg"
REVERT_CLICK_IMAGE_PATH = "pictures/revert_click.jpg"
ROTATE_RIGHT_IDLE_IMAGE_PATH = "pictures/bend_right_idle.jpg"
ROTATE_RIGHT_CLICK_IMAGE_PATH = "pictures/bend_right_click.jpg"
ROTATE_LEFT_IDLE_IMAGE_PATH = "pictures/bend_left_idle.jpg"
ROTATE_LEFT_CLICK_IMAGE_PATH = "pictures/bend_left_click.jpg"

SEND_IDLE_IMAGE_PATH = "pictures/send_idle.jpg"
SEND_CLICK_IMAGE_PATH = "pictures/send_click.jpg"
INFO_IDLE_IMAGE_PATH = "pictures/info_idle.jpg"
INFO_CLICK_IMAGE_PATH = "pictures/info_click.jpg"

CLEAR_IDLE_IMAGE_PATH = "pictures/clear_all_idle.jpg"
CLEAR_CLICK_IMAGE_PATH = "pictures/clear_all_click.jpg"
NEXT_INFO_IDLE_IMAGE_PATH = "pictures/next_page.jpg"
PREV_INFO_IDLE_IMAGE_PATH = "pictures/prev_page.jpg"

CAPACITY_IMAGE_PATH = "pictures/loading.jpg"

PLEASE_WAIT_SCREEN_0 = "pictures/please_wait_1.jpg"
PLEASE_WAIT_SCREEN_1 = "pictures/please_wait_2.jpg"

LEFT_ALARM_PATH = "pictures/out_of_boundary_alarm.jpg"
RIGHT_ALARM_PATH = "pictures/out_of_boundary_alarm.jpg"
SEGMENT_OUT_OF_BOUNDARY_PATH = "pictures/out_of_boundary_alarm.jpg"
TOO_LONG_ALARM_PATH = "pictures/max_length_alarm.jpg"
