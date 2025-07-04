import pygame

from src.config import TILE_SIZE, COIN_IMAGE

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load(COIN_IMAGE).convert_alpha()
        self.image = pygame.transform.scale(img, (TILE_SIZE//1.5, TILE_SIZE//1.5))
        self.rect = self.image.get_rect(center=(x+TILE_SIZE//2, y+TILE_SIZE//2))
