import pygame
import time
import math
import random

from constants import *
from util import *

from gameElements.dot import Dot
from gameElements.fruit import Fruit
from gameElements.ghost import Ghost
from gameElements.life import Life
from gameElements.pellet import Pellet
from gameElements.player import Player
from gameElements.tile import Tile
from gameElements.wall import Wall

pygame.init()
font = pygame.font.Font("Retro Gaming.ttf", 26)


'''
    SET UP
'''
display = pygame.display.set_mode([LCD_WIDTH, LCD_HEIGHT])

screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

spritesheet = pygame.image.load('Arcade - Pac-Man - General Sprites.png').convert_alpha()

running = True

clock = pygame.time.Clock()
gameMode = "Scatter"

# Create background
screen.fill((0, 0, 0))
map = get_image(spritesheet, 1.02, 0, SPRITE_PIXEL_SIZE*GRID_SPRITE_WIDTH, SPRITE_PIXEL_SIZE*GRID_SPRITE_HEIGHT, False)

# Create walls
wall1 = Wall(1.25, 1.25, 1.5, 1)
wall2 = Wall(3.75, 1.25, 2, 1)
wall3 = Wall(1.25, 3.25, 1.5, 0.5)
wall4 = Wall(3.75, 3.25, 0.5, 3.5)
wall5 = Wall(3.75, 4.75, 2, 0.5)
wall6 = Wall(3.75, 7.75, 0.5, 2)
wall7 = Wall(1.25, 10.75, 1.5, 0.5)
wall8 = Wall(2.25, 10.75, 0.5, 2)
wall9 = Wall(3.75, 10.75, 2, 0.5)
wall10 = Wall(1.25, 13.75, 4.5, 0.5)
wall11 = Wall(3.75, 12.25, 0.5, 2)

wall12 = Wall(5.25, 3.25, 3.5, 0.5)
wall13 = Wall(6.75, 3.25, 0.5, 2)
wall14 = Wall(5.25, 6.25, 3.5, 2)
wall15 = Wall(5.25, 9.25, 3.5, 0.5)
wall16 = Wall(6.75, 9.25, 0.5, 2)
wall17 = Wall(5.25, 12.25, 3.5, 0.5)
wall18 = Wall(6.75, 12.25, 0.5, 2)

wall19 = Wall(11.25, 1.25, 1.5, 1)
wall20 = Wall(8.25, 1.25, 2, 1)
wall21 = Wall(11.25, 3.25, 1.5, 0.5)
wall22 = Wall(9.75, 3.25, 0.5, 3.5)
wall23 = Wall(8.25, 4.75, 2, 0.5)
wall24 = Wall(9.75, 7.75, 0.5, 2)
wall25 = Wall(11.25, 10.75, 1.5, 0.5)
wall26 = Wall(11.25, 10.75, 0.5, 2)
wall27 = Wall(8.25, 10.75, 2, 0.5)
wall28 = Wall(8.25, 13.75, 4.5, 0.5)
wall29 = Wall(9.75, 12.25, 0.5, 2)

wall30 = Wall(6.75, 0, 0.5, 2.25)
wall31 = Wall(0, 12.25, 1.25, 0.5)
wall32 = Wall(12.75, 12.25, 1.25, 0.5)

wall33 = Wall(0, 4.75, 2.75, 2)
wall34 = Wall(0, 7.75, 2.75, 2)
wall35 = Wall(11.25, 4.75, 2.75, 2)
wall36 = Wall(11.25, 7.75, 2.75, 2)

wall37 = Wall(0, 0, 14, 0.25)
wall38 = Wall(0, 15.25, 14, 0.25)
wall39 = Wall(0, 0, 0.25, 5)
wall40 = Wall(0, 9.5, 0.25, 6)
wall41 = Wall(13.75, 0, 0.25, 5)
wall42 = Wall(13.75, 9.5, 0.25, 6)

