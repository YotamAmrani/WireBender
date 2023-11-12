import pygame
from enum import Enum
import time
from Constants import CONVERSION_FACTOR


class Alarm:
    alarm_timer = 1

    def __init__(self, screen, position, color, event_id):
        self.screen = screen
        self.position = position
        self.color = color
        self.img = None
        self.turn_on = False
        self.timer = 0
        self.event_id = event_id

    def load_image(self, image_path: str):
        temp_image = pygame.image.load(image_path)
        size = temp_image.get_size()
        size = (size[0] * CONVERSION_FACTOR, size[1] * CONVERSION_FACTOR)
        temp_image = pygame.transform.scale(temp_image, size)
        self.img = temp_image

    def draw_alarm(self):
        if self.timer == 0 and self.turn_on:
            self.timer = time.time()
        else:
            if time.time() - self.timer < Alarm.alarm_timer and self.turn_on:
                self.screen.blit(self.img, self.img.get_rect(center=self.screen.get_rect().center))
            else:
                self.turn_on = False
                self.timer = 0

