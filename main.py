import pygame
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
        self.images = []
        img_0 = get_image(spritesheet, 28.5, 0, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        img_1 = get_image(spritesheet, 29.5, 0, SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, True)
        self.images.append(img_0)
        self.images.append(img_1)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.movex = 0
        self.movey = 0
        self.frame = 0

    def control(self, x, y):
        self.movex = x
        self.movey = y
    
    def stop(self):
        self.movex = 0
        self.movey = 0

    def update(self):
        self.rect.x = self.rect.x + self.movex 
        self.rect.y = self.rect.y + self.movey

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
map = get_image(spritesheet, 0, 0, SPRITE_PIXEL_SIZE*GRID_SPRITE_WIDTH, SPRITE_PIXEL_SIZE*GRID_SPRITE_HEIGHT, False)

# Create Player
player = Player()
player.rect.x = 0
player.rect.y = 0
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 1

'''
    MAIN LOOP
'''
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(-steps, 0)
                print('left')
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(steps, 0)
                print('right')
            if event.key == pygame.K_UP or event.key == ord('w'):
                player.control(0, -steps)
                print('up')
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                player.control(0, steps)
                print('down')
        else:
            player.stop()

    screen.blit(map, (0, 0))
    player.update()
    player_list.draw(screen)
    pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)


# Done! Time to quit.
pygame.quit()

