import pygame
from config import PLAYER_IMG, PLAYER_SPEED, PLAYER_JUMP, GRAVITY, TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(PLAYER_IMG).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = PLAYER_SPEED
        self.jump_strength = PLAYER_JUMP
        self.gravity = GRAVITY
        self.on_ground = False
        self.facing_right = True

    def handle_input(self, keys):
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            self.facing_right = True
        if keys[pygame.K_UP] and self.on_ground:
            self.velocity.y = self.jump_strength

    def apply_gravity(self):
        self.velocity.y += self.gravity
        if self.velocity.y > 10:
            self.velocity.y = 10

    def update(self, tiles):
        self.handle_input(pygame.key.get_pressed())
        self.apply_gravity()
        self.rect.x += self.velocity.x
        self.collide(tiles, 'x')
        self.rect.y += self.velocity.y
        self.collide(tiles, 'y')
        if not self.facing_right:
            self.image = pygame.transform.flip(pygame.image.load(PLAYER_IMG).convert_alpha(), True, False)
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        else:
            self.image = pygame.transform.scale(pygame.image.load(PLAYER_IMG).convert_alpha(), (TILE_SIZE, TILE_SIZE))

    def collide(self, tiles, direction):
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if direction == 'x':
                    if self.velocity.x > 0:
                        self.rect.right = tile.rect.left
                    elif self.velocity.x < 0:
                        self.rect.left = tile.rect.right
                elif direction == 'y':
                    if self.velocity.y > 0:
                        self.rect.bottom = tile.rect.top
                        self.velocity.y = 0
                        self.on_ground = True
                    elif self.velocity.y < 0:
                        self.rect.top = tile.rect.bottom
                        self.velocity.y = 0
        if direction == 'y' and not any(self.rect.colliderect(tile.rect) for tile in tiles):
            self.on_ground = False
