from Constants import *
from Button import *
from Alarm import *
import pygame


class Model:
    """
    The model object will Hold all data
    Attributes. (i.e. at any given time, the model hold the system current state.)
    Model will be updated via the Controller, and enable the View element
    to extract relevant data for the current frame.
    """

    def __init__(self, screen):
        self.screen = screen
        self.points = []
        self.polar_points = []
        self.current_polar_point = -2
        self.sent_current_segment = False
        self.bender_angle = 0
        self.segment_length = MINIMAL_SEGMENT_LENGTH
        self.total_length = 0
        self.buttons = []
        self.alarms = []
        self.colliders = []
        self.spinner = pygame.image.load(SPINNER_IMAGE)
        self.capacity_buffer = pygame.image.load(CAPACITY_IMAGE_PATH)
        self.screen_image = pygame.image.load(SCREEN_IMAGE)
        self.info_modal = pygame.image.load(INFO_SCREEN_IMAGE_PATH)
        self.pending_screen = [pygame.image.load(PLEASE_WAIT_SCREEN_0),pygame.image.load(PLEASE_WAIT_SCREEN_1)]
        self.current_pending_screen = 0
        self.pending_screen_timer = time.time()
        self.info_turn_on = False
        self.is_bending = False
        self.current_segment_sent = 0
        self.key_0_pressed = False
        self.key_1_pressed = False
        self.key_2_pressed = False

    def append_button(self,name, button_function, image_position, image_size, idle_image_path, click_image_path,
                      press_once=False):
        # set the buttons and make an array of them
        current_button = Button(name, self.screen, image_position, image_size
                                , button_function, press_once)
        current_button.load_image(Button.State.IDLE, idle_image_path)
        # current_button.load_image(hover_image_path)
        current_button.load_image(Button.State.CLICK, click_image_path)
        self.buttons.append(current_button)

    def append_alarm(self, image_position, image_path, event_id):
        current_alarm = Alarm(self.screen, image_position, buttonInactiveColour, event_id)
        current_alarm.load_image(image_path)
        self.alarms.append(current_alarm)
