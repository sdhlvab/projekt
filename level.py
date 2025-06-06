import os
import pygame
from config import TILE_SIZE, LEVEL_DIR

class Level:
    def __init__(self, filename):
        self.tiles = []
        self.ground_rects = []
        self.enemy_positions = []
        self._load_map(os.path.join(LEVEL_DIR, filename))

    def _load_map(self, path):
        with open(path) as f:
            for y, line in enumerate(f):
                row = []
                for x, char in enumerate(line.rstrip('\n')):
                    row.append(char)
                    if char == '#':
                        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        self.ground_rects.append(rect)
                    elif char == 'E':
                        self.enemy_positions.append((x * TILE_SIZE, y * TILE_SIZE))
                self.tiles.append(row)

    def get_ground_rects(self):
        return self.ground_rects

    def get_enemy_positions(self):
        return self.enemy_positions

    def draw(self, screen, camera_x=0, camera_y=0, tile_images=None):
        for y, row in enumerate(self.tiles):
            for x, char in enumerate(row):
                pos = (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y)
                if char == '#':
                    screen.blit(tile_images['wall'], pos)
                elif char == '.':
                    screen.blit(tile_images['floor'], pos)

