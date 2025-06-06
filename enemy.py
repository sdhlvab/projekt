import pygame
from config import ENEMY_IMG, TILE_SIZE

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, ground_rects, speed=2):
        super().__init__()
        img = pygame.image.load(ENEMY_IMG).convert_alpha()
        self.image = pygame.transform.scale(img, (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.ground_rects = ground_rects
        self.speed = speed
        self.direction = 1

    def update(self, ground_rects, camera_x):
        self.rect.x += self.direction * self.speed
        for tile in ground_rects:
            if self.rect.colliderect(tile):
                if self.direction == 1:
                    self.rect.right = tile.left
                else:
                    self.rect.left = tile.right
                self.direction *= -1
