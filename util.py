import pygame
import math

from constants import *

'''
    FUNCTIONS
'''
def get_image(sheet, xOffset, yOffset, width, height, transparent):
    image = pygame.Surface((width, height)).convert_alpha()
    scale = 2

    image.blit(sheet, (0, 0), ((xOffset * width), (yOffset * height), width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))

    if transparent:
        image.set_colorkey((0, 0, 0))

    return image

def getPinkGhostTarget(player):
    x = player.rect.x
    y = player.rect.y
    dir = player.currentDirection

    if dir == 0:
        y -= 8 * SPRITE_PIXEL_SIZE
    elif dir == 1:
        x -= 8 * SPRITE_PIXEL_SIZE
    elif dir == 2:
        y += 8 * SPRITE_PIXEL_SIZE
    else:
        x += 8 * SPRITE_PIXEL_SIZE

    return pygame.Rect(x, y, 16, 16)

def getBlueGhostTarget(player, redGhost):
    playerX = player.rect.x
    playerY = player.rect.y
    playerDir = player.currentDirection
    ghostX = redGhost.rect.x
    ghostY = redGhost.rect.y

    if playerDir == 0:
        playerY -= 4 * SPRITE_PIXEL_SIZE
    elif playerDir == 1:
        playerX -= 4 * SPRITE_PIXEL_SIZE
    elif playerDir == 2:
        playerY += 4 * SPRITE_PIXEL_SIZE
    else:
        playerX += 4 * SPRITE_PIXEL_SIZE

    x = ghostX + ((playerX - ghostX) * 2)
    y = ghostY + ((playerY - ghostY) * 2)

    return pygame.Rect(x, y, 16, 16)

def getOrangeGhostTarget(player, orangeGhost):
    playerX = player.rect.x
    playerY = player.rect.y

    ghostX = orangeGhost.rect.x
    ghostY = orangeGhost.rect.y

    if math.sqrt((abs(playerX - ghostX)^2) + (abs(playerY - ghostY)^2)) > 16:
        orangeGhost.movementMode = "Chase"
        return player.rect
    else:
        orangeGhost.movementMode = "Scatter"
        return orangeGhost.scatterTargetRect