walls = [
    wall1,
    wall2,
    wall3,
    wall4,
    wall5,
    wall6,
    wall7,
    wall8,
    wall9,
    wall10,
    wall11,
    wall12,
    wall13,
    wall14,
    wall15,
    wall16,
    wall17,
    wall18,
    wall19,
    wall20,
    wall21,
    wall22,
    wall23,
    wall24,
    wall25,
    wall26,
    wall27,
    wall28,
    wall29,
    wall30,
    wall31,
    wall32,
    wall33,
    wall34,
    wall35,
    wall36,
    wall37,
    wall38,
    wall39,
    wall40,
    wall41,
    wall42
]

noSpawn1 = Wall(3.5, 4.75, 7, 5)
noSpawn2 = Wall(0, 4.75, 2.75, 5)
noSpawn3 = Wall(11.25, 4.75, 2.75, 5)

noSpawn4 = Wall(6.5, 11.25, 1, 1)

noSpawn5 = Wall(0.5, 1.5, 0.5, 0.5)
noSpawn6 = Wall(13, 1.5, 0.5, 0.5)
noSpawn7 = Wall(0.5, 11.5, 0.5, 0.5)
noSpawn8 = Wall(13, 11.5, 0.5, 0.5)

noSpawns = [
    noSpawn1,
    noSpawn2,
    noSpawn3,
    noSpawn4,
    noSpawn5,
    noSpawn6,
    noSpawn7,
    noSpawn8
]

dots = []
for i in range(22, 438, 16):
    for j in range(22, 486, 16):
        dot = Dot(i, j)
        if dot.rect.collidelist(walls) is -1 and dot.rect.collidelist(noSpawns) is -1:
            dots.append(dot)
totalDots = len(dots)

pellet1 = Pellet(0.75, 1.75)
pellet2 = Pellet(0.75, 11.75)
pellet3 = Pellet(13.25, 1.75)
pellet4 = Pellet(13.25, 11.75)

pellets = [
    pellet1,
    pellet2,
    pellet3,
    pellet4
]

life1 = Life()
life1.rect = life1.image.get_rect(center=(16, LCD_HEIGHT - 16))

life2 = Life()
life2.rect = life2.image.get_rect(center=(48, LCD_HEIGHT - 16))

life3 = Life()
life3.rect = life3.image.get_rect(center=(80, LCD_HEIGHT - 16))

life_list = pygame.sprite.Group()
life_list.add(life1)
life_list.add(life2)
life_list.add(life3)

fruit = Fruit(0, 100)
fruit_list = pygame.sprite.Group()

fruit_timer = time.time()
canAddFruit = True

animStartTime = time.time()

grid = []
for i in range(0, 438, 16):
    for j in range(0, 486, 16):
        tile = Tile(i/32.0, j/32.0, 0.5, 0.5)
        grid.append(tile)

# Create Player
player = Player(grid)
player.rect.x = (GRID_SPRITE_WIDTH - 0.75) * SPRITE_PIXEL_SIZE
player.rect.y = (GRID_SPRITE_HEIGHT + 6.5) * SPRITE_PIXEL_SIZE
player_list = pygame.sprite.Group()
player_list.add(player)

# Create Ghosts
redGhost = Ghost(0, player, pygame.Rect(10.5*32, -0.5*32, 16, 16), grid, walls)
redGhost.rect.x = (GRID_SPRITE_WIDTH - 1) * SPRITE_PIXEL_SIZE
redGhost.rect.y = (GRID_SPRITE_HEIGHT - 5.5) * SPRITE_PIXEL_SIZE

pinkGhost = Ghost(1, player, pygame.Rect(2*32, -0.5*32, 16, 16), grid, walls)
pinkGhost.rect.x = (GRID_SPRITE_WIDTH - 3) * SPRITE_PIXEL_SIZE
pinkGhost.rect.y = (GRID_SPRITE_HEIGHT - 2.5) * SPRITE_PIXEL_SIZE

