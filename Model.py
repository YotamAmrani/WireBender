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
        self.bender_angle = 0
        self.segment_length = 0
        self.total_length = 0
        self.buttons = []
        self.alarms = []
        self.spinner = pygame.image.load(SPINNER_IMAGE)
        self.key_0_pressed = False
        self.key_1_pressed = False
        self.key_2_pressed = False

    def append_button(self, button_function, image_position, image_size, idle_image_path, hover_image_path, click_image_path,press_once = False):
        # set the buttons and make an array of them
        current_button = Button(self.screen, image_position, image_size, buttonInactiveColour,
                                buttonPressedColour,button_function, press_once)
        current_button.load_image(Button.State.IDLE, idle_image_path)
        current_button.load_image(Button.State.HOVER, hover_image_path)
        current_button.load_image(Button.State.CLICK, click_image_path)
        self.buttons.append(current_button)

    def append_alarm(self,image_position, image_size,image_path, event_id):
        current_alarm = Alarm(self.screen, image_position, image_size, buttonInactiveColour, event_id)
        current_alarm.load_image(image_path)
        self.alarms.append(current_alarm)


