from Constants import *
import sys
import pygame
from View import *
from Model import *
import time
import serial
import logging

# TODO: setup maybe minimal length to the wire after large rotation
# TODO: differ between one time press button and long press
# TODO: add logger to the system
# TODO: add currently bending banner
# TODO: add automatic reset to welcome page


# Drawing with rounded corners
# https://stackoverflow.com/questions/70051590/draw-lines-with-round-edges-in-pygame

# Rotating an object:
# https://stackoverflow.com/questions/59902716/how-to-rotate-element-around-pivot-point-in-pygame


# Time rotating logging
# https://stackoverflow.com/questions/44718204/python-how-to-create-log-file-everyday-using-logging-module

logging.basicConfig(filename='logging.log', level=logging.DEBUG)


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
        self.add_colliders()

        try:
            self.serial = serial.Serial('/dev/ttyACM0', baudrate=BAUD_RATE, timeout=1)
        except serial.SerialException as e:
            print(e)
            print("ERROR: could not open serial port")
            self.serial = None

    def load_buttons(self):
        self.model.append_button("PRESS", self.extrude, EXTRUDE_BUTTON_POSITION, EXTRUDE_BUTTON_SIZE,
                                 EXTRUDE_IDLE_IMAGE_PATH, EXTRUDE_CLICK_IMAGE_PATH)
        self.model.append_button("REVERT", self.revert, REVERT_BUTTON_POSITION, REVERT_BUTTON_SIZE,
                                 REVERT_IDLE_IMAGE_PATH, REVERT_CLICK_IMAGE_PATH, True)
        self.model.append_button("ROTATE RIGHT", self.rotate_right, ROTATE_RIGHT_BUTTON_POSITION,
                                 ROTATE_RIGHT_BUTTON_SIZE,
                                 ROTATE_RIGHT_IDLE_IMAGE_PATH,
                                 ROTATE_RIGHT_CLICK_IMAGE_PATH)
        self.model.append_button("ROTATE LEFT", self.rotate_left, ROTATE_LEFT_BUTTON_POSITION, ROTATE_LEFT_BUTTON_SIZE,
                                 ROTATE_LEFT_IDLE_IMAGE_PATH,
                                 ROTATE_LEFT_CLICK_IMAGE_PATH)

        self.model.append_button("SEND", self.send_to_bender, SEND_BUTTON_POSITION, ROTATE_LEFT_BUTTON_SIZE,
                                 SEND_IDLE_IMAGE_PATH,
                                 SEND_CLICK_IMAGE_PATH, True)

        self.model.append_button("INFO", self.display_info, INFO_BUTTON_POSITION, ROTATE_LEFT_BUTTON_SIZE,
                                 INFO_IDLE_IMAGE_PATH,
                                 INFO_CLICK_IMAGE_PATH, True)

        self.model.append_button("CLOSE INFO", self.close_info_screen, CLOSE_INFO_BUTTON_POSITION,
                                 ROTATE_LEFT_BUTTON_SIZE,
                                 CLOSE_INFO_IDLE_IMAGE_PATH,
                                 CLOSE_INFO_CLICK_IMAGE_PATH, True)
        # self.model.append_button(self.add_segment_and_reset, ADD_SEGMENT_BUTTON_POSITION, ADD_SEGMENT_BUTTON_SIZE,
        #                          ADD_SEGMENT_IDLE_IMAGE_PATH, ADD_SEGMENT_HOVER_IMAGE_PATH,
        #                          ADD_SEGMENT_CLICK_IMAGE_PATH, True)
        # self.model.append_button(self.finish, FINISH_BUTTON_POSITION, FINISH_BUTTON_SIZE,
        #                          FINISH_IDLE_IMAGE_PATH, FINISH_HOVER_IMAGE_PATH,
        #                          FINISH_CLICK_IMAGE_PATH, True)

    def load_alarms(self):
        self.model.append_alarm(ALARM_POSITION, RIGHT_ALARM_PATH, ROTATE_RIGHT_ALARM)
        self.model.append_alarm(ALARM_POSITION, LEFT_ALARM_PATH, ROTATE_LEFT_ALARM)
        self.model.append_alarm(ALARM_POSITION, SEGMENT_OUT_OF_BOUNDARY_PATH, SEGMENT_OUT_OF_BOUNDARY_ALARM)
        self.model.append_alarm(ALARM_POSITION, TOO_LONG_ALARM_PATH, SEGMENT_TOO_LONG_ALARM)

    def add_colliders(self):
        # for i in range(0,SPINNER_DISTANCE, 10):
        #     self.model.colliders.append(Rect((SCREEN_WIDTH-(420-i*2))//2, (SCREEN_HEIGHT-i), 420-i*2, i))
        for i in range(SPINNER_DISTANCE, 0, -10):
            self.model.colliders.append(
                Rect((SCREEN_WIDTH - (SPINNER_DISTANCE - i) * 2) // 2, (SCREEN_HEIGHT - i), (SPINNER_DISTANCE - i) * 2,
                     i))
            # pygame.draw.rect(self._model.screen, 'red', ((SCREEN_WIDTH-(300-i*2))//2, (SCREEN_HEIGHT-i), 300-i*2, i))
            # print(i)

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
            elif event.type == SEGMENT_OUT_OF_BOUNDARY_ALARM:
                self.model.alarms[2].turn_on = True
            elif event.type == SEGMENT_TOO_LONG_ALARM:
                self.model.alarms[3].turn_on = True

        global key_0_pressed
        global key_1_pressed
        global key_2_pressed

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.model.segment_length += 1
        elif keys[pygame.K_DOWN] and self.model.segment_length > 0:
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

        self.model.points = self.extract_multiple_points(self.model.segment_length, self.model.bender_angle)

        self.check_buttons()

    def check_buttons(self):
        """
        Check all buttons states. # for each button, check if it was pressed
        :return: None
        """
        for button in self.model.buttons:
            if self.model.is_bending and button.name == "SEND":
                button.update()
                self.send_to_bender()
            elif not self.model.is_bending:
                button.update()

    def extract_multiple_points(self, length, angle):
        points = []
        if self.model.polar_points:
            origin = pygame.Vector2(self.model.screen.get_width() // 2,
                                    self.model.screen.get_height() - SPINNER_DISTANCE)
            # points.append(origin)
            edge_point = pygame.Vector2(0, 0)
            edge_point.from_polar((length, -(90 + angle)))
            edge_point += origin

            # new_polar_points = [origin.as_polar()] + polar_points
            points = [edge_point]
            current_angle = angle
            for p in range(len(self.model.polar_points)):
                phi, r = self.model.polar_points[p]
                # convert to current presentation
                r = -(r + current_angle + 90)
                # rotate by angles of previous lines
                current_polar_point = pygame.Vector2(0, 0)
                current_polar_point.from_polar((phi, r))
                current_polar_point += points[p]
                points.append(current_polar_point)
                current_angle += self.model.polar_points[p][1]

        return points
        # print(self.model.points)

    def add_segment(self):
        current_segment = (self.model.segment_length, self.model.bender_angle)
        print("adding: " + str(self.model.segment_length))
        if current_segment[0] != 0 and current_segment[1] != 0:
            self.model.total_length += self.model.segment_length
            self.model.polar_points = [current_segment] + self.model.polar_points
        print(self.model.polar_points)

    def reset_state(self):
        self.model.bender_angle = 0
        self.model.segment_length = MINIMAL_SEGMENT_LENGTH

    def revert(self):
        if self.model.polar_points:
            self.model.segment_length, self.model.bender_angle = self.model.polar_points[0]
            self.model.total_length -= self.model.segment_length
            self.model.polar_points = self.model.polar_points[1:]
            # print(self.model.total_length)
            print("revert: " + str(self.model.polar_points))
            print("cuurent: ")
            print(self.model.segment_length, self.model.bender_angle)
        else:
            self.reset_state()

    def extrude(self):
        if self.test_collisions(self.model.segment_length + 1, self.model.bender_angle) or \
                self.test_boarders(self.model.segment_length + 1, self.model.bender_angle):
            pygame.event.post(pygame.event.Event(SEGMENT_OUT_OF_BOUNDARY_ALARM))

        elif self.model.bender_angle == 0:
            if self.model.total_length + self.model.segment_length < LINE_MAX_LENGTH:
                self.model.segment_length += 1
            else:
                pygame.event.post(pygame.event.Event(SEGMENT_TOO_LONG_ALARM))
                print("segment is too long alarm")

        else:
            self.add_segment_and_reset()

    def rotate_right(self):
        if self.test_collisions(self.model.segment_length, self.model.bender_angle - 1) or \
                self.test_boarders(self.model.segment_length, self.model.bender_angle - 1):
            pygame.event.post(pygame.event.Event(SEGMENT_OUT_OF_BOUNDARY_ALARM))
            print("out ou boundary right")

        elif self.model.bender_angle > RIGHT_MIN_VALUE:
            self.model.bender_angle -= 1

        else:
            pygame.event.post(pygame.event.Event(ROTATE_RIGHT_ALARM))
            print("rotate right alarm")

    def rotate_left(self):
        if self.test_collisions(self.model.segment_length, self.model.bender_angle + 1) or \
                self.test_boarders(self.model.segment_length, self.model.bender_angle + 1):
            pygame.event.post(pygame.event.Event(SEGMENT_OUT_OF_BOUNDARY_ALARM))
            print("out ou boundary right")

        elif self.model.bender_angle < LEFT_MAX_VALUE:
            self.model.bender_angle += 1

        else:
            pygame.event.post(pygame.event.Event(ROTATE_LEFT_ALARM))
            print("rotate left alarm")

    def add_segment_and_reset(self):
        self.add_segment()
        self.reset_state()

    # def send_to_bender(self):
    #     if self.serial is not None:
    #         self.model.is_bending = True
    #         self.model.pending_screen_timer = time.time()
    #         for seg in reversed(self.model.polar_points):
    #
    #             print("segment is: " + str(seg))
    #             to_string = str(seg[0] // PIXEL_TO_MM) + "," + str(seg[1]*-1) + "\n"
    #             print("After conversion: " + to_string)
    #             self.serial.write(to_string.encode())
    #             print("sent :"
    #                   + to_string)
    #             time.sleep(6)
    #         to_string = str(self.model.segment_length // PIXEL_TO_MM) + "," + str(0) + "\n"
    #         print("After conversion: " + to_string)
    #         self.serial.write(to_string.encode())
    #         print("sent :"
    #               + to_string)
    #         time.sleep(3)
    #         to_string = "CUT" + "\n"
    #         self.serial.write(to_string.encode())
    #         time.sleep(8)
    #
    #         # reset to new plan
    #         self.model.points = []
    #         self.model.polar_points = []
    #         self.reset_state()
    #         self.model.total_length = 0
    #         self.model.is_bending = False
    def send_to_bender(self):
        #     non blocking version of send to bender
        if self.serial is not None:
            if not self.model.is_bending: # case we sent print for the first time
                self.model.is_bending = True
                self.model.pending_screen_timer = time.time()
                self.model.current_polar_point = len(self.model.polar_points)-1
                print("Enter bending mode")
                print("We have " + str(len(self.model.polar_points)) + " segments!")
            elif self.model.is_bending and self.model.current_polar_point >= 0 and not self.model.sent_current_segment:
                # case we send one the segments
                self.model.sent_current_segment = True
                current_segment = self.model.polar_points[self.model.current_polar_point]
                print("segment is: " + str(current_segment))
                to_string = str(current_segment[0] // PIXEL_TO_MM) + "," + str(current_segment[1] * -1) + "\n"
                self.serial.write(to_string.encode())
                print("sent :"
                      + to_string)
            elif self.model.is_bending and self.model.current_polar_point == -2 and not self.model.sent_current_segment:
                # case we need to send CUT
                print("Sending CUT")
                to_string = "CUT" + "\n"
                self.serial.write(to_string.encode())
                self.model.sent_current_segment = True
            elif self.model.is_bending and self.model.current_polar_point ==-1 and not self.model.sent_current_segment:
                # case we need to send CUT
                to_string = str(self.model.segment_length // PIXEL_TO_MM) + "," + str(0) + "\n"
                print("Sending last segment: " + to_string)
                self.serial.write(to_string.encode())
                self.model.sent_current_segment = True

            elif self.model.sent_current_segment:
                # case we wait for approval message (degree is not 0 or we sent "CUT")
                if ((self.model.current_polar_point == -1 and self.model.bender_angle != 0) or
                        self.model.current_polar_point == -2 or
                    (self.model.current_polar_point >= 0 and
                     self.model.polar_points[self.model.current_polar_point][1] != 0)):
                    acknowledge = self.serial.readline().decode().strip()
                    if "OK" in acknowledge:
                        print(acknowledge)
                        print("acknowledge segment: " + str(self.model.current_polar_point))
                        self.model.sent_current_segment = False
                        self.model.current_polar_point -= 1

                # case degree is 0
                elif ((self.model.current_polar_point == -1 and self.model.bender_angle == 0) or
                      (self.model.current_polar_point >= 0
                       and self.model.polar_points[self.model.current_polar_point][1] == 0)):
                    time.sleep(3)
                    print("acknowledge segment: " + str(self.model.current_polar_point))
                    self.model.sent_current_segment = False
                    self.model.current_polar_point -= 1

            else:
                print("Ending bend mode")
                time.sleep(2)
                # reset to new plan
                self.model.points = []
                self.model.polar_points = []
                self.reset_state()
                self.model.total_length = 0
                self.model.is_bending = False

    def test_collisions(self, length, angle):
        points_to_test = self.extract_multiple_points(length, angle)

        if not points_to_test:
            radar_center = (self.model.screen.get_width() // 2, self.model.screen.get_height() - SPINNER_DISTANCE)
            x = radar_center[0] + math.sin(math.radians(angle)) * \
                (-length)
            y = radar_center[1] + math.cos(math.radians(angle)) * \
                (-length)
            points_to_test.append(pygame.Vector2(x, y))

        for c in self.model.colliders:
            for p in points_to_test:
                if c.collidepoint(p):
                    return True
        return False

    def test_boarders(self, length, angle):
        points_to_test = self.extract_multiple_points(length, angle)
        if not points_to_test:
            radar_center = (self.model.screen.get_width() // 2, self.model.screen.get_height() - SPINNER_DISTANCE)
            x = radar_center[0] + math.sin(math.radians(angle)) * \
                (-length)
            y = radar_center[1] + math.cos(math.radians(angle)) * \
                (-length)
            points_to_test.append(pygame.Vector2(x, y))

        for p in points_to_test:
            if p[0] > SCREEN_WIDTH or p[1] > SCREEN_HEIGHT:
                return True
        return False

    def display_info(self):
        self.model.info_turn_on = not self.model.info_turn_on

    def close_info_screen(self):
        self.model.info_turn_on = False

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

    to_string = "CUT" + "\n"
    controller.serial.write(to_string.encode())
    line = controller.serial.readline()
    # while not line:
    #     controller.serial.readline()
    # print(line.decode())

    print("sent")
    while True:
        controller.update(dt)
        controller.view.draw()

        pygame.display.update()
        pygame.display.flip()
        dt = fpsClock.tick(fps)


runPyGame()
