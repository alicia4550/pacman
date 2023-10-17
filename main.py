import pygame
import time
import math
import random

pygame.init()
font = pygame.font.Font("Retro Gaming.ttf", 26)

'''
    CONSTANTS
'''
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SPRITE_PIXEL_SIZE = 16
GRID_SPRITE_WIDTH = 14
GRID_SPRITE_HEIGHT = 16

# 4:5 aspect ratio
LCD_WIDTH = 448 # 550
LCD_HEIGHT =  560 # 728

FPS = 40

'''
    OBJECTS
'''
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

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

        self.score = 0
        self.tileNumber = 0
        self.currentDirection = 3
        self.lose = False

    def move(self, key):
        if gameMode == "Frightened":
            steps = self.frightenedSpeed
        else:
            steps = self.speed
        steps = 1
        if key[pygame.K_LEFT]:
            rect = pygame.Rect(self.rect.x - 1, self.rect.y, self.rect.width, self.rect.height)
            if rect.collidelist(walls) is -1:
                self.images = self.leftImages
                self.control(-steps, 0)
                self.currentDirection = 1
            else:
                self.stop()
        elif key[pygame.K_RIGHT]:
            rect = pygame.Rect(self.rect.x + 1, self.rect.y, self.rect.width, self.rect.height)
            if rect.collidelist(walls) is -1:
                self.images = self.rightImages
                self.control(steps, 0)
                self.currentDirection = 3
            else:
                self.stop()
        elif key[pygame.K_UP]:
            rect = pygame.Rect(self.rect.x, self.rect.y - 1, self.rect.width, self.rect.height)
            if rect.collidelist(walls) is -1:
                self.images = self.upImages
                self.control(0, -steps)
                self.currentDirection = 0
            else:
                self.stop()
        elif key[pygame.K_DOWN]:
            rect = pygame.Rect(self.rect.x, self.rect.y + 1, self.rect.width, self.rect.height)
            if rect.collidelist(walls) is -1:
                self.images = self.downImages
                self.control(0, steps)
                self.currentDirection = 2
            else:
                self.stop()
        else:
            self.stop()
        self.tileNumber = self.rect.collidelist(grid)

    def eat(self):
        if self.rect.collidelist(dots) is not -1:
            index = self.rect.collidelist(dots)
            dots.pop(index)
            self.score += 10
            # print(self.score)
        if self.rect.collidelist(pellets) is not -1:
            print("Frightened")
            global gameMode, timer
            gameMode = "Frightened"
            timer = pygame.time.get_ticks()
            index = self.rect.collidelist(pellets)
            pellets.pop(index)
            self.score += 50
            # print(self.score)

    def checkGhostCollision(self):
        for ghost in ghost_list:
            # if self.rect.colliderect(ghost.rect):
            if self.tileNumber == ghost.tileNumber:
                self.lose = True
                self.images = self.loseImages
                self.image = self.images[0]

    def control(self, x, y):
        self.movex = x
        self.movey = y
    
    def stop(self):
        self.movex = 0
        self.movey = 0

    def update(self):
        self.rect.x = self.rect.x + self.movex 
        self.rect.y = self.rect.y + self.movey

        if self.rect.x > 425:
            self.rect.x = 0
        elif self.rect.x < 0:
            self.rect.x = 425

