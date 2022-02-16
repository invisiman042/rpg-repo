import pygame
from pygame.sprite import Sprite, LayeredUpdates
from sprites import *
from config import *
import sys

class Game:
    # Class for game setup
    def __init__(self) -> None:
        # Initialisation
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 32)
        self.running = True

        self.character_spritesheet = SpriteSheet('img/character.png')
        self.terrain_spritesheet = SpriteSheet('img/terrain.png')
        self.enemy_spritesheet = SpriteSheet('img/enemy.png')
    
    def create_tile_map(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == 'R':
                    Obstacle(self, j, i, type='rock')
                if column == 'B':
                    Obstacle(self, j, i, type='block')
                if column == 'P':
                    Player(self, j, i)
                if column == 'E':
                    Enemy(self, j, i)

    def new(self):
        # Create a new game
        self.playing = True

        self.all_sprites = LayeredUpdates()
        self.blocks = LayeredUpdates()
        self.enemies = LayeredUpdates()
        self.attacks = LayeredUpdates()

        self.create_tile_map()

    def events(self):
        # Game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
    
    def update(self):
        # Game loop update
        self.all_sprites.update()

    def draw(self):
        # Game loop draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # Game loop
        while self.playing == True:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass

g = Game()
g.intro_screen()
g.new()

while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()