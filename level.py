from config import TILE_SIZE, COLOR_PLATFORM
import pygame

class Level:
    def __init__(self, file_path):
        self.tiles = []
        self.ground_rects = []
        self.player_start = (100, 600)
        self.enemy_starts = []
        self.width = 0
        self.height = 0
        self._load(file_path)

    def _load(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            lines = [line.rstrip('\n') for line in f if line.strip()]
        self.height = len(lines)
        self.width = max(len(line) for line in lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if char == "#":
                    self.tiles.append((rect, COLOR_PLATFORM))
                    self.ground_rects.append(rect)
                elif char == "P":
                    self.player_start = (x * TILE_SIZE, y * TILE_SIZE)
                elif char == "E":
                    self.enemy_starts.append((x * TILE_SIZE, y * TILE_SIZE))

    def get_ground_rects(self):
        return self.ground_rects

    def draw(self, surface, camera_x):
        for rect, color in self.tiles:
            r = rect.copy()
            r.x -= camera_x
            pygame.draw.rect(surface, color, r)
