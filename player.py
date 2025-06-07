import pygame
from config import *
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, projectile_group):
        super().__init__()
        img_path = os.path.join(IMG_DIR, "hackerman_brown_small.png")
        raw = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(raw, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.speed = 5
        self.velocity = pygame.math.Vector2(0, 0)
        self.jump_strength = -12
        self.gravity = 0.5
        self.on_ground = False
        self.projectile_group = projectile_group
        self.last_direction = 1  # 1: prawo, -1: lewo

    def handle_input(self, keys):
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
            self.last_direction = -1
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            self.last_direction = 1
        if keys[pygame.K_UP] and self.on_ground:
            self.velocity.y = self.jump_strength

    def attack(self):
        from projectile import Projectile
        proj = Projectile(self.rect.centerx, self.rect.centery, self.last_direction)
        self.projectile_group.add(proj)

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

    def collide(self, tiles, direction):
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
        if direction == 'y' and not any(self.rect.colliderect(tile) for tile in tiles):
            self.on_ground = False
