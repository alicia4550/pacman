import pygame
import time
pygame.init()

'''
    CONSTANTS
'''
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500
SPRITE_PIXEL_SIZE = 16
GRID_SPRITE_WIDTH = 14
GRID_SPRITE_HEIGHT = 16

FPS = 40

'''
    OBJECTS
'''
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        img_0 = get_image(spritesheet, 28.5, 0, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        img_1 = get_image(spritesheet, 29.5, 0, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        img_2 = get_image(spritesheet, 28.5, 1, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        img_3 = get_image(spritesheet, 29.5, 1, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        img_4 = get_image(spritesheet, 28.5, 2, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        img_5 = get_image(spritesheet, 29.5, 2, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        img_6 = get_image(spritesheet, 28.5, 3, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        img_7 = get_image(spritesheet, 29.5, 3, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)

        self.rightImages = [img_0, img_1]
        self.leftImages = [img_2, img_3]
        self.upImages = [img_4, img_5]
        self.downImages = [img_6, img_7]

        self.images = self.rightImages
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.movex = 0
        self.movey = 0
        self.frame = 0

        self.score = 0

    def move(self, key):
        if key[pygame.K_LEFT]:
            rect = pygame.Rect(self.rect.x - 1, self.rect.y, self.rect.width, self.rect.height)
            if rect.collidelist(walls) is -1:
                self.images = self.leftImages
                self.control(-steps, 0)
            else:
                self.stop()
            # print('left')
        elif key[pygame.K_RIGHT]:
            rect = pygame.Rect(self.rect.x + 1, self.rect.y, self.rect.width, self.rect.height)
            if rect.collidelist(walls) is -1:
                self.images = self.rightImages
                self.control(steps, 0)
            else:
                self.stop()
            # print('right')
        elif key[pygame.K_UP]:
            rect = pygame.Rect(self.rect.x, self.rect.y - 1, self.rect.width, self.rect.height)
            if rect.collidelist(walls) is -1:
                self.images = self.upImages
                self.control(0, -steps)
            else:
                self.stop()
            # print('up')
        elif key[pygame.K_DOWN]:
            rect = pygame.Rect(self.rect.x, self.rect.y + 1, self.rect.width, self.rect.height)
            if rect.collidelist(walls) is -1:
                self.images = self.downImages
                self.control(0, steps)
            else:
                self.stop()
            # print('down')
        else:
            self.stop()

    def eat(self):
        if self.rect.collidelist(dots) is not -1:
            index = self.rect.collidelist(dots)
            dots.pop(index)
            self.score += 10
            print(self.score)
        if self.rect.collidelist(pellets) is not -1:
            index = self.rect.collidelist(pellets)
            pellets.pop(index)
            self.score += 50
            print(self.score)

    def control(self, x, y):
        self.movex = x
        self.movey = y
    
    def stop(self):
        self.movex = 0
        self.movey = 0

    def update(self):
        self.rect.x = self.rect.x + self.movex 
        self.rect.y = self.rect.y + self.movey

class Wall(object):
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

'''
    SET UP
'''
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

spritesheet = pygame.image.load('Arcade - Pac-Man - General Sprites.png').convert_alpha()

running = True

clock = pygame.time.Clock()

# Create background
screen.fill((50, 50, 50))
map = get_image(spritesheet, 1.02, 0, SPRITE_PIXEL_SIZE*GRID_SPRITE_WIDTH, SPRITE_PIXEL_SIZE*GRID_SPRITE_HEIGHT, False)

# Create Player
player = Player()
player.rect.x = (GRID_SPRITE_WIDTH - 0.75) * SPRITE_PIXEL_SIZE
player.rect.y = (GRID_SPRITE_HEIGHT + 6.5) * SPRITE_PIXEL_SIZE
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 1

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

animStartTime = time.time()

'''
    MAIN LOOP
'''
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()
    
    player.move(key)
    player.eat()

    screen.blit(map, (0, 0))
    if time.time() - animStartTime > 0.5:
        if player.image == player.images[0]:
            player.image = player.images[1]
        else:
            player.image = player.images[0]
        animStartTime = time.time()
    player.update()

    for dot in dots:
        dot.draw(screen)

    for pellet in pellets:
        pellet.draw(screen)

    player_list.draw(screen)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)


# Done! Time to quit.
pygame.quit()