import pygame

class Button(object):
    def __init__(self, screen, pos, size, color, coloron, img, imghov ,imgon, function, press_once=False):
        self.pos = pos
        self.size = size
        self.color = color
        self.coloron = coloron
        self.img = img
        self.imghov = imghov
        self.imgon = imgon
        self.function = function
        self.press_once = press_once
        self.done = True
        self.screen = screen

    def check(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        on_button = rect.collidepoint(mouse)
        if not on_button:
            pygame.draw.rect(self.screen, self.color, rect)
            self.screen.blit(self.img, self.img.get_rect(center=rect.center))
            self.done = True
        elif click[0] == 0:
            pygame.draw.rect(self.screen, self.color, rect)
            self.screen.blit(self.imghov, self.imghov.get_rect(center=rect.center))
            self.done = True
        elif click[0] == 1 and self.done:
            pygame.draw.rect(self.screen, self.coloron, rect)
            self.screen.blit(self.imgon, self.imgon.get_rect(center=rect.center))
            if self.press_once:
                self.done = False
            if self.function is not None:
                self.function()
        else:
            pygame.draw.rect(self.screen, self.coloron, rect)
            self.screen.blit(self.imgon, self.imgon.get_rect(center=rect.center))

