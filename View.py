from Model import *
import math
import pygame


class View:
    """
    The View object will extract the current game state,
    and update the current state accordingly.
    (the model will draw to screen all the elements)
    """

    def __init__(self, model: Model):
        self._model = model

    def draw_line_round_corners_polygon(self, p1, p2, c, w):
        p1v = pygame.math.Vector2(p1)
        p2v = pygame.math.Vector2(p2)
        if p2v - p1v:
            lv = (p2v - p1v).normalize()
            lnv = pygame.math.Vector2(-lv.y, lv.x) * w // 2
            pts = [p1v + lnv, p2v + lnv, p2v - lnv, p1v - lnv]
            pygame.draw.polygon(self._model.screen, c, pts)
            pygame.draw.circle(self._model.screen, c, p1, round(w / 2))
            pygame.draw.circle(self._model.screen, c, p2, round(w / 2))

    def draw_metal_line(self, start_position, end_position):
        self.draw_line_round_corners_polygon(start_position, end_position, LINE_COLOR, LINE_WIDTH)
        # draw_line_round_corners_polygon(screen, start_position + pygame.math.Vector2(5, 0),
        #                                 end_position + pygame.math.Vector2(5, 0), DARK_GREY, 7)
        # draw_line_round_corners_polygon(screen, start_position + pygame.math.Vector2(0, 0),
        #                                 end_position + pygame.math.Vector2(0, 0), 'white', 5)

    def draw_start_line(self):
        # Draw the starting line
        start_position = pygame.math.Vector2(self._model.screen.get_width() // 2, self._model.screen.get_height())
        end_position = pygame.math.Vector2(self._model.screen.get_width() // 2,
                                           self._model.screen.get_height() - SPINNER_DISTANCE)
        self._model.screen.fill(SCREEN_COLOR)
        self.draw_metal_line(start_position, end_position)

    def draw_current_line(self):

        # Turn the current line segment
        if self._model.segment_length > 0:
            # self._model.screen.fill(SCREEN_COLOR)

            radar_center = (self._model.screen.get_width() // 2, self._model.screen.get_height() - SPINNER_DISTANCE)
            x = radar_center[0] + math.sin(math.radians(self._model.bender_angle)) * \
                                  (-self._model.segment_length)
            y = radar_center[1] + math.cos(math.radians(self._model.bender_angle)) * \
                                  (-self._model.segment_length)

            # then render the line radar->(x,y)
            # self.draw_metal_line(start_position, radar_center)
            self.draw_metal_line(radar_center, (x, y))

    def draw_current_spinner(self):

        rotated = pygame.transform.rotate(self._model.spinner, self._model.bender_angle)
        self._model.screen.blit(rotated, rotated.get_rect(center=(self._model.screen.get_width() // 2,
                                                                  self._model.screen.get_height() - SPINNER_DISTANCE)))

        # circle = pygame.draw.circle(screen, 'black', (0, 0), 30, width=2)
        # rotated = pygame.transform.rotate(circle, angle)
        # screen.blit(rotated,
        # rotated.get_rect(center=(screen.get_width() // 2, screen.get_height() - SPINNER_DISTANCE)))

    def draw_multiple_lines(self):
        for i in range(len(self._model.points) - 1):
            self.draw_metal_line(self._model.points[i + 1], self._model.points[i])

    def draw_buttons(self):
        """
        Check all buttons states. # for each button, check if it was pressed
        :return: None
        """
        for button in self._model.buttons:
            button.draw_button()
            # print("was here!")

    def draw_alarms(self):
        for a in self._model.alarms:
            if a.turn_on:
                a.draw_alarm()

    def draw_length_bar(self):
        bar_width = 200
        bar_hieght = 30
        bar_offset = 60

        font = pygame.font.Font(FONT_PATH, 24)
        text = font.render('Segment capacity', True, 'black', SCREEN_COLOR)
        textRect = text.get_rect()
        textRect.left = bar_offset
        textRect.top = SCREEN_HEIGHT - bar_offset - bar_hieght -5

        pygame.draw.rect(self._model.screen, BLACK,
                         (bar_offset-10, textRect.top -10, bar_width +25, bar_hieght+50
                          ), 8)
        pygame.draw.rect(self._model.screen, SCREEN_COLOR,
                         (bar_offset - 10, textRect.top - 10, bar_width + 25, bar_hieght + 50
                          ))

        self._model.screen.blit(text, textRect)



        ratio = ((self._model.total_length + self._model.segment_length)
                                                              / LINE_MAX_LENGTH)

        pygame.draw.rect(self._model.screen, 'grey', (bar_offset, SCREEN_HEIGHT - bar_offset, bar_width+6, bar_hieght
                                                         ))
        if ratio < 0.95:
            pygame.draw.rect(self._model.screen, 'green',
                             (bar_offset+3,SCREEN_HEIGHT - bar_offset+3, bar_width*ratio, bar_hieght-6))
        elif ratio <=1:
            pygame.draw.rect(self._model.screen, 'red',
                             (bar_offset + 3, SCREEN_HEIGHT - bar_offset + 3, bar_width * ratio, bar_hieght - 6))


    def collision_box(self):
        # get the start point
        # end_position = pygame.math.Vector2(self._model.screen.get_width() // 2,
        #                                    self._model.screen.get_height() - SPINNER_DISTANCE)

        # for i in range(0,SPINNER_DISTANCE, 10):
        #     pygame.draw.rect(self._model.screen, 'red', ((SCREEN_WIDTH-(300-i*2))//2, (SCREEN_HEIGHT-i), 300-i*2, i))
            # print(i)
        for c in self._model.colliders:
            pygame.draw.rect(self._model.screen, 'red',
                             c)
            print(c)


    def draw(self):
        self.draw_start_line()
        self.draw_current_line()
        # extract_multiple_points(self._model.screen)
        if self._model.points:
            self.draw_multiple_lines()
        self.draw_current_spinner()
        self.draw_buttons()
        self.draw_alarms()
        self.draw_length_bar()
        # self.collision_box()
