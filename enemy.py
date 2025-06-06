import pygame
from config import BUGZILLA_IMG, TILE_SIZE, ENEMY_SPEED

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(BUGZILLA_IMG).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 1
        self.speed = ENEMY_SPEED

    def update(self, tiles):
        self.rect.x += self.direction * self.speed
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                self.direction *= -1
                break
