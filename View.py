from Model import *
import math


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

    def draw_current_line(self):
        # Draw the starting line
        start_position = pygame.math.Vector2(self._model.screen.get_width() // 2, self._model.screen.get_height())
        end_position = pygame.math.Vector2(self._model.screen.get_width() // 2,
                                           self._model.screen.get_height() - self._model.segment_length)
        self._model.screen.fill(SCREEN_COLOR)
        self.draw_metal_line(start_position, end_position)

        # Turn the current line segment
        if self._model.segment_length > SPINNER_DISTANCE:
            self._model.screen.fill(SCREEN_COLOR)

            radar_center = (self._model.screen.get_width() // 2, self._model.screen.get_height() - SPINNER_DISTANCE)
            x = radar_center[0] + math.sin(math.radians(self._model.bender_angle)) * \
                                  (SPINNER_DISTANCE - self._model.segment_length)
            y = radar_center[1] + math.cos(math.radians(self._model.bender_angle)) * \
                                  (SPINNER_DISTANCE - self._model.segment_length)

            # then render the line radar->(x,y)
            self.draw_metal_line(start_position, radar_center)
            self.draw_metal_line(radar_center, (x, y))
            # pygame.draw.line(screen, Color("black"), radar_center, (x, y), 1)

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
            button.draw()
            # print("was here!")

    def draw(self):

        self.draw_current_line()
        # extract_multiple_points(self._model.screen)
        if self._model.points:
            self.draw_multiple_lines()
        self.draw_current_spinner()
        self.draw_buttons()
