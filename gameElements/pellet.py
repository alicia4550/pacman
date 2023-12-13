import pygame

class Pellet(object):
    def __init__(self, x, y):
        self.x = int(x * 32)
        self.y = int(y * 32)
        self.rect = pygame.Rect(self.x, self.y, 16, 16)
    def draw(self, win):
        pygame.draw.circle(win, (255, 183, 174), (self.x, self.y), 8)