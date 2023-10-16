import pygame
from enum import Enum


class Button(object):
    class State(Enum):
        IDLE = 1
        CLICK = 2
        HOVER = 3

    def __init__(self, screen, pos, size, triggered_function, press_once=False):
        self.pos = pos
        self.size = size
        # self.color = color
        # self.coloron = coloron
        self.img = None
        # self.imghov = None
        # self.imgon = None
        self.function = triggered_function
        self.press_once = press_once
        self.done = True
        self.screen = screen
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.state = self.State.IDLE

    # Split to Update and Draw
    def update(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        on_button = self.rect.collidepoint(mouse)
        if not on_button:
            self.state = self.State.IDLE
            self.done = True
        elif click[0] == 0:
            self.state = self.State.HOVER
            self.done = True
        elif click[0] == 1 and self.done:
            self.state = self.State.CLICK
            if self.press_once:
                self.done = False
            if self.function is not None:
                self.function()
        else:
            self.state = self.State.HOVER

    def draw_button(self):
        if self.state == self.State.IDLE:
            pygame.draw.rect(self.screen, 'white', self.rect)
            # self.screen.blit(self.img, self.img.get_rect(center=self.rect.center))
        elif self.state == self.State.CLICK:
            pygame.draw.rect(self.screen, 'green', self.rect)
            # self.screen.blit(self.imgon, self.imgon.get_rect(center=self.rect.center))
        elif self.state == self.State.HOVER:
            pygame.draw.rect(self.screen, 'grey', self.rect)
            # self.screen.blit(self.imghov, self.imghov.get_rect(center=self.rect.center))
        self.screen.blit(self.img, self.img.get_rect(center=self.rect.center))

    def load_image(self, image_path: str):
        temp_image = pygame.image.load(image_path)
        # temp_image = pygame.transform.scale(temp_image, self.size)
        self.img = temp_image
        # if image_state == self.State.IDLE:

        # elif image_state == self.State.CLICK:
        #     self.imgon = temp_image
        # elif image_state == self.State.HOVER:
        #     self.imghov = temp_image
