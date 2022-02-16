import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
from pygame.sprite import spritecollide
from pygame.locals import *
import sys, random
from tkinter import filedialog
from tkinter import *

# Initialisation
pygame.init()

# Variables
vector = pygame.math.Vector2
HEIGHT = 350
WIDTH = 700
ACCELERATION = 0.3
FRICTION = - 0.1
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0

# Creating display
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

# Loading images
run_ani_R = [pygame.image.load(r'files\player\run\Player_Sprite_R.png'), pygame.image.load(r'files\player\run\Player_Sprite2_R.png'),
            pygame.image.load(r'files\player\run\Player_Sprite3_R.png'), pygame.image.load(r'files\player\run\Player_Sprite4_R.png'),
            pygame.image.load(r'files\player\run\Player_Sprite5_R.png'), pygame.image.load(r'files\player\run\Player_Sprite6_R.png')]

run_ani_L = [pygame.image.load(r'files\player\run\Player_Sprite_L.png'), pygame.image.load(r'files\player\run\Player_Sprite2_L.png'),
            pygame.image.load(r'files\player\run\Player_Sprite3_L.png'), pygame.image.load(r'files\player\run\Player_Sprite4_L.png'),
            pygame.image.load(r'files\player\run\Player_Sprite5_L.png'), pygame.image.load(r'files\player\run\Player_Sprite6_L.png')]

att_ani_R = [pygame.image.load(r'files\player\run\Player_Sprite_R.png'), pygame.image.load(r'files\player\attack\Player_Attack_R.png'),
            pygame.image.load(r'files\player\attack\Player_Attack2_R.png'), pygame.image.load(r'files\player\attack\Player_Attack3_R.png'),
            pygame.image.load(r'files\player\attack\Player_Attack4_R.png'), pygame.image.load(r'files\player\attack\Player_Attack5_R.png'),
            pygame.image.load(r'files\player\run\Player_Sprite_R.png')]

att_ani_L = [pygame.image.load(r'files\player\run\Player_Sprite_L.png'), pygame.image.load(r'files\player\attack\Player_Attack_L.png'),
            pygame.image.load(r'files\player\attack\Player_Attack2_L.png'), pygame.image.load(r'files\player\attack\Player_Attack3_L.png'),
            pygame.image.load(r'files\player\attack\Player_Attack4_L.png'), pygame.image.load(r'files\player\attack\Player_Attack5_L.png'),
            pygame.image.load(r'files\player\run\Player_Sprite_L.png')]

health_ani = [pygame.image.load(r'files\hearts\heart0.png'), pygame.image.load(r'files\hearts\heart.png'), 
            pygame.image.load(r'files\hearts\heart2.png'), pygame.image.load(r'files\hearts\heart3.png'),
            pygame.image.load(r'files\hearts\heart4.png'), pygame.image.load(r'files\hearts\heart5.png')]

# Define font styles
heading_font = pygame.font.SysFont('Verdana', 40)
regular_font = pygame.font.SysFont('Corbel', 25)
smaller_font = pygame.font.SysFont('Corbel', 16)

# Colors
GREY = (170, 170, 170)
DARK_GREY = (100, 100, 100)
WHITE = (255, 255, 255)

# Creating the classes
class Background(Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.bgimage = pygame.image.load('files\Background.png')
        self.bgX = 0
        self.bgY = 0
    
    def render(self):
        displaysurface.blit(self.bgimage, (self.bgX, self.bgY))

class Ground(Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load('files\Ground.png')
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT))

    def render(self):
        displaysurface.blit(self.image, (self.rect.x, self.rect.y))

