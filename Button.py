import pygame
from enum import Enum


class Button(object):
    class State(Enum):
        IDLE = 1
        CLICK = 2
        HOVER = 3

    def __init__(self, screen, pos, size, color, coloron, function):
        self.pos = pos
        self.size = size
        self.color = color
        self.coloron = coloron
        self.img = None
        self.imghov = None
        self.imgon = None
        self.function = function
        self.press_once = False
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

    def draw(self):
        if self.state == self.State.IDLE:
            pygame.draw.rect(self.screen, self.color, self.rect)
            self.screen.blit(self.img, self.img.get_rect(center=self.rect.center))
        elif self.state == self.State.CLICK:
            pygame.draw.rect(self.screen, self.coloron, self.rect)
            self.screen.blit(self.imgon, self.imgon.get_rect(center=self.rect.center))
        elif self.state == self.State.HOVER:
            pygame.draw.rect(self.screen, self.color, self.rect)
            self.screen.blit(self.imghov, self.imghov.get_rect(center=self.rect.center))

    def load_image(self, image_state, image_path):
        temp_image = pygame.image.load(image_path)
        temp_image = pygame.transform.scale(temp_image, self.size)

        if image_state == self.State.IDLE:
            self.img = temp_image
        elif image_state == self.State.CLICK:
            self.imgon = temp_image
        elif image_state == self.State.HOVER:
            self.imghov = temp_image





            # def check(self):
    #     mouse = pygame.mouse.get_pos()
    #     click = pygame.mouse.get_pressed()
    #     on_button = self.rect.collidepoint(mouse)
    #     if not on_button:
    #         pygame.draw.rect(self.screen, self.color, self.rect)
    #         self.screen.blit(self.img, self.img.get_rect(center=self.rect.center))
    #         self.done = True
    #     elif click[0] == 0:
    #         pygame.draw.rect(self.screen, self.color, self.rect)
    #         self.screen.blit(self.imghov, self.imghov.get_rect(center=self.rect.center))
    #         self.done = True
    #     elif click[0] == 1 and self.done:
    #         pygame.draw.rect(self.screen, self.coloron, self.rect)
    #         self.screen.blit(self.imgon, self.imgon.get_rect(center=self.rect.center))
    #         if self.press_once:
    #             self.done = False
    #         if self.function is not None:
    #             self.function()
    #     else:
    #         pygame.draw.rect(self.screen, self.coloron, self.rect)
    #         self.screen.blit(self.imgon, self.imgon.get_rect(center=self.rect.center))