class Ghost(pygame.sprite.Sprite):
    def __init__(self, yOffset, scatterTargetRect):
        pygame.sprite.Sprite.__init__(self)

        self.rightImage = get_image(spritesheet, 28.5, 4+yOffset, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        self.leftImage = get_image(spritesheet, 30.5, 4+yOffset, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        self.upImage = get_image(spritesheet, 32.5, 4+yOffset, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        self.downImage = get_image(spritesheet, 34.5, 4+yOffset, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        self.frightenedImage = get_image(spritesheet, 36.5, 4, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        self.image = self.rightImage

        self.rect = self.image.get_rect()
        self.movex = 0
        self.movey = 0
        self.targetRect = player.rect
        self.scatterTargetRect = scatterTargetRect
        self.movementMode = "Chase"

        self.speed = 0.75
        self.frightenedSpeed = 0.5

        self.tileNumber = 0
        self.currentDirection = 3

        self.reachedInit = False
        self.initX = (GRID_SPRITE_WIDTH - 1) * SPRITE_PIXEL_SIZE
        self.initY = (GRID_SPRITE_HEIGHT - 5.5) * SPRITE_PIXEL_SIZE

    def move(self, targetRect):
        if not self.reachedInit:
            if abs(self.initX - self.rect.x) < 10 and abs(self.initY - self.rect.y) < 0.5:
                self.reachedInit = True
            self.control((self.initX - self.rect.x)/10, (self.initY - self.rect.y)/100)
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
                            self.pickDirection(dir, priority)
                        elif vector[1] > 0:
                            priority = [2, 1, 3, 0]
                            self.pickDirection(dir, priority)
                        else:
                            self.stop()
                    elif vector[1] == 0:
                        if vector[0] < 0:
                            priority = [1, 0, 2, 3]
                            self.pickDirection(dir, priority)
                        elif vector[0] > 0:
                            priority = [3, 0, 2, 1]
                            self.pickDirection(dir, priority)
                        else:
                            self.stop()
                    elif vector[0] < 0:
                        if vector[1] < 0:
                            if abs(vector[1]/vector[0]) < 1:
                                priority = [1, 0, 2, 3]
                                self.pickDirection(dir, priority)
                            else:
                                priority = [0, 1, 3, 2]
                                self.pickDirection(dir, priority)
                        else:
                            if abs(vector[1]/vector[0]) < 1:
                                priority = [1, 2, 0, 3]
                                self.pickDirection(dir, priority)
                            else:
                                priority = [2, 1, 3, 0]
                                self.pickDirection(dir, priority)
                    else:
                        if vector[1] < 0:
                            if abs(vector[1]/vector[0]) < 1:
                                priority = [3, 0, 2, 1]
                                self.pickDirection(dir, priority)
                            else:
                                priority = [0, 3, 1, 2]
                                self.pickDirection(dir, priority)
                        else:
                            if abs(vector[1]/vector[0]) < 1:
                                priority = [3, 2, 0, 1]
                                self.pickDirection(dir, priority)
                            else:
                                priority = [2, 3, 1, 0]
                                self.pickDirection(dir, priority)
            else:
                self.moveDirection(self.currentDirection)
        self.tileNumber = self.rect.collidelist(grid)

    def moveRandom(self):
        if (self.rect.x - 8) % 16 == 0 and (self.rect.y - 8) % 16 == 0:
            self.stop()
            dir = self.getPossibleDirections()
            self.moveDirection(random.choice(dir))
    
    def control(self, x, y):
        self.movex = x
        self.movey = y
    
    def stop(self):
        self.movex = 0
        self.movey = 0

    def update(self):
        self.rect.x = self.rect.x + self.movex 
        self.rect.y = self.rect.y + self.movey

        # print(self.rect.x)
        if self.rect.x > 435:
            self.rect.x = 0
        elif self.rect.x < 0:
            self.rect.x = 420
    
    def findVector(self):
        x1 = self.rect.x
        y1 = self.rect.y
        x2 = self.targetRect.x
        y2 = self.targetRect.y

        return [x2 - x1, y2 - y1]
    
    def pickDirection(self, dir, priority):
        for i in priority:
            if i in dir:
                if (i + self.currentDirection) % 2 == 0 and i is not self.currentDirection and (gameMode == "Scatter" or self.movementMode == "Scatter"):
                    continue
                self.moveDirection(i)
                return
        self.stop()

    def moveDirection(self, dir):
        if gameMode == "Frightened":
            steps = self.frightenedSpeed
        else:
            steps = self.speed
        steps = 1
        if dir is 1:
            self.image = self.leftImage
            self.control(-steps, 0)
            self.currentDirection = 1
        elif dir is 3:
            self.image = self.rightImage
            self.control(steps, 0)
            self.currentDirection = 3
        elif dir is 0:
            self.image = self.upImage
            self.control(0, -steps)
            self.currentDirection = 0
        elif dir is 2:
            self.image = self.downImage
            self.control(0, steps)
            self.currentDirection = 2
        else:
            self.stop()
        if gameMode == "Frightened":
            self.image = self.frightenedImage
        

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
        if grid[(x * 31) + (y - 1)].rect.collidelist(walls) is -1:
            dir.append(0)
        if x - 1 < 0:
            return [1]
        if grid[((x - 1) * 31) + y].rect.collidelist(walls) is -1:
            dir.append(1)
        if grid[(x * 31) + (y + 1)].rect.collidelist(walls) is -1:
            dir.append(2)
        if x + 1 >= 28:
            return [3]
        if grid[((x + 1) * 31) + y].rect.collidelist(walls) is -1:
            dir.append(3)
        return dir


class Wall(object):
    def __init__(self, x, y, width, height):
        self.x = (x * 32)
        self.y = (y * 32)
        self.width = (width * 32)
        self.height = (height * 32)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 255), self.rect, 2)

class Tile(object):
    def __init__(self, x, y, width, height):
        self.x = (x * 32)
        self.y = (y * 32)
        self.width = (width * 32)
        self.height = (height * 32)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 0), self.rect, 2)

class Dot(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 4.5, 4.5)
    def draw(self, win):
        pygame.draw.rect(win, (255, 183, 174), self.rect, 2)

class Pellet(object):
    def __init__(self, x, y):
        self.x = (x * 32)
        self.y = (y * 32)
        self.rect = pygame.Rect(self.x, self.y, 16, 16)
    def draw(self, win):
        pygame.draw.circle(win, (255, 183, 174), (self.x, self.y), 8)

class Life(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image(spritesheet, 36.5, 1, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        self.rect = self.image.get_rect()

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

# Create Player
player = Player()
player.rect.x = (GRID_SPRITE_WIDTH - 0.75) * SPRITE_PIXEL_SIZE
player.rect.y = (GRID_SPRITE_HEIGHT + 6.5) * SPRITE_PIXEL_SIZE
player_list = pygame.sprite.Group()
player_list.add(player)
# steps = 1

# Create Ghosts
redGhost = Ghost(0, pygame.Rect(10.5*32, -0.5*32, 16, 16))
redGhost.rect.x = (GRID_SPRITE_WIDTH - 1) * SPRITE_PIXEL_SIZE
redGhost.rect.y = (GRID_SPRITE_HEIGHT - 5.5) * SPRITE_PIXEL_SIZE

pinkGhost = Ghost(1, pygame.Rect(2*32, -0.5*32, 16, 16))
pinkGhost.rect.x = (GRID_SPRITE_WIDTH - 3) * SPRITE_PIXEL_SIZE
pinkGhost.rect.y = (GRID_SPRITE_HEIGHT - 2.5) * SPRITE_PIXEL_SIZE

blueGhost = Ghost(2, pygame.Rect(12.5*32, 25*32, 16, 16))
blueGhost.rect.x = (GRID_SPRITE_WIDTH - 1) * SPRITE_PIXEL_SIZE
blueGhost.rect.y = (GRID_SPRITE_HEIGHT - 2.5) * SPRITE_PIXEL_SIZE

orangeGhost = Ghost(3, pygame.Rect(2*32, 25*32, 16, 16))
orangeGhost.rect.x = (GRID_SPRITE_WIDTH + 1) * SPRITE_PIXEL_SIZE
orangeGhost.rect.y = (GRID_SPRITE_HEIGHT - 2.5) * SPRITE_PIXEL_SIZE

ghost_list = pygame.sprite.Group()
ghost_list.add(redGhost)
ghost_list.add(pinkGhost)
ghost_list.add(blueGhost)
ghost_list.add(orangeGhost)

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

animStartTime = time.time()

grid = []
for i in range(0, 438, 16):
    for j in range(0, 486, 16):
        tile = Tile(i/32.0, j/32.0, 0.5, 0.5)
        grid.append(tile)

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
        player.move(key)
        player.eat()
        player.checkGhostCollision()

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
                gameMode = "Chase"
                timer = now

        if gameMode == "Chase":
            redGhost.move(player.rect)
            pinkGhost.move(getPinkGhostTarget(player))
            if totalDots - len(dots) >= 30:
                blueGhost.move(getBlueGhostTarget(player, redGhost))
            if totalDots - len(dots) >= totalDots/3:
                orangeGhost.move(getOrangeGhostTarget(player, orangeGhost))
        elif gameMode == "Scatter":
            redGhost.move(redGhost.scatterTargetRect)
            pinkGhost.move(pinkGhost.scatterTargetRect)
            if totalDots - len(dots) >= 30:
                blueGhost.move(blueGhost.scatterTargetRect)
            if totalDots - len(dots) >= totalDots/3:
                orangeGhost.move(orangeGhost.scatterTargetRect)
        elif gameMode == "Frightened":
            for ghost in ghost_list:
                ghost.moveRandom()
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
    scoreText_rect.right = LCD_WIDTH * 0.925
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
                redGhost.currentDirection = 3

                pinkGhost.rect.x = (GRID_SPRITE_WIDTH - 3) * SPRITE_PIXEL_SIZE
                pinkGhost.rect.y = (GRID_SPRITE_HEIGHT - 2.5) * SPRITE_PIXEL_SIZE
                pinkGhost.currentDirection = 3
                pinkGhost.reachedInit = False

                blueGhost.rect.x = (GRID_SPRITE_WIDTH - 1) * SPRITE_PIXEL_SIZE
                blueGhost.rect.y = (GRID_SPRITE_HEIGHT - 2.5) * SPRITE_PIXEL_SIZE
                blueGhost.currentDirection = 3
                blueGhost.reachedInit = False

                orangeGhost.rect.x = (GRID_SPRITE_WIDTH + 1) * SPRITE_PIXEL_SIZE
                orangeGhost.rect.y = (GRID_SPRITE_HEIGHT - 2.5) * SPRITE_PIXEL_SIZE
                orangeGhost.currentDirection = 3
                orangeGhost.reachedInit = False

                player.lose = False
        animStartTime = time.time()
    player.update()
    redGhost.update()
    pinkGhost.update()
    blueGhost.update()
    orangeGhost.update()

    # for tile in grid:
    #     tile.draw(screen)

    # for wall in walls:
    #     wall.draw(screen)

    for dot in dots:
        dot.draw(screen)

    for pellet in pellets:
        pellet.draw(screen)

    player_list.draw(screen)
    ghost_list.draw(screen)
    life_list.draw(display)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)


# Done! Time to quit.
pygame.quit()