# level.py

import os
from config import LEVEL_DIR, TILE_SIZE

class Level:
    def __init__(self, filename):
        self.tiles = []
        self.width = 0
        self.height = 0
        self._load_map(os.path.join(LEVEL_DIR, filename))

    def _load_map(self, path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                row = list(line.rstrip('\n'))
                if len(row) > self.width:
                    self.width = len(row)
                self.tiles.append(row)
        self.height = len(self.tiles)
        # Uzupełnij do równej szerokości (przezroczyste "powietrze")
        for row in self.tiles:
            while len(row) < self.width:
                row.append(' ')

    def get_ground_rects(self):
        """Zwraca listę pygame.Rect dla każdego kafla ziemi (floor lub wall)."""
        import pygame
        rects = []
        for y, row in enumerate(self.tiles):
            for x, char in enumerate(row):
                if char in "#.":  # Wall lub Floor
                    rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return rects

    def find_floor_y(self, x, y_start):
        """Zwraca y, na którym znajduje się najniższy kafel podanego x (dla spawnu przeciwnika)."""
        for y in range(y_start, self.height):
            if self.tiles[y][x] in "#.":
                return y
        return self.height - 1

    def draw(self, screen, camera_x=0, camera_y=0, tile_images=None):
        # Rysuj tylko kafelki, nie tło!
        for y, row in enumerate(self.tiles):
            for x, char in enumerate(row):
                pos = (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y)
                if char == '#':
                    screen.blit(tile_images['wall'], pos)
                elif char == '.':
                    screen.blit(tile_images['floor'], pos)
        # UWAGA: brak rysowania tła! (terminal pod spodem)
