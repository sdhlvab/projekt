import pygame
import random

from character import (Character)
from config import TILE_SIZE, ENEMY_TYPES

class Enemy(Character):
    def __init__(self, pos):
        enemy_kinds = list(ENEMY_TYPES.keys())
        kind = random.choice(enemy_kinds)
        image = pygame.image.load(ENEMY_TYPES[kind]["image"]).convert_alpha()
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))  # <-- KLUCZ!
        super().__init__(image, pos, ENEMY_TYPES[kind]["speed"], ENEMY_TYPES[kind]["hp"])
        self.direction = 1

    def update(self, tiles):
        self.velocity.x = self.direction * self.speed if self.on_ground else 0

        def bounce():
            self.direction *= -1
            self.set_facing(self.direction)

        self.apply_gravity()
        self.move_collide(tiles, on_horizontal_collision=bounce)

