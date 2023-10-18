import pygame

from util import *

class Fruit(pygame.sprite.Sprite):
    def __init__(self, xOffset, points):
        pygame.sprite.Sprite.__init__(self)
        spritesheet = pygame.image.load('Arcade - Pac-Man - General Sprites.png').convert_alpha()
        self.image = get_image(spritesheet, 30.5+xOffset, 3, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        self.rect = self.image.get_rect()
        self.rect.x = (GRID_SPRITE_WIDTH - 0.75) * 32 / 2
        self.rect.y =  (GRID_SPRITE_HEIGHT + 0.5) * 32 / 2
        self.points = points