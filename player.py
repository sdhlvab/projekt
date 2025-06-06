import pygame
from config import *
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, game):
        super().__init__()
        self.game = game
        img = pygame.image.load(PLAYER_IMG).convert_alpha()
        self.image_right = pygame.transform.scale(img, (64, 64))
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right
        self.rect = self.image.get_rect(topleft=pos)
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.jump_strength = -12
        self.gravity = 0.5
        self.on_ground = False
        self.direction = 1  # 1=right, -1=left
        self.attack_cooldown = 0

    def handle_keydown(self, event):
        if event.key == pygame.K_SPACE and self.attack_cooldown <= 0:
            self.attack()
            self.attack_cooldown = 20

    def attack(self):
        from projectile import Disk
        disk = Disk(self.rect.centerx, self.rect.centery, self.direction)
        self.game.attacks.add(disk)

    def apply_gravity(self):
        self.velocity.y += self.gravity
        if self.velocity.y > 10:
            self.velocity.y = 10

    def update(self, tiles, camera_x):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
            self.image = self.image_left
            self.direction = -1
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            self.image = self.image_right
            self.direction = 1
        if keys[pygame.K_UP] and self.on_ground:
            self.velocity.y = self.jump_strength
        self.apply_gravity()
        self.rect.x += self.velocity.x
        self.collide(tiles, 'x')
        self.rect.y += self.velocity.y
        self.collide(tiles, 'y')
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

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
        # Grawitacja off tylko gdy stoimy na czymś
        if direction == 'y' and not any(self.rect.colliderect(tile) for tile in tiles):
            self.on_ground = False
