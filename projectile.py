import pygame
from config import IMG_DIR, SCREEN_WIDTH
import os

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed=12, damage=10):
        super().__init__()
        img_path = os.path.join(IMG_DIR, "cd.png")
        raw = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(raw, (32, 32))
        if direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = speed
        self.damage = damage

    def update(self, tiles):
        self.rect.x += self.direction * self.speed
        # Zniszcz pocisk jeśli poza mapą
        if self.rect.right < 0 or self.rect.left > max(tile.right for tile in tiles):
            self.kill()
        # Kolizja ze ścianą
        for tile in tiles:
            if self.rect.colliderect(tile):
                self.kill()
