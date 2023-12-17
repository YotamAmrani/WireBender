from Constants import *
import sys
import pygame
from View import *
from Model import *
import time
import serial
from myLogger import logger

# TODO: setup maybe minimal length to the wire after large rotation
# TODO: add automatic reset to welcome page


# Drawing with rounded corners
# https://stackoverflow.com/questions/70051590/draw-lines-with-round-edges-in-pygame

# Rotating an object:
# https://stackoverflow.com/questions/59902716/how-to-rotate-element-around-pivot-point-in-pygame


# Time rotating logging
# https://stackoverflow.com/questions/44718204/python-how-to-create-log-file-everyday-using-logging-module



class Controller:
    def __init__(self):

        # screen = pygame.display.set_mode((width, height))
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen.fill(SCREEN_COLOR)

        print("screen width: ", pygame.display.Info().current_w)
        print("screen height: ", pygame.display.Info().current_h)
        logger.info("Screen width: " + str(pygame.display.Info().current_w))
        logger.info("screen height: " + str(pygame.display.Info().current_h))

        self.model = Model(screen)
        logger.info("Model module loaded successfully!")
        self.view = View(self.model)
        logger.info("View module loaded successfully!")
        self.load_buttons()
        logger.info("Buttons were loaded successfully!")
        self.load_alarms()
        logger.info("Alarms were loaded successfully!")
        self.add_colliders()
        logger.info("Colliders were loaded successfully!")

        try:
            self.serial = serial.Serial('/dev/ttyACM0', baudrate=BAUD_RATE, timeout=1)
        except serial.SerialException as e:
            # print(e)
            # print("ERROR: could not open serial port")
            logger.critical("could not open serial port: " + '/dev/ttyACM0')
            logger.critical("make sure baud rate is correct, serial port is configured by the system,"
                             "and that the USB cable is connected.")
            logger.critical("the serial module exception message: " + str(e))
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

        self.model.append_button("CLEAR", self.clear_all, CLEAR_BUTTON_POSITION, ROTATE_LEFT_BUTTON_SIZE,
                                 CLEAR_IDLE_IMAGE_PATH,
                                 CLEAR_CLICK_IMAGE_PATH, True)

        self.model.append_button("NEXT", self.next_info_screen, NEXT_BUTTON_POSITION, ROTATE_LEFT_BUTTON_SIZE,
                                 NEXT_INFO_IDLE_IMAGE_PATH,
                                 NEXT_INFO_IDLE_IMAGE_PATH, True)

        self.model.append_button("PREV", self.prev_info_screen, NEXT_BUTTON_POSITION, ROTATE_LEFT_BUTTON_SIZE,
                                 PREV_INFO_IDLE_IMAGE_PATH,
                                 PREV_INFO_IDLE_IMAGE_PATH, True)

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
                if not ((button.name == "NEXT" and not self.model.current_info_page == 0) or
                        (button.name == "PREV" and not self.model.current_info_page == 1)):
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

    def add_segment(self):
        current_segment = (self.model.segment_length, self.model.bender_angle)
        # print("adding: " + str(self.model.segment_length))
        if current_segment[0] != 0 and current_segment[1] != 0:
            self.model.total_length += self.model.segment_length
            self.model.polar_points = [current_segment] + self.model.polar_points
        # print(self.model.polar_points)
        logger.info("Segment was added: " + str(current_segment))
        logger.info("current state: " + str(self.model.polar_points))

    def reset_state(self):
        self.model.bender_angle = 0
        self.model.segment_length = MINIMAL_SEGMENT_LENGTH
        logger.info("reset state")
        logger.info("current state: " + str(self.model.polar_points))

    def revert(self):
        if self.model.polar_points:
            self.model.segment_length, self.model.bender_angle = self.model.polar_points[0]
            self.model.total_length -= self.model.segment_length
            self.model.polar_points = self.model.polar_points[1:]
            # print(self.model.total_length)
            # print("revert: " + str(self.model.polar_points))
            # print("cuurent: ")
            # print(self.model.segment_length, self.model.bender_angle)
            logger.info("revert: " + str(self.model.polar_points))
            logger.info("current: " + str(self.model.segment_length) + "," + str(self.model.bender_angle))



        else:
            self.reset_state()
        logger.info("revert last step")
        logger.info("current state: " + str(self.model.polar_points))

    def extrude(self):
        if self.test_collisions(self.model.segment_length + 1, self.model.bender_angle) or \
                self.test_boarders(self.model.segment_length + 1, self.model.bender_angle):
            pygame.event.post(pygame.event.Event(SEGMENT_OUT_OF_BOUNDARY_ALARM))
            logger.info("Segment is out of boundaries!")

        elif self.model.bender_angle == 0:
            if self.model.total_length + self.model.segment_length < LINE_MAX_LENGTH:
                self.model.segment_length += PIXEL_PER_PRESS
            else:
                pygame.event.post(pygame.event.Event(SEGMENT_TOO_LONG_ALARM))
                # print("segment is too long alarm")
                logger.info("Segment is too long!")

        else:
            if self.model.total_length + self.model.segment_length < LINE_MAX_LENGTH:
                self.add_segment_and_reset()
            else:
                pygame.event.post(pygame.event.Event(SEGMENT_TOO_LONG_ALARM))
                # print("segment is too long alarm")
                logger.info("Segment is too long!")

    def rotate_right(self):
        if self.test_collisions(self.model.segment_length, self.model.bender_angle - 1) or \
                self.test_boarders(self.model.segment_length, self.model.bender_angle - 1):
            pygame.event.post(pygame.event.Event(SEGMENT_OUT_OF_BOUNDARY_ALARM))
            # print("out ou boundary right")
            logger.info("Segment is out of boundaries! to the right")

        elif self.model.bender_angle > RIGHT_MIN_VALUE:
            self.model.bender_angle -= 1

        else:
            pygame.event.post(pygame.event.Event(ROTATE_RIGHT_ALARM))
            # print("rotate right alarm")
            logger.info("Segment is out of boundaries! to the right")


    def rotate_left(self):
        if self.test_collisions(self.model.segment_length, self.model.bender_angle + 1) or \
                self.test_boarders(self.model.segment_length, self.model.bender_angle + 1):
            pygame.event.post(pygame.event.Event(SEGMENT_OUT_OF_BOUNDARY_ALARM))
            logger.info("Segment is out of boundaries! to the left")

        elif self.model.bender_angle < LEFT_MAX_VALUE:
            self.model.bender_angle += 1

        else:
            pygame.event.post(pygame.event.Event(ROTATE_LEFT_ALARM))
            # print("rotate left alarm")
            logger.info("Segment is out of boundaries! to the left")

    def add_segment_and_reset(self):
        self.add_segment()
        self.reset_state()

    def send_to_bender(self):
        #     non blocking version of send to bender
        if self.serial is not None:
            if not self.model.is_bending: # case we sent print for the first time
                self.serial.read_all()
                self.model.is_bending = True
                self.model.pending_screen_timer = time.time()
                self.model.current_polar_point = len(self.model.polar_points)-1
                # print("Enter bending mode")
                # print("We have " + str(len(self.model.polar_points)) + " segments!")
                logger.info("Enter bending mode")
                logger.info("We have " + str(len(self.model.polar_points)) + " segments!")

            elif self.model.is_bending and self.model.current_polar_point >= 0 and not self.model.sent_current_segment:
                # case we send one the segments
                self.model.sent_current_segment = True
                current_segment = self.model.polar_points[self.model.current_polar_point]
                # print("segment is: " + str(current_segment))
                logger.info("segment is: " + str(current_segment))
                to_string = str(current_segment[0] // PIXEL_TO_MM) + "," + str(current_segment[1] * -1) + "\n"
                self.serial.write(to_string.encode())
                # print("sent :" + to_string)
                logger.info("sent :" + to_string)
            elif (self.model.is_bending and self.model.current_polar_point == CUT_COMMAND
                  and not self.model.sent_current_segment):
                # case we need to send CUT
                # print("Sending CUT")
                logger.info("sent CUT!")
                to_string = "CUT" + "\n"
                self.serial.write(to_string.encode())
                self.model.sent_current_segment = True
            elif (self.model.is_bending and self.model.current_polar_point == LAST_SEGMENT_COMMAND
                  and not self.model.sent_current_segment):
                # case we need to send CUT
                to_string = str(self.model.segment_length // PIXEL_TO_MM) + "," + str(self.model.bender_angle* -1) + "\n"
                # print("Sending last segment: " + to_string)
                logger.info("Sending last segment: " + to_string)

                self.serial.write(to_string.encode())
                self.model.sent_current_segment = True

            elif self.model.sent_current_segment:
                # case we wait for approval message (degree is not 0 or we sent "CUT")
                if ((self.model.current_polar_point == LAST_SEGMENT_COMMAND and self.model.bender_angle != 0) or
                        self.model.current_polar_point == CUT_COMMAND or
                    (self.model.current_polar_point >= 0 and
                     self.model.polar_points[self.model.current_polar_point][1] != 0)):
                    acknowledge = self.serial.readline().decode().strip()
                    if "OK" in acknowledge:
                        # print(acknowledge)
                        # print("acknowledge segment: " + str(self.model.current_polar_point))
                        logger.info("acknowledge segment: " + str(self.model.current_polar_point))

                        self.model.sent_current_segment = False
                        self.model.current_polar_point -= 1

                # case degree is 0
                elif ((self.model.current_polar_point == LAST_SEGMENT_COMMAND and self.model.bender_angle == 0) or
                      (self.model.current_polar_point >= 0
                       and self.model.polar_points[self.model.current_polar_point][1] == 0)):
                    time.sleep(3)
                    # print("acknowledge segment: " + str(self.model.current_polar_point))
                    logger.info("acknowledge segment: " + str(self.model.current_polar_point))
                    self.model.sent_current_segment = False
                    self.model.current_polar_point -= 1

            else:
                # print("Ending bend mode")
                logger.info("Exit bend mode")

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
        self.model.current_info_page = 0
        logger.info("Info button was pressed")

    def next_info_screen(self):
        logger.info("Next info screen button was pressed")
        self.model.current_info_page += 1

    def prev_info_screen(self):
        logger.info("Prev info screen button was pressed")
        self.model.current_info_page -= 1

    def close_info_screen(self):
        self.model.info_turn_on = False

    def clear_all(self):
        # reset to new plan
        self.model.points = []
        self.model.polar_points = []
        self.reset_state()
        self.model.total_length = 0
        self.model.is_bending = False
        logger.info("Cleared all segments")
        logger.info("current state: " + str(self.model.polar_points))

    @staticmethod
    def finish():
        logger.info("Quit")
        pygame.event.post(pygame.event.Event(QUIT))


def runPyGame():
    try:
        pygame.init()
        logger.info("pygame Loaded successfully!")
    except e:
        logger.critical("pygame failed to load")

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


def main():
    runPyGame()


if __name__ == "__main__":
    main()