class Player(Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('files\player\Player_Sprite_R.png')
        self.rect = self.image.get_rect()
        self.vx = 0
        self.position = vector((WIDTH / 2, 0))
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)
        self.direction = 'RIGHT'
        self.jumping = False
        self.running = False
        self.move_frame = 0
        self.move_frame_count = 0
        self.attacking = False
        self.attack_frame = 0
        self.attack_frame_count = 0
        self.cooldown = False
        self.health = 5
        self.mana = 0
        self.experience = 0

    def move(self):
        # Gravity
        self.acceleration = vector(0, 0.5)

        # Stop running under 0.3
        if abs(self.velocity.x) > 0.2:
            self.running = True
        else:
            self.running = False
        
        # Return key press
        pressed_key = pygame.key.get_pressed()

        # Direction of acceleration
        if pressed_key[K_q]:
            self.acceleration.x = - ACCELERATION
        if pressed_key[K_d]:
            self.acceleration.x = ACCELERATION

        # Motion formulas
        self.acceleration.x += self.velocity.x * FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        # Wraping between sides
        if self.position.x > WIDTH:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y < self.rect.height:
            self.position.y = self.rect.height

        # Update rectangle position
        self.rect.midbottom = self.position

    def update(self):
        
        if cursor.wait == 1:
            return
        # Return to 1st frame
        if self.move_frame > 5:
            self.move_frame = 0
            self.move_frame_count = 0
        
        # Change frame when running
        if self.jumping == False and self.running == True:
            if self.velocity.x > 0:
                self.image = run_ani_R[self.move_frame]
                self.direction = 'RIGHT'
            else:
                self.image = run_ani_L[self.move_frame]
                self.direction = 'LEFT'
            if self.move_frame_count % 3 == 0:
                self.move_frame += 1
            self.move_frame_count += 1
        
        # Return to base frame if standing
        if abs(self.velocity.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == 'RIGHT':
                self.image = run_ani_R[self.move_frame]
            if self.direction == 'LEFT':
                self.image = run_ani_L[self.move_frame]
            
    def attack(self):

        if cursor.wait == 1:
            return

        if self.attack_frame > 6:
            self.attack_frame = 0
            self.attacking = False

        if self.direction == 'RIGHT':
            self.image = att_ani_R[self.attack_frame]
        if self.direction == 'LEFT':
            self.correction()
            self.image = att_ani_L[self.attack_frame]

        if self.attack_frame_count % 3 == 0:
            self.attack_frame += 1
        self.attack_frame_count += 1

    def correction(self):
        if self.attack_frame == 1:
            self.position.x -= 20
            self.attack_frame += 1
        if self.attack_frame == 6:
            self.position.x += 20
            self.attack_frame = 0
            self.attacking = False

    def jump(self):
        hits = spritecollide(self, ground_group, False)

        if hits and not self.jumping:
            self.jumping = True
            self.velocity.y = - 12

            if self.direction == 'LEFT':
                self.velocity.x -= 3
            if self.direction == 'RIGHT':
                self.velocity.x += 3

    def gravity_check(self):
        hits = spritecollide(player, ground_group, False)
        if self.velocity.y > 0:
            if hits:
                lowest = hits[0]
                if self.position.y < HEIGHT:
                    self.position.y = lowest.rect.top + 1
                    self.velocity.y = 0
                    self.jumping = False

    def player_hit(self):
        if not self.cooldown:
            self.cooldown = True
            pygame.time.set_timer(hit_cooldown, 1000)

            self.health -= 1
            health.image = health_ani[self.health]
            print(f'{self} hit : {self.health} / 5')

            if self.health <= 0:
                self.kill()
                pygame.display.update()

class Enemy(Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('files\enemy\Enemy.png')
        self.rect = self.image.get_rect()
        self.position = vector(0, 0)
        self.velocity = vector(0, 0)
        self.direction = random.randint(0, 1)
        self.velocity.x = random.randint(2, 6)
        self.mana = random.randint(1, 3)
        if self.direction == 0:
            self.position.x = 0
        if self.direction == 1:
            self.position.x = WIDTH
        self.position.y = 235
        self.living = True
    
    def move(self):

        if cursor.wait == 1:
            return
        # Wraping between sides
        if self.position.x > (WIDTH - self.rect.width):
            self.direction = 1
        if self.position.x < 0:
            self.direction = 0
        
        # Update position
        if self.direction == 0:
            self.position.x += self.velocity.x
        if self.direction == 1:
            self.position.x -= self.velocity.x

        self.rect.center = self.position

    def render(self):
        if self.living:
            displaysurface.blit(self.image, (self.position.x, self.position.y))

    def update(self):
        hits = spritecollide(self, Playergroup, False)

        f_hits = spritecollide(self, FireballGroup, False)

        if hits and player.attacking or f_hits:

            if player.mana < 100:
                player.mana += self.mana

            player.experience += 1
            handler.dead_enemy_count += 1

            self.kill()

            item_id = 0
            rand_num = random.uniform(0, 100)

            if rand_num >= 0 and rand_num <= 5:
                item_id = 1 # Heart
            if rand_num > 5 and rand_num <= 15:
                item_id = 2 # Coin
            
            if item_id != 0:
                item = Item(item_id)
                ItemGroup.add(item)

                item.position.x = self.position.x
                item.position.y = self.position.y

        if hits and not player.attacking:
            player.player_hit()

class Castle(Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.hide = False
        self.image = pygame.image.load('files\Castle.png')
    
    def update(self):
        if self.hide == False:
            displaysurface.blit(self.image, (400, 80))

class EventHandler(Sprite):
    def __init__(self):
        self.enemy_count = 0
        self.battle = False
        self.enemy_generation = pygame.USEREVENT + 2
        self.stage = 1
        self.dead_enemy_count = 0
        self.waiting_for_next_stage = False
        
        self.stage_enemies = []
        for x in range(1, 21):
            self.stage_enemies.append(x * 2)
            # self.stage_enemies.append(int((x ** 2 / 2) + 1))
    
    def stage_handler(self):
        self.root = Tk()
        self.root.geometry('200x170')

        button1 = Button(self.root, text='Twilight Dungeon', width=18, height=2, command=self.world1)
        button2 = Button(self.root, text='Skyward Dungeon', width=18, height=2, command=self.world2)
        button3 = Button(self.root, text='Hell Dungeon', width=18, height=2, command=self.world3)

        button1.place(x=40, y=15)
        button2.place(x=40, y=65)
        button3.place(x=40, y=115)

        self.root.mainloop()

    def update(self):
        if self.dead_enemy_count == self.stage_enemies[self.stage - 1]:
            self.dead_enemy_count = 0
            stage_text.clear = True
            stage_text.stage_clear()
            self.waiting_for_next_stage = True

    def world1(self):
        # self.root.destroy()
        pygame.time.set_timer(self.enemy_generation, 2000)
        button.image_display = 1
        castle.hide = True
        self.battle = True

    def world2(self):
        self.battle = True
        button.image_display = 1

    def world3(self):
        self.battle = True
        button.image_display = 1

    def next_stage(self):
        button.image_display = 1
        self.stage += 1
        print(f'Stage : {self.stage}')
        self.enemy_count = 0
        self.dead_enemy_count = 0
        pygame.time.set_timer(self.enemy_generation, 1500 - (50 * self.stage))
        self.waiting_for_next_stage = False

    def home(self):
        pygame.time.set_timer(self.enemy_generation, 0)
        self.battle = True
        self.enemy_count = 0
        self.dead_enemy_count = 0
        self.stage = 1

        for group in Enemies, ItemGroup:
            for entity in group:
                entity.kill()

        castle.hide = False
        background.bgimage = pygame.image.load('files\Background.png')
        ground.image = pygame.image.load('files\Ground.png')

class HealthBar(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('files\hearts\heart5.png')
    
    def render(self):
        displaysurface.blit(self.image, (10, 10))

class StageText(Sprite):
    def __init__(self):
        super().__init__()
        pygame.font.init()
        self.font = heading_font
        self.text = self.font.render(f'Stage : {handler.stage}', True, DARK_GREY)
        self.position = vector(-100, 100)
        self.display = False
        self.clear = False
    
    def move_display(self):
        self.text = self.font.render(f'Stage : {handler.stage}', True, DARK_GREY)
        if self.position.x < 720:
            self.position.x += 10
            displaysurface.blit(self.text, (self.position.x, self.position.y))
        else:
            self.display = False
            self.position.x = - 100
            self.position.y = 100

    def stage_clear(self):
        self.font = heading_font
        self.text = self.font.render('STAGE CLEAR !', True, DARK_GREY)
        button.image_display = 0

        if self.position.x < 720:
            self.position.x += 10
            displaysurface.blit(self.text, (self.position.x, self.position.y))
        else:
            self.clear = False
            self.position.x = - 100
            self.position.y = 100

class StatusBar(Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.surf = pygame.Surface((90, 65))
        self.rect = self.surf.get_rect(center=(500, 100))

    def update_draw(self):
        text1 = smaller_font.render(f'STAGE : {handler.stage}', True, WHITE)
        text2 = smaller_font.render(f'EXP : {player.experience}', True, WHITE)
        text3 = smaller_font.render(f'MANA : {player.mana}', True, WHITE)
        text4 = smaller_font.render(f'FPS : {int(FPS_CLOCK.get_fps())}', True, WHITE)
        text5 = smaller_font.render(f'KILL : {handler.dead_enemy_count} / {handler.stage_enemies[handler.stage - 1]}', True, WHITE)
        text5b = smaller_font.render(f'KILL : {handler.stage_enemies[handler.stage - 1]} / {handler.stage_enemies[handler.stage - 1]}', True, WHITE)

        displaysurface.blit(text1, (585, 7))
        displaysurface.blit(text2, (585, 22))
        displaysurface.blit(text3, (585, 37))
        displaysurface.blit(text4, (585, 52))
        if handler.battle:
            self.surf = pygame.Surface((90, 83))
            if handler.waiting_for_next_stage:
                displaysurface.blit(text5b, (585, 70))
            else:
                displaysurface.blit(text5, (585, 70))

class Item(Sprite):

    def __init__(self, item_type) -> None:
        super().__init__()
        if item_type == 1:
            self.image = pygame.image.load('files\heart.png')
        if item_type == 2:
            self.image = pygame.image.load('files\coin.png')
        self.rect = self.image.get_rect()
        self.type = item_type
        self.position = vector(0, 0)
    
    def render(self):
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        displaysurface.blit(self.image, self.rect)

    def update(self):
        hits = spritecollide(self, Playergroup, False)
        if hits:
            print(f'collide with {self.type}')
            if player.health < 5 and self.type == 1:
                player.health += 1
                health.image = health_ani[player.health]
                self.kill()
            if self.type == 2:
                self.kill()

class PButton(Sprite):

    def __init__(self):
        super().__init__()
        self.vector = vector(620, 300)
        self.image_display = 0
    
    def render(self, num):
        if num == 0:
            self.image = pygame.image.load('files\home_small.png')
        if num == 1:
            if cursor.wait == 0:
                self.image = pygame.image.load('files\pause_small.png')
            else:
                self.image = pygame.image.load('files\play_small.png')
        
        displaysurface.blit(self.image, self.vector)

class Cursor(Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('files\cursor.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.wait = 0

    def pause(self):
        if self.wait == 1:
            self.wait = 0
        else:
            self.wait = 1
    
    def hover(self):
        if 620 <= mouse[0] <= 670 and 300 <= mouse[1] <= 345:
            pygame.mouse.set_visible(False)
            cursor.rect.center = pygame.mouse.get_pos()
            displaysurface.blit(cursor.image, cursor.rect)
        else:
            pygame.mouse.set_visible(True)

class Fireball(Sprite):

    def __init__(self):
        super().__init__()
        self.direction = player.direction
        if self.direction == 'RIGHT':
            self.image = pygame.image.load(r'files\fireball1_R.png')
        if self.direction == 'LEFT':
            self.image = pygame.image.load(r'files\fireball1_L.png')
        
        self.rect = self.image.get_rect(center=(player.position))
        self.rect.x = player.position.x
        self.rect.y = player.position.y - 40
    
    def fire(self):
        player.magic_cooldown = 0

        if - 10 < self.rect.x < WIDTH + 10:
            if self.direction == 'RIGHT':
                self.image = pygame.image.load(r'files\fireball1_R.png')
            if self.direction == 'LEFT':
                self.image = pygame.image.load(r'files\fireball1_L.png')
            displaysurface.blit(self.image, self.rect)

            if self.direction == 'RIGHT':
                self.rect.move_ip(12, 0)
            if self.direction == 'LEFT':
                self.rect.move_ip(- 12, 0)
        else:
            self.kill()
            player.magic_cooldown = 1
            player.attacking = False

# Creating objects
background = Background()

ground = Ground()
ground_group = Group()
ground_group.add(ground)

player = Player()
Playergroup = Group()
Playergroup.add(player)

ItemGroup = Group()

Enemies = Group()

FireballGroup = Group()

castle = Castle()

handler = EventHandler()

health = HealthBar()

hit_cooldown = pygame.USEREVENT + 1

stage_text = StageText()

status_bar = StatusBar()

button = PButton()

cursor = Cursor()

# Game Loop
while True:
    player.gravity_check()
    mouse = pygame.mouse.get_pos()

    # Iterate in the event list
    for event in pygame.event.get():
        # print(event)
        # Close button
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Left clic
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 620 <= mouse[0] <= 670 and 300 <= mouse[1] <= 345:
                if button.image_display == 1:
                    cursor.pause()
                if button.image_display == 0:
                    handler.home()

        # Keyboard
        if event.type == pygame.KEYDOWN:

            # SPACE to jump
            if event.key == pygame.K_SPACE:
                player.jump()
            
            # KEYPAD 3 to attack
            if event.key == pygame.K_KP3:
                if player.attacking == False:
                    player.attack()
                    player.attacking = True

            # E for dungeon entrance
            if event.key == pygame.K_e and 450 < player.position.x < 550:
                handler.world1()

            # N for next stage
            if event.key == pygame.K_n:
                if handler.battle == True and len(Enemies) == 0:
                    handler.next_stage()
                    stage_text = StageText()
                    stage_text.display = True
            
            # I for Informations
            if event.key == pygame.K_i:
                print(f'Stage : {handler.stage}, len(Enemies) : {len(Enemies)}, enemy_count : {handler.enemy_count}, stage_enemies : {handler.stage_enemies[handler.stage - 1]}')

            # KEYPAD 2 for magic attack
            if event.key == pygame.K_KP2:
                if player.mana >= 2:
                    player.mana -= 2
                    player.attacking = True
                    fireball = Fireball()
                    FireballGroup.add(fireball)

        if event.type == hit_cooldown:
            player.cooldown = False
            pygame.time.set_timer(hit_cooldown, 0)
        
        if event.type == handler.enemy_generation:
            if handler.enemy_count < handler.stage_enemies[handler.stage - 1]:
                enemy = Enemy()
                Enemies.add(enemy)
                handler.enemy_count += 1
            
    # Render functions
    background.render()
    ground.render()
    button.render(button.image_display)
    cursor.hover()

    castle.update()

    player.update()
    if player.attacking:
        player.attack()
    player.move()
    
    if player.health > 0:
        displaysurface.blit(player.image, player.rect)
    
    health.render()

    for entity in Enemies:
        entity.update()
        entity.move()
        entity.render()
    
    if stage_text.display:
        stage_text.move_display()

    if stage_text.display:
        stage_text.move_display()
    if stage_text.clear:
        stage_text.stage_clear()

    for i in ItemGroup:
        i.render()
        i.update()

    for ball in FireballGroup:
        ball.fire()

    displaysurface.blit(status_bar.surf, (580, 5))
    status_bar.update_draw()
    handler.update()

    pygame.display.update()
    FPS_CLOCK.tick(FPS)