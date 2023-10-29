import pygame
from enum import Enum
import time
from Constants import CONVERSION_FACTOR


class Alarm:
    alarm_timer = 1

    def __init__(self, screen, position, size, color, event_id):
        self.screen = screen
        self.size = size
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.color = color
        self.img = None
        self.turn_on = False
        self.timer = 0
        self.event_id = event_id

    def load_image(self, image_path: str):
        temp_image = pygame.image.load(image_path)
        size = temp_image.get_size()
        self.size = (size[0] // CONVERSION_FACTOR, size[1] // CONVERSION_FACTOR)
        temp_image = pygame.transform.scale(temp_image, self.size)
        self.img = temp_image

    def draw_alarm(self):
        if self.timer == 0 and self.turn_on:
            self.timer = time.time()
        else:
            if time.time() - self.timer < Alarm.alarm_timer and self.turn_on:
                # print("screen: " + str(self.screen.get_rect().center))
                # print("img: " + str(self.rect.center))
                pygame.draw.rect(self.screen, self.color, self.rect)
                self.screen.blit(self.img, self.img.get_rect(center=self.screen.get_rect().center))
            else:
                self.turn_on = False
                self.timer = 0

