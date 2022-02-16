class Enemy(Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load('files\enemy\Enemy.png')
        self.rect = self.image.get_rect()
        self.position = vector(0, 0)
        self.velocity = vector(0, 0)
        self.direction = random.randint(0, 1)
        self.velocity.x = random.randint(2, 6)
        if self.direction == 0:
            self.position.x = 0
        if self.direction == 1:
            self.position.x = WIDTH
        self.position.y = 235
        self.living = True
    
    def move(self):

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

        if hits and player.attacking:
            self.living = False
            self.kill()
        if hits and not player.attacking:
            player.player_hit()