blueGhost = Ghost(2, player, pygame.Rect(12.5*32, 25*32, 16, 16), grid, walls)
blueGhost.rect.x = (GRID_SPRITE_WIDTH - 1) * SPRITE_PIXEL_SIZE
blueGhost.rect.y = (GRID_SPRITE_HEIGHT - 2.5) * SPRITE_PIXEL_SIZE

orangeGhost = Ghost(3, player, pygame.Rect(2*32, 25*32, 16, 16), grid, walls)
orangeGhost.rect.x = (GRID_SPRITE_WIDTH + 1) * SPRITE_PIXEL_SIZE
orangeGhost.rect.y = (GRID_SPRITE_HEIGHT - 2.5) * SPRITE_PIXEL_SIZE

ghost_list = pygame.sprite.Group()
ghost_list.add(redGhost)
ghost_list.add(pinkGhost)
ghost_list.add(blueGhost)
ghost_list.add(orangeGhost)

timer = pygame.time.get_ticks()
gamePhase = 1

scoreLabel = font.render("Score", True, (255, 255, 255))
animInterval = 0.5
livesLeft = 3

'''
    MAIN LOOP
'''
while running:

    display.fill((0, 0, 0))
    display.blit(screen, (0, 32))

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()
    
    if not player.lose and (len(dots) > 0 or len(pellets) > 0):
        player.move(key, walls, gameMode)
        player.checkGhostCollision(ghost_list)
        dots, pellets, fruit_list, isFrightened = player.eat(dots, pellets, fruit_list)

        if totalDots - len(dots) == 70 and canAddFruit == True:
            print("Add fruit")
            fruit_list.add(fruit)
            fruit_timer = time.time()
            canAddFruit = False
        elif totalDots - len(dots) == 170 and canAddFruit == True:
            print("Add fruit")
            fruit_list.add(fruit)
            fruit_timer = time.time()
            canAddFruit = False
        if len(fruit_list.sprites()) > 0 and time.time() - fruit_timer > 9:
            fruit_list.sprites()[0].kill()
            canAddFruit = True

        if isFrightened is True:
            gameMode = "Frightened"
            for ghost in ghost_list:
                ghost.status = "Frightened"
            timer = pygame.time.get_ticks()

        if player.lose:
            animInterval = 0.25
            if livesLeft is 3:
                life_list.remove(life3)
            elif livesLeft is 2:
                life_list.remove(life2)
            elif livesLeft is 1:
                life_list.remove(life1)
            livesLeft -= 1

        now = pygame.time.get_ticks()
        if gameMode == "Chase":
            if now - timer >= 20 * 1000 and gamePhase < 4:
                print("Scatter")
                gameMode = "Scatter"
                gamePhase += 1
                timer = now
        elif gameMode == "Scatter":
            if now - timer >= 7 * 1000 and gamePhase <= 2:
                print("Chase")
                gameMode = "Chase"
                timer = now
            elif now - timer >= 5 * 1000:
                print("Chase")
                gameMode = "Chase"
                timer = now
        else:
            if now - timer >= 6 * 1000:
                print("Chase")
                for ghost in ghost_list:
                    if ghost.status != "Eaten":
                        ghost.status = "Alive"
                gameMode = "Chase"
                timer = now

        if gameMode == "Chase":
            redGhost.move(player.rect, gameMode)
            pinkGhost.move(getPinkGhostTarget(player), gameMode)
            if totalDots - len(dots) >= 30:
                blueGhost.move(getBlueGhostTarget(player, redGhost), gameMode)
            if totalDots - len(dots) >= totalDots/3:
                orangeGhost.move(getOrangeGhostTarget(player, orangeGhost), gameMode)
        elif gameMode == "Scatter":
            redGhost.move(redGhost.scatterTargetRect, gameMode)
            pinkGhost.move(pinkGhost.scatterTargetRect, gameMode)
            if totalDots - len(dots) >= 30:
                blueGhost.move(blueGhost.scatterTargetRect, gameMode)
            if totalDots - len(dots) >= totalDots/3:
                orangeGhost.move(orangeGhost.scatterTargetRect, gameMode)
        elif gameMode == "Frightened":
            for ghost in ghost_list:
                ghost.moveRandom(now - timer)
    else:
        player.stop()
        for ghost in ghost_list:
            ghost.stop()
        if livesLeft == 0:
            finalText = font.render("You lose", True, (255, 255, 255))
            finalText_rect = finalText.get_rect()
            finalText_rect.center = (LCD_WIDTH/2, (LCD_HEIGHT/2) + 32)
            display.blit(finalText, finalText_rect)
        elif len(dots) == 0 and len(pellets) == 0:
            finalText = font.render("You win", True, (255, 255, 255))
            finalText_rect = finalText.get_rect()
            finalText_rect.center = (LCD_WIDTH/2, (LCD_HEIGHT/2) + 32)
            display.blit(finalText, finalText_rect)

    screen.fill((0, 0, 0))
    screen.blit(map, (0, 0))

    display.blit(scoreLabel, (LCD_WIDTH / 2, 0))
    scoreText = font.render(str(player.score), True, (255, 255, 255))
    scoreText_rect = scoreText.get_rect()
    scoreText_rect.top = 0
    scoreText_rect.right = LCD_WIDTH * 0.975
    display.blit(scoreText, scoreText_rect)

    if time.time() - animStartTime > animInterval:
        if player.lose is False:
            if player.image == player.images[0]:
                player.image = player.images[1]
            else:
                player.image = player.images[0]
        else:
            index = player.images.index(player.image)
            if index < len(player.images) - 1:
                player.image = player.images[index+1]
            elif livesLeft > 0:
                player.rect.x = (GRID_SPRITE_WIDTH - 0.75) * SPRITE_PIXEL_SIZE
                player.rect.y = (GRID_SPRITE_HEIGHT + 6.5) * SPRITE_PIXEL_SIZE
                player.images = player.rightImages
                player.currentDirection = 3
                animInterval = 0.5

                redGhost.rect.x = (GRID_SPRITE_WIDTH - 1) * SPRITE_PIXEL_SIZE
                redGhost.rect.y = (GRID_SPRITE_HEIGHT - 5.5) * SPRITE_PIXEL_SIZE
                redGhost.image = redGhost.rightImage
                redGhost.currentDirection = 3

                pinkGhost.rect.x = (GRID_SPRITE_WIDTH - 3) * SPRITE_PIXEL_SIZE
                pinkGhost.rect.y = (GRID_SPRITE_HEIGHT - 2.5) * SPRITE_PIXEL_SIZE
                pinkGhost.image = pinkGhost.rightImage
                pinkGhost.currentDirection = 3
                pinkGhost.reachedInit = False

                blueGhost.rect.x = (GRID_SPRITE_WIDTH - 1) * SPRITE_PIXEL_SIZE
                blueGhost.rect.y = (GRID_SPRITE_HEIGHT - 2.5) * SPRITE_PIXEL_SIZE
                blueGhost.image = blueGhost.rightImage
                blueGhost.currentDirection = 3
                blueGhost.reachedInit = False

                orangeGhost.rect.x = (GRID_SPRITE_WIDTH + 1) * SPRITE_PIXEL_SIZE
                orangeGhost.rect.y = (GRID_SPRITE_HEIGHT - 2.5) * SPRITE_PIXEL_SIZE
                orangeGhost.image = orangeGhost.rightImage
                orangeGhost.currentDirection = 3
                orangeGhost.reachedInit = False

                player.lose = False
        animStartTime = time.time()
    player.update()
    redGhost.update()
    pinkGhost.update()
    blueGhost.update()
    orangeGhost.update()

    for dot in dots:
        dot.draw(screen)

    for pellet in pellets:
        pellet.draw(screen)

    player_list.draw(screen)
    ghost_list.draw(screen)
    fruit_list.draw(screen)
    life_list.draw(display)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)


# Done! Time to quit.
pygame.quit()