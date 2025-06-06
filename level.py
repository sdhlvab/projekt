# level.py
import pygame
from config import TILE_SIZE, WALL_IMG, FLOOR_IMG, LEVEL_DIR
import os

class Level:
    def __init__(self, filename):
        self.tiles = pygame.sprite.Group()
        self.enemies = []
        self.player_start = (100, 100)
        self.map_width = 0
        self.map_height = 0
        self._load_map(os.path.join(LEVEL_DIR, filename))

    def _load_map(self, path):
        with open(path) as f:
            lines = [line.rstrip('\n') for line in f]
        self.map_height = len(lines)
        self.map_width = max(len(line) for line in lines)

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                world_x = x * TILE_SIZE
                world_y = y * TILE_SIZE
                if char == '#':
                    self.tiles.add(Tile(world_x, world_y, WALL_IMG))
                elif char == '.':
                    self.tiles.add(Tile(world_x, world_y, FLOOR_IMG))
                elif char == 'E':
                    self.tiles.add(Tile(world_x, world_y, FLOOR_IMG))
                    self.enemies.append((world_x, world_y))
                elif char == 'P':
                    self.tiles.add(Tile(world_x, world_y, FLOOR_IMG))
                    self.player_start = (world_x, world_y)
                # Dodaj kolejne typy jeśli chcesz

    def get_tiles(self):
        return self.tiles

    def get_enemies(self):
        return self.enemies

    def get_player_start(self):
        return self.player_start

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, img_path):
        super().__init__()
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
