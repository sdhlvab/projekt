import pygame
from config import TILE_SIZE, PLAYER_IMAGE

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.base_image = pygame.image.load(PLAYER_IMAGE).convert_alpha()
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.speed = 4
        self.jump_strength = -12
        self.velocity = pygame.math.Vector2(0, 0)
        self.gravity = 0.7
        self.on_ground = False
        self.facing_right = True

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
            if self.facing_right:
                self.facing_right = False
                self.image = pygame.transform.flip(self.base_image, True, False)
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            if not self.facing_right:
                self.facing_right = True
                self.image = self.base_image
        if keys[pygame.K_UP] and self.on_ground:
            self.velocity.y = self.jump_strength

    def apply_gravity(self):
        self.velocity.y += self.gravity
        if self.velocity.y > 12:
            self.velocity.y = 12

    def update(self, tiles):
        self.handle_input()
        self.apply_gravity()
        self.rect.x += self.velocity.x
        self.collide(tiles, 'x')
        self.rect.y += self.velocity.y
        self.collide(tiles, 'y')

    def collide(self, tiles, direction):
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile):
                if direction == 'x':
                    if self.velocity.x > 0:
                        self.rect.right = tile.left
                    elif self.velocity.x < 0:
                        self.rect.left = tile.right
                elif direction == 'y':
                    if self.velocity.y > 0:
                        self.rect.bottom = tile.top
                        self.velocity.y = 0
                        self.on_ground = True
                    elif self.velocity.y < 0:
                        self.rect.top = tile.bottom
                        self.velocity.y = 0

    def shoot(self, group):
        from projectile import Projectile
        proj = Projectile(self.rect.center, right=self.facing_right)
        group.add(proj)
