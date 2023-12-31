import pygame
import math
import random

from util import *

class Ghost(pygame.sprite.Sprite):
    def __init__(self, yOffset, startX, startY, player, scatterTargetRect, grid, walls):
        pygame.sprite.Sprite.__init__(self)

        spritesheet = pygame.image.load('Arcade - Pac-Man - General Sprites.png').convert_alpha()

        self.rightImage = get_image(spritesheet, 28.5, 4+yOffset, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        self.leftImage = get_image(spritesheet, 30.5, 4+yOffset, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        self.upImage = get_image(spritesheet, 32.5, 4+yOffset, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        self.downImage = get_image(spritesheet, 34.5, 4+yOffset, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        
        self.frightenedBlueImage = get_image(spritesheet, 36.5, 4, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        self.frightenedWhiteImage = get_image(spritesheet, 38.5, 4, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        self.eyesRightImage = get_image(spritesheet, 36.5, 5, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        self.eyesLeftImage = get_image(spritesheet, 37.5, 5, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        self.eyesUpImage = get_image(spritesheet, 38.5, 5, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        self.eyesDownImage = get_image(spritesheet, 39.5, 5, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        self.status = "Alive"
        
        self.image = self.rightImage

        self.rect = self.image.get_rect()
        self.movex = 0
        self.movey = 0
        self.targetRect = player.rect
        self.scatterTargetRect = scatterTargetRect
        self.movementMode = "Chase"

        self.speed = 0.75
        self.frightenedSpeed = 0.5

        self.xActual = self.rect.x
        self.yActual = self.rect.y

        self.tileNumber = 0
        self.currentDirection = 3

        self.reachedHome = False
        self.reachedInit = False
        self.initX = (GRID_SPRITE_WIDTH - 1) * SPRITE_PIXEL_SIZE
        self.initY = (GRID_SPRITE_HEIGHT - 5.5) * SPRITE_PIXEL_SIZE

        self.grid = grid
        self.walls = walls

        self.startX = startX
        self.startY = startY
        self.setX(startX)
        self.setY(startY)

    def redrawLevel(self, speed, frightenedSpeed):
        self.setX(self.startX)
        self.setY(self.startY)
        self.reachedHome = False
        self.reachedInit = False
        self.speed = speed
        self.frightenedSpeed = frightenedSpeed
        self.currentDirection = 3

    def setX(self, x):
        self.rect.x = x
        self.xActual = x
    
    def setY(self, y):
        self.rect.y = y
        self.yActual = y

    def move(self, targetRect, gameMode):
        if not self.reachedInit:
            if abs(self.initX - self.rect.x) < 10 and abs(self.initY - self.rect.y) < 0.5:
                self.reachedInit = True
            self.control((self.initX - self.rect.x)/10, (self.initY - self.rect.y)/10)
        else:
            if self.status == "Eaten":
                if self.reachedHome is False:
                    self.targetRect = pygame.Rect(self.initX, self.initY, 16, 16)
                    if abs(self.initX - self.rect.x) < 10 and abs(self.initY - self.rect.y) < 0.5:
                        self.reachedHome = True
                        return
                else:
                    if abs(self.initX - self.rect.x) < 10 and abs(self.initY + 32 - self.rect.y) < 0.5:
                        self.reachedInit = False
                        self.reachedHome = False
                        self.status = "Alive"
                        self.image = self.upImage
                    else:
                        self.control(0, 1)
                        return
            
            else:
                self.targetRect = targetRect
            if (self.rect.x - 8) % 16 == 0 and (self.rect.y - 8) % 16 == 0:
                self.stop()
                dir = self.getPossibleDirections()
                if len(dir) is 0:
                    print(dir)
                    self.stop()
                elif len(dir) is 1:
                    self.moveDirection(dir[0])
                elif len(dir) is 2:
                    if self.currentDirection in dir:
                        self.moveDirection(self.currentDirection)
                    else:
                        if (dir[0] + self.currentDirection) % 2 is 0:
                            self.moveDirection(dir[1])
                        else:
                            self.moveDirection(dir[0])
                else:
                    vector = self.findVector()
                    if vector[0] == 0:
                        if vector[1] < 0:
                            priority = [0, 1, 3, 2]
                            self.pickDirection(dir, priority, gameMode)
                        elif vector[1] > 0:
                            priority = [2, 1, 3, 0]
                            self.pickDirection(dir, priority, gameMode)
                        else:
                            self.stop()
                    elif vector[1] == 0:
                        if vector[0] < 0:
                            priority = [1, 0, 2, 3]
                            self.pickDirection(dir, priority, gameMode)
                        elif vector[0] > 0:
                            priority = [3, 0, 2, 1]
                            self.pickDirection(dir, priority, gameMode)
                        else:
                            self.stop()
                    elif vector[0] < 0:
                        if vector[1] < 0:
                            if abs(vector[1]/vector[0]) < 1:
                                priority = [1, 0, 2, 3]
                                self.pickDirection(dir, priority, gameMode)
                            else:
                                priority = [0, 1, 3, 2]
                                self.pickDirection(dir, priority, gameMode)
                        else:
                            if abs(vector[1]/vector[0]) < 1:
                                priority = [1, 2, 0, 3]
                                self.pickDirection(dir, priority, gameMode)
                            else:
                                priority = [2, 1, 3, 0]
                                self.pickDirection(dir, priority, gameMode)
                    else:
                        if vector[1] < 0:
                            if abs(vector[1]/vector[0]) < 1:
                                priority = [3, 0, 2, 1]
                                self.pickDirection(dir, priority, gameMode)
                            else:
                                priority = [0, 3, 1, 2]
                                self.pickDirection(dir, priority, gameMode)
                        else:
                            if abs(vector[1]/vector[0]) < 1:
                                priority = [3, 2, 0, 1]
                                self.pickDirection(dir, priority, gameMode)
                            else:
                                priority = [2, 3, 1, 0]
                                self.pickDirection(dir, priority, gameMode)
            else:
                self.moveDirection(self.currentDirection)

    def moveRandom(self, frightenedTime):
        if (self.rect.x - 8) % 16 == 0 and (self.rect.y - 8) % 16 == 0:
            self.stop()
            dir = self.getPossibleDirections()
            newDir = random.choice(dir)
            while (newDir + self.currentDirection) % 2 == 0 and newDir != self.currentDirection:
                newDir = random.choice(dir)
            self.moveDirection(newDir, frightenedTime)
    
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

        if self.rect.x > 435:
            self.rect.x = 0
            self.xActual = 0
        elif self.rect.x < 0:
            self.rect.x = 420
            self.xActual = 420

        self.tileNumber = self.rect.collidelist(self.grid)
    
    def findVector(self):
        x1 = self.rect.x
        y1 = self.rect.y
        x2 = self.targetRect.x
        y2 = self.targetRect.y

        return [x2 - x1, y2 - y1]
    
    def pickDirection(self, dir, priority, gameMode):
        for i in priority:
            if i in dir:
                if (i + self.currentDirection) % 2 == 0 and i is not self.currentDirection and (gameMode == "Scatter" or self.movementMode == "Scatter"):
                    continue
                self.moveDirection(i)
                return
        self.stop()

    def moveDirection(self, dir, frightenedTime=-1):
        if frightenedTime > 0:
            steps = self.frightenedSpeed
        else:
            steps = self.speed

        if dir is 1:
            if self.status == "Alive":
                self.image = self.leftImage
            elif self.status == "Frightened":
                if frightenedTime < 4 * 1000:
                    self.image = self.frightenedBlueImage
                else:
                    self.image = self.frightenedWhiteImage
            elif self.status == "Eaten":
                self.image = self.eyesLeftImage
            self.control(-steps, 0)
            self.currentDirection = 1
        elif dir is 3:
            if self.status == "Alive":
                self.image = self.rightImage
            elif self.status == "Frightened":
                if frightenedTime < 4 * 1000:
                    self.image = self.frightenedBlueImage
                else:
                    self.image = self.frightenedWhiteImage
            elif self.status == "Eaten":
                self.image = self.eyesRightImage
            self.control(steps, 0)
            self.currentDirection = 3
        elif dir is 0:
            if self.status == "Alive":
                self.image = self.upImage
            elif self.status == "Frightened":
                if frightenedTime < 4 * 1000:
                    self.image = self.frightenedBlueImage
                else:
                    self.image = self.frightenedWhiteImage
            elif self.status == "Eaten":
                self.image = self.eyesUpImage
            self.control(0, -steps)
            self.currentDirection = 0
        elif dir is 2:
            if self.status == "Alive":
                self.image = self.downImage
            elif self.status == "Frightened":
                if frightenedTime < 4 * 1000:
                    self.image = self.frightenedBlueImage
                else:
                    self.image = self.frightenedWhiteImage
            elif self.status == "Eaten":
                self.image = self.eyesDownImage
            self.control(0, steps)
            self.currentDirection = 2
        else:
            self.stop()
        

    def getPossibleDirections(self):
        x = 0
        y = 0
        if self.rect.x % 16 < 8:
            x = math.floor((self.rect.x - 8) / 16.0) + 1
        else:
            x = math.ceil((self.rect.x - 8) / 16.0) + 1
        if x >= 27:
            x = 27
        if self.rect.y % 16 < 8:
            y = math.floor((self.rect.y - 8) / 16.0) + 1
        else:
            y = math.ceil((self.rect.y - 8) / 16.0) + 1
        
        dir = [] # 0 = up, 1 = left, 2 = right, 3 = down
        if self.grid[(x * 31) + (y - 1)].rect.collidelist(self.walls) is -1:
            dir.append(0)
        if x - 1 < 0:
            return [1]
        if self.grid[((x - 1) * 31) + y].rect.collidelist(self.walls) is -1:
            dir.append(1)
        if self.grid[(x * 31) + (y + 1)].rect.collidelist(self.walls) is -1:
            dir.append(2)
        if x + 1 >= 28:
            return [3]
        if self.grid[((x + 1) * 31) + y].rect.collidelist(self.walls) is -1:
            dir.append(3)
        return dir