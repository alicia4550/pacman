import pygame

from util import *
from joystick import *

class Player(pygame.sprite.Sprite):
    def __init__(self, startX, startY, grid):
        pygame.sprite.Sprite.__init__(self)

        spritesheet = pygame.image.load('Arcade - Pac-Man - General Sprites.png').convert_alpha()

        img_0 = get_image(spritesheet, 28.5+1.9, 0, SPRITE_PIXEL_SIZE-1, SPRITE_PIXEL_SIZE-1, True)
        img_1 = get_image(spritesheet, 29.5+2.0, 0, SPRITE_PIXEL_SIZE-1, SPRITE_PIXEL_SIZE-1, True)
        img_2 = get_image(spritesheet, 28.5+1.9, 1+0.13, SPRITE_PIXEL_SIZE-1, SPRITE_PIXEL_SIZE-1, True)
        img_3 = get_image(spritesheet, 29.5+2.0, 1+0.13, SPRITE_PIXEL_SIZE-1, SPRITE_PIXEL_SIZE-1, True)
        img_4 = get_image(spritesheet, 28.5+1.9, 2+0.26, SPRITE_PIXEL_SIZE-1, SPRITE_PIXEL_SIZE-1, True)
        img_5 = get_image(spritesheet, 29.5+2.0, 2+0.26, SPRITE_PIXEL_SIZE-1, SPRITE_PIXEL_SIZE-1, True)
        img_6 = get_image(spritesheet, 28.5+1.9, 3+0.26, SPRITE_PIXEL_SIZE-1, SPRITE_PIXEL_SIZE-1, True)
        img_7 = get_image(spritesheet, 29.5+2.0, 3+0.26, SPRITE_PIXEL_SIZE-1, SPRITE_PIXEL_SIZE-1, True)

        img_8 = get_image(spritesheet, 30.5+2.1, 0, SPRITE_PIXEL_SIZE-1, SPRITE_PIXEL_SIZE-1, True)
        img_9 = get_image(spritesheet, 31.5+2.15, 0, SPRITE_PIXEL_SIZE-1, SPRITE_PIXEL_SIZE-1, True)
        img_10 = get_image(spritesheet, 32.5+2.2, 0, SPRITE_PIXEL_SIZE-1, SPRITE_PIXEL_SIZE-1, True)
        img_11 = get_image(spritesheet, 33.5+2.25, 0, SPRITE_PIXEL_SIZE-1, SPRITE_PIXEL_SIZE-1, True)
        img_12 = get_image(spritesheet, 34.5+2.3, 0, SPRITE_PIXEL_SIZE-1, SPRITE_PIXEL_SIZE-1, True)
        img_13 = get_image(spritesheet, 35.5+2.35, 0, SPRITE_PIXEL_SIZE-1, SPRITE_PIXEL_SIZE-1, True)
        img_14 = get_image(spritesheet, 36.5+2.4, 0, SPRITE_PIXEL_SIZE-1, SPRITE_PIXEL_SIZE-1, True)
        img_15 = get_image(spritesheet, 37.5+2.45, 0, SPRITE_PIXEL_SIZE-1, SPRITE_PIXEL_SIZE-1, True)
        img_16 = get_image(spritesheet, 38.5+2.5, 0, SPRITE_PIXEL_SIZE-1, SPRITE_PIXEL_SIZE-1, True)
        img_17 = get_image(spritesheet, 39.5+2.55, 0, SPRITE_PIXEL_SIZE-1, SPRITE_PIXEL_SIZE-1, True)
        img_18 = get_image(spritesheet, 40.5+2.6, 0, SPRITE_PIXEL_SIZE-1, SPRITE_PIXEL_SIZE-1, True)
        img_19 = get_image(spritesheet, 41.5+2.65, 0+0.13, SPRITE_PIXEL_SIZE-1, SPRITE_PIXEL_SIZE-1, True)
        img_20 = get_image(spritesheet, 41.5+2.65, 1+0.13, SPRITE_PIXEL_SIZE-1, SPRITE_PIXEL_SIZE-1, True)


        self.rightImages = [img_0, img_1]
        self.leftImages = [img_2, img_3]
        self.upImages = [img_4, img_5]
        self.downImages = [img_6, img_7]
        self.loseImages = [img_8, img_9, img_10, img_11, img_12, img_13, img_14, img_15, img_16, img_17, img_18, img_19, img_20]

        self.images = self.rightImages
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.movex = 0
        self.movey = 0
        self.frame = 0

        self.speed = 0.8
        self.frightenedSpeed = 0.9

        self.xActual = self.rect.x
        self.yActual = self.rect.y

        self.score = 0
        self.tileNumber = 0
        self.currentDirection = 3
        self.lose = False

        self.ghostsEaten = 0

        self.grid = grid

        self.startX = startX
        self.startY = startY
        self.setX(startX)
        self.setY(startY)

    def redrawLevel(self, speed, frightenedSpeed):
        self.setX(self.startX)
        self.setY(self.startY)
        self.ghostsEaten = 0
        self.currentDirection = 3
        self.images = self.rightImages
        self.image = self.images[0]
        self.speed = speed
        self.frightenedSpeed = frightenedSpeed

    def setX(self, x):
        self.rect.x = x
        self.xActual = x
    
    def setY(self, y):
        self.rect.y = y
        self.yActual = y

    def move(self, key, walls, gameMode):
        if gameMode == "Frightened":
            steps = self.frightenedSpeed
        else:
            steps = self.speed
        steps = 1
        if key[pygame.K_LEFT] or getDirection() == "LEFT":
            rect = pygame.Rect(self.rect.x - 1, self.rect.y, self.rect.width, self.rect.height)
            if rect.collidelist(walls) == -1:
                self.images = self.leftImages
                self.control(-steps, 0)
                self.currentDirection = 1
            else:
                self.stop()
        elif key[pygame.K_RIGHT] or getDirection() == "RIGHT":
            rect = pygame.Rect(self.rect.x + 1, self.rect.y, self.rect.width, self.rect.height)
            if rect.collidelist(walls) == -1:
                self.images = self.rightImages
                self.control(steps, 0)
                self.currentDirection = 3
            else:
                self.stop()
        elif key[pygame.K_UP] or getDirection() == "UP":
            rect = pygame.Rect(self.rect.x, self.rect.y - 1, self.rect.width, self.rect.height)
            if rect.collidelist(walls) == -1:
                self.images = self.upImages
                self.control(0, -steps)
                self.currentDirection = 0
            else:
                self.stop()
        elif key[pygame.K_DOWN] or getDirection() == "DOWN":
            rect = pygame.Rect(self.rect.x, self.rect.y + 1, self.rect.width, self.rect.height)
            if rect.collidelist(walls) == -1:
                self.images = self.downImages
                self.control(0, steps)
                self.currentDirection = 2
            else:
                self.stop()
        else:
            self.stop()
        self.tileNumber = self.rect.collidelist(self.grid)

    def eat(self, dots, pellets, fruits):
        isFrightened = False
        if self.rect.collidelist(dots) != -1:
            index = self.rect.collidelist(dots)
            dots.pop(index)
            self.score += 10
        if self.rect.collidelist(pellets) != -1:
            print("Frightened")
            index = self.rect.collidelist(pellets)
            pellets.pop(index)
            self.score += 50
            isFrightened = True
        if len(fruits.sprites()) > 0 and self.rect.colliderect(fruits.sprites()[0].rect) == True:
            print("Eat fruit")
            fruit = fruits.sprites()[0]
            self.score += fruit.points
            fruit.kill()
        return dots, pellets, fruits, isFrightened

    def checkGhostCollision(self, ghost_list):
        for ghost in ghost_list:
            if self.tileNumber == ghost.tileNumber:
                if ghost.status == "Alive":
                    self.lose = True
                    self.images = self.loseImages
                    self.image = self.images[0]
                elif ghost.status == "Frightened":
                    print("Eaten")
                    self.ghostsEaten += 1
                    ghost.status = "Eaten"
                    self.score += int(math.pow(2, self.ghostsEaten) * 100)

    def control(self, x, y):
        self.movex = x
        self.movey = y
    
    def stop(self):
        self.movex = 0
        self.movey = 0

    def update(self):
        self.xActual += self.movex
        self.yActual += self.movey

        self.rect.x = round(self.xActual)
        self.rect.y = round(self.yActual)

        if self.rect.x > 425:
            self.rect.x = 0
            self.xActual = 0
        elif self.rect.x < 0:
            self.rect.x = 425
            self.xActual = 425
