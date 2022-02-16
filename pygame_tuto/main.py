#imports
from turtle import back
import pygame, sys
from pygame.locals import *
import random, time

#initialisation
pygame.init()

#FPS setup
FPS = 60
frame_per_sec = pygame.time.Clock()

#colors
BLUE = pygame.Color(0, 0, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

# image loading and scaling
red_car = pygame.image.load('red_car.png')
blue_car = pygame.image.load('blue_car.png')
scale_r = 0.12
scale_b = 0.14
r_h = red_car.get_height()
r_w = red_car.get_width()
b_h = blue_car.get_height()
b_w = blue_car.get_width()
red_car = pygame.transform.scale(red_car, (r_w * scale_r, r_h * scale_r))
blue_car = pygame.transform.scale(blue_car, (b_w * scale_b, b_h * scale_b))
red_car = pygame.transform.rotate(red_car, 180)
r_h = red_car.get_height()
r_w = red_car.get_width()
b_h = blue_car.get_height()
b_w = blue_car.get_width()

#screen creation
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption('Game')

#screen width and height
screen_w, screen_h = pygame.display.get_surface().get_size()

#font setup
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load('AnimatedStreet.png')

#other variables
score = 0
speed = 5
player_speed = 8

class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = red_car
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(r_w, screen_w - r_w), 0)

    def move(self):
        global score
        self.rect.move_ip(0, speed)
        if (self.rect.bottom > (screen_h + (r_h / 2))):
            score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(r_w, screen_w - r_w), 0)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = blue_car
        self.rect = self.image.get_rect()
        self.rect.center = (screen_w / 2, screen_h - b_h)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, - player_speed)
        if self.rect.bottom < screen_h:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, player_speed)
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-player_speed, 0)
        if self.rect.right < screen_w:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(player_speed, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

#creating objects
P1 = Player()
E1 = Enemy()
E2 = Enemy()

#creating groups
enemies = pygame.sprite.Group()
enemies.add(E1)
enemies.add(E2)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
# all_sprites.add(E2)

#user event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 2000)

#game loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            speed += 1
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    score_display = font_small.render(str(score), True, BLACK)
    DISPLAYSURF.blit(score_display, (10, 10))

    #move and draw entities
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    
    if pygame.sprite.spritecollideany(P1, enemies):

        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)
        
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()

        for entity in all_sprites:
            entity.kill()
        time.sleep(0.5)
        pygame.quit()
        sys.exit()
    
    pygame.display.update()
    frame_per_sec.tick(FPS)