from Constants import *
from Button import *
import sys
import pygame
from View import *
from Model import *
import time
import serial


# TODO: setup boarder to the points movement
# TODO: setup limitations to the wire length
# TODO: setup maybe minimal length to the wire after large rotation
# TODO: setup global counter
# TODO: adding alerts to indicate if we passed the length / rotation which is allowed


# Drawing with rounded corners
# https://stackoverflow.com/questions/70051590/draw-lines-with-round-edges-in-pygame

# Rotating an object:
# https://stackoverflow.com/questions/59902716/how-to-rotate-element-around-pivot-point-in-pygame


class Controller:
    def __init__(self):

        # screen = pygame.display.set_mode((width, height))
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen.fill(SCREEN_COLOR)

        print("screen width: ", pygame.display.Info().current_w)
        print("screen height: ", pygame.display.Info().current_h)

        self.model = Model(screen)
        self.view = View(self.model)
        self.load_buttons()
        self.load_alarms()
        try:
            self.serial = serial.Serial('COM3', baudrate=BAUD_RATE, timeout=1)
        except serial.SerialException:
            print("ERROR: could not open serial port")
            self.serial = None

    def load_buttons(self):
        self.model.append_button(self.extrude, EXTRUDE_BUTTON_POSITION, EXTRUDE_BUTTON_SIZE,
                                 EXTRUDE_IDLE_IMAGE_PATH, EXTRUDE_HOVER_IMAGE_PATH, EXTRUDE_CLICK_IMAGE_PATH)
        self.model.append_button(self.revert, REVERT_BUTTON_POSITION, REVERT_BUTTON_SIZE,
                                 REVERT_IDLE_IMAGE_PATH, REVERT_HOVER_IMAGE_PATH, REVERT_CLICK_IMAGE_PATH, True)
        self.model.append_button(self.rotate_right, ROTATE_RIGHT_BUTTON_POSITION, ROTATE_RIGHT_BUTTON_SIZE,
                                 ROTATE_RIGHT_IDLE_IMAGE_PATH, ROTATE_RIGHT_HOVER_IMAGE_PATH,
                                 ROTATE_RIGHT_CLICK_IMAGE_PATH)
        self.model.append_button(self.rotate_left, ROTATE_LEFT_BUTTON_POSITION, ROTATE_LEFT_BUTTON_SIZE,
                                 ROTATE_LEFT_IDLE_IMAGE_PATH, ROTATE_LEFT_HOVER_IMAGE_PATH,
                                 ROTATE_LEFT_CLICK_IMAGE_PATH)
        # self.model.append_button(self.add_segment_and_reset, ADD_SEGMENT_BUTTON_POSITION, ADD_SEGMENT_BUTTON_SIZE,
        #                          ADD_SEGMENT_IDLE_IMAGE_PATH, ADD_SEGMENT_HOVER_IMAGE_PATH,
        #                          ADD_SEGMENT_CLICK_IMAGE_PATH, True)
        self.model.append_button(self.finish, FINISH_BUTTON_POSITION, FINISH_BUTTON_SIZE,
                                 FINISH_IDLE_IMAGE_PATH, FINISH_HOVER_IMAGE_PATH,
                                 FINISH_CLICK_IMAGE_PATH, True)

    def load_alarms(self):
        self.model.append_alarm(ALARM_POSITION, ALARM_SIZE, EXTRUDE_IDLE_IMAGE_PATH, ROTATE_RIGHT_ALARM)
        self.model.append_alarm(ALARM_POSITION, ALARM_SIZE, EXTRUDE_CLICK_IMAGE_PATH, ROTATE_LEFT_ALARM)

    def update(self, dt):
        """
        Update game. Called once per frame.
        dt is the amount of time passed since last frame.
        If you want to have constant apparent movement no matter your framerate,
        what you can do is something like

        x += v * dt

        and this will scale your velocity based on time. Extend as necessary."""

        # Go through events that are passed to the script by the window.
        for event in pygame.event.get():
            # We need to handle these events. Initially the only one you'll want to care
            # about is the QUIT event, because if you don't handle it, your game will crash
            # whenever someone tries to exit.
            if event.type == QUIT:
                pygame.quit()  # Opposite of pygame.init
                sys.exit()  # Not including this line crashes the script on Windows. Possibly
                # on other operating systems too, but I don't know for sure.
                # Handle other events as you wish.
            if event.type == ROTATE_RIGHT_ALARM:
                self.model.alarms[0].turn_on = True
            elif event.type == ROTATE_LEFT_ALARM:
                self.model.alarms[1].turn_on = True


        global key_0_pressed
        global key_1_pressed
        global key_2_pressed

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.model.segment_length += 1
        elif keys[pygame.K_DOWN] and self.model.segment_length > SPINNER_DISTANCE:
            self.model.segment_length -= 1
        if (keys[K_LEFT]) and self.model.bender_angle < LEFT_MAX_VALUE:
            self.model.bender_angle += 1
        elif (keys[K_RIGHT]) and self.model.bender_angle > RIGHT_MIN_VALUE:
            self.model.bender_angle -= 1
        elif keys[K_0]:
            key_0_pressed = keys[K_0]
        elif not keys[K_0] and key_0_pressed:
            self.add_segment()
            self.reset_state()
            key_0_pressed = keys[K_0]
        elif keys[K_1]:
            key_1_pressed = keys[K_1]
        elif not keys[K_1] and key_1_pressed:
            self.revert()
            key_1_pressed = keys[K_1]
        elif keys[K_2]:
            key_2_pressed = keys[K_2]
        elif not keys[K_2] and key_2_pressed:
            # send_to_bender()
            key_2_pressed = keys[K_2]
        if keys[K_ESCAPE]:
            pygame.event.post(pygame.event.Event(QUIT))

        self.extract_multiple_points()
        self.check_buttons()

    def check_buttons(self):
        """
        Check all buttons states. # for each button, check if it was pressed
        :return: None
        """
        for button in self.model.buttons:
            button.update()

    def extract_multiple_points(self):

        self.model.points = []
        if self.model.polar_points:
            origin = pygame.Vector2(self.model.screen.get_width() // 2,
                                    self.model.screen.get_height() - SPINNER_DISTANCE)
            # points.append(origin)
            edge_point = pygame.Vector2(0, 0)
            edge_point.from_polar((self.model.segment_length - SPINNER_DISTANCE, -(90 + self.model.bender_angle)))
            edge_point += origin

            # new_polar_points = [origin.as_polar()] + polar_points
            self.model.points = [edge_point]
            current_angle = self.model.bender_angle
            for p in range(len(self.model.polar_points)):
                phi, r = self.model.polar_points[p]
                # convert to current presentation
                r = -(r + current_angle + 90)
                # rotate by angles of previous lines
                current_polar_point = pygame.Vector2(0, 0)
                current_polar_point.from_polar((phi, r))
                current_polar_point += self.model.points[p]
                self.model.points.append(current_polar_point)
                current_angle += self.model.polar_points[p][1]

                # print(self.model.points)

    def add_segment(self):
        current_segment = (self.model.segment_length - SPINNER_DISTANCE, self.model.bender_angle)
        if current_segment[0] != 0 and current_segment[1] != 0:
            self.model.total_length += self.model.segment_length - SPINNER_DISTANCE
            self.model.polar_points = [current_segment] + self.model.polar_points
        print(self.model.polar_points)

    def reset_state(self):
        self.model.bender_angle = 0
        self.model.segment_length = SPINNER_DISTANCE

    def revert(self):
        if self.model.polar_points:
            self.model.segment_length, self.model.bender_angle = self.model.polar_points[0]
            self.model.total_length -= self.model.segment_length
            self.model.polar_points = self.model.polar_points[1:]
            print(self.model.total_length)
        else:
            self.model.segment_length, self.model.bender_angle = (SPINNER_DISTANCE, 0)

    def extrude(self):
        if self.model.bender_angle == 0:
            self.model.segment_length += 1
        else:
            self.add_segment_and_reset()

    def rotate_right(self):
        if self.model.bender_angle > RIGHT_MIN_VALUE:
            self.model.bender_angle -= 1
        else:
            pygame.event.post(pygame.event.Event(ROTATE_RIGHT_ALARM))
            print("rotate right alarm")

    def rotate_left(self):
        if self.model.bender_angle < LEFT_MAX_VALUE:
            self.model.bender_angle += 1
        else:
            pygame.event.post(pygame.event.Event(ROTATE_LEFT_ALARM))
            print("rotate left alarm")

    def add_segment_and_reset(self):
        self.add_segment()
        self.reset_state()

    def send_to_bender(self):
        if self.serial is not None:
            for seg in reversed(self.model.polar_points):
                print("segment is: " + str(seg))
                to_string = str(seg[0] // PIXEL_TO_MM) + "," + str(seg[1]) + "\n"
                print("After conversion: " + to_string)
                print(to_string)
                self.serial.write(to_string.encode())
                time.sleep(15)

    @staticmethod
    def finish():
        print("finish")
        pygame.event.post(pygame.event.Event(QUIT))


def runPyGame():
    pygame.init()

    # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
    fpsClock = pygame.time.Clock()
    # Main game loop.
    dt = 1 / fps  # dt is the time since last frame.
    controller = Controller()
    while True:
        controller.update(dt)
        controller.view.draw()

        pygame.display.update()
        pygame.display.flip()
        dt = fpsClock.tick(fps)


runPyGame()
