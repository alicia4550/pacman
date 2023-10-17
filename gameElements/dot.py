import pygame

class Dot(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 4.5, 4.5)
    def draw(self, win):
        pygame.draw.rect(win, (255, 183, 174), self.rect, 2)