import pygame
from pygame.sprite import Sprite, spritecollide
from config import *
import math, random

class Player(Sprite):

    def __init__(self, game, x, y) -> None:
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        super().__init__(self.groups)

        self.x = x * TILES_SIZE
        self.y = y * TILES_SIZE
        self.width = TILES_SIZE
        self.height = TILES_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'DOWN'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(PLAYER_COORD, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.move()
        self.animate()
        self.collide_enemy()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'LEFT'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'RIGHT'
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'UP'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'DOWN'

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def timer(self):

        if self.in_collision:
            self.in_collision = False
        if not self.in_collision:
            self.in_collision = True
            
    def collide_enemy(self):

        hits = spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False

    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(ANIM_DOWN1, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(ANIM_DOWN2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(ANIM_DOWN3, self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite(ANIM_UP1, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(ANIM_UP2, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(ANIM_UP3, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(ANIM_LEFT1, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(ANIM_LEFT2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(ANIM_LEFT3, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(ANIM_RIGHT1, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(ANIM_RIGHT2, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(ANIM_RIGHT3, self.width, self.height)]

        if self.facing == 'DOWN':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(PLAYER_COORD, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'UP':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(ANIM_UP1, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == 'LEFT':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(ANIM_LEFT1, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == 'RIGHT':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(ANIM_RIGHT1, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

class Obstacle(Sprite):

    def __init__(self, game, x, y, type='block') -> None:

        self.type = type
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        super().__init__(self.groups)

        self.x = x * TILES_SIZE
        self.y = y * TILES_SIZE
        self.width = TILES_SIZE
        self.height = TILES_SIZE

        if type == 'rock':
            self.image = self.game.terrain_spritesheet.get_sprite(ROCK_COORD, self.width, self.height)
        if type == 'block':
            self.image = self.game.terrain_spritesheet.get_sprite(BLOCK_COORD, 78, 78)
            self.image = pygame.transform.scale(self.image, (TILES_SIZE, TILES_SIZE))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class SpriteSheet:

    def __init__(self, file) -> None:
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, coords, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (coords[0], coords[1], width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Ground(Sprite):
    
    def __init__(self, game, x, y) -> None:
        
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        super().__init__(self.groups)

        self.x = x * TILES_SIZE
        self.y = y * TILES_SIZE
        self.width = TILES_SIZE
        self.height = TILES_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(GROUND_COORD, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Enemy(Sprite):

    def __init__(self, game, x, y) -> None:
        
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        super().__init__(self.groups)

        self.x = x * TILES_SIZE
        self.y = y * TILES_SIZE
        self.width = TILES_SIZE
        self.height = TILES_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)
        print(self.max_travel)
        
        self.image = self.game.enemy_spritesheet.get_sprite(ENEMY_COORD, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):

        if self.facing == 'LEFT':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'RIGHT'

        if self.facing == 'RIGHT':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'LEFT'

        if self.facing == 'UP':
            self.y_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'DOWN'
                
        if self.facing == 'DOWN':
            self.y_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'UP'

    def animate(self):
        down_animations = [self.game.enemy_spritesheet.get_sprite(ANIM_DOWN1, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(ANIM_DOWN2, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(ANIM_DOWN3, self.width, self.height)]

        up_animations = [self.game.enemy_spritesheet.get_sprite(ANIM_UP1, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(ANIM_UP2, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(ANIM_UP3, self.width, self.height)]

        left_animations = [self.game.enemy_spritesheet.get_sprite(ANIM_LEFT1, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(ANIM_LEFT2, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(ANIM_LEFT3, self.width, self.height)]

        right_animations = [self.game.enemy_spritesheet.get_sprite(ANIM_RIGHT1, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(ANIM_RIGHT2, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(ANIM_RIGHT3, self.width, self.height)]

        if self.facing == 'DOWN':
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(PLAYER_COORD, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'UP':
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(ANIM_UP1, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == 'LEFT':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(ANIM_LEFT1, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == 'RIGHT':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(ANIM_RIGHT1, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1