import pygame
from config import TILE_SIZE

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        image = pygame.image.load("assets/img/bugzilla.png").convert_alpha()
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))  # <-- KLUCZ!
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 1
        self.speed = 2

    def update(self, ground_rects):
        self.rect.x += self.direction * self.speed
        # Odbijaj się od krawędzi/ścian
        for tile in ground_rects:
            if self.rect.colliderect(tile):
                if self.direction > 0:
                    self.rect.right = tile.left
                else:
                    self.rect.left = tile.right
                self.direction *= -1
