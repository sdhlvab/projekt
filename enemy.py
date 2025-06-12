import pygame

from character import (Character)
from config import TILE_SIZE, ENEMY_IMAGE

class Enemy(Character):
    def __init__(self, pos):
        image = pygame.image.load(ENEMY_IMAGE).convert_alpha()
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))  # <-- KLUCZ!
        super().__init__(image, pos)
        self.direction = 1

    def update(self, tiles):
        if self.on_ground:
            self.velocity.x = self.direction * self.speed
        else:
            self.velocity.x = 0

        self.apply_gravity()
        self.move_collide(tiles)

        for tile in tiles:
            if self.rect.colliderect(tile):
                self.direction *= -1
                self.set_facing(self.direction)