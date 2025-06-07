import pygame
from config import ENEMY_IMAGE, TILE_SIZE

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(ENEMY_IMAGE).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 2

    def update(self, tiles):
        # Prosty patrol, opcjonalnie
        pass
