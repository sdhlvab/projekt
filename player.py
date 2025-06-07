# player.py

import pygame
from config import TILE_SIZE, PLAYER_IMG, WINDOW_WIDTH, WINDOW_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        raw = pygame.image.load(PLAYER_IMG).convert_alpha()
        self.image = pygame.transform.scale(raw, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 5
        self.velocity = pygame.math.Vector2(0, 0)
        self.jump_strength = -12
        self.gravity = 0.5
        self.on_ground = False
        self.attack_cooldown = 0

    def handle_input(self, keys):
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
        if keys[pygame.K_UP] and self.on_ground:
            self.velocity.y = self.jump_strength
        if keys[pygame.K_SPACE] and self.attack_cooldown <= 0:
            self.attack_cooldown = 20

    def apply_gravity(self):
        self.velocity.y += self.gravity
        if self.velocity.y > 10:
            self.velocity.y = 10

    def update(self, tiles):
        self.handle_input(pygame.key.get_pressed())
        self.apply_gravity()
        self.rect.x += self.velocity.x
        self.collide(tiles, 'x')
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        self.rect.y += self.velocity.y
        self.collide(tiles, 'y')
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def collide(self, tiles, direction):
        for tile in tiles:
            if self.rect.colliderect(tile):  # UWAGA: tile to pygame.Rect!
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
