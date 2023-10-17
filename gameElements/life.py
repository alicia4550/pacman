import pygame

from util import *

class Life(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        spritesheet = pygame.image.load('Arcade - Pac-Man - General Sprites.png').convert_alpha()
        self.image = get_image(spritesheet, 36.5, 1, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        self.rect = self.image.get_rect()