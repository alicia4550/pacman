import pygame

class Wall(object):
    def __init__(self, x, y, width, height):
        self.x = (x * 32)
        self.y = (y * 32)
        self.width = (width * 32)
        self.height = (height * 32)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 255), self.rect, 2)