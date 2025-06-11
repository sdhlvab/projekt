# import pygame
#
# WINDOW_WIDTH = 800
#
# class Projectile(pygame.sprite.Sprite):
#     def __init__(self, x, y, direction, image_path="assets/img/cd.png", speed=10):
#         super().__init__()
#         self.image = pygame.image.load(image_path).convert_alpha()
#         self.image = pygame.transform.scale(self.image, (32, 32))
#         if direction == -1:
#             self.image = pygame.transform.flip(self.image, True, False)
#         self.rect = self.image.get_rect(center=(x, y))
#         self.direction = direction
#         self.speed = speed
#
#     def update(self):
#         self.rect.x += self.speed * self.direction
#         # Usuwanie, jeśli wyjdzie poza ekran
#         if self.rect.right < 0 or self.rect.left > WINDOW_WIDTH:
#             self.kill()


import pygame
from config import *
import os

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        img_path = os.path.join(IMG_DIR, "cd.png")
        raw = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(raw, (32, 32))
        if direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 12

    def update(self, enemies, tiles):
        self.rect.x += self.direction * self.speed
        # Zniszcz pocisk jeśli poza ekranem/mapą
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH * 2:
            self.kill()
        # Kolizja z przeciwnikami
        for enemy in enemies:
            if hasattr(enemy, "rect") and self.rect.colliderect(enemy.rect):
                enemy.kill()
                self.kill()
        # Kolizja ze ścianą
        for tile in tiles:
            if self.rect.colliderect(tile):
                self.kill()
