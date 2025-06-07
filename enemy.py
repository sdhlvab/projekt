import pygame
from config import *
import os

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img_path = os.path.join(IMG_DIR, "bugzilla.png")
        raw = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(raw, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.direction = 1
        self.speed = 2
        self.gravity = 1

    def update(self, tiles):
        # Poruszanie w lewo/prawo i grawitacja
        self.rect.x += self.direction * self.speed
        collide = False
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.direction > 0:
                    self.rect.right = tile.left
                else:
                    self.rect.left = tile.right
                self.direction *= -1
                collide = True
        # Grawitacja
        self.rect.y += self.gravity
        on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile):
                self.rect.bottom = tile.top
                on_ground = True
        if not on_ground:
            self.rect.y += self.gravity
