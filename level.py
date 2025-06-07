import pygame
from config import TILE_SIZE, FLOOR_TILE, WALL_TILE

class Level:
    def __init__(self, filename):
        with open(filename) as f:
            lines = [line.rstrip('\n') for line in f if line.strip()]
        self.map = lines
        self.width = len(lines[0])
        self.height = len(lines)
        self.pixel_width = self.width * TILE_SIZE
        self.pixel_height = self.height * TILE_SIZE
        self.floor_img = pygame.image.load(FLOOR_TILE).convert_alpha()
        self.wall_img = pygame.image.load(WALL_TILE).convert_alpha()

    def draw(self, surface, camera):
        for y, row in enumerate(self.map):
            for x, char in enumerate(row):
                px, py = x * TILE_SIZE, y * TILE_SIZE
                pos = camera.apply(pygame.Rect(px, py, TILE_SIZE, TILE_SIZE))
                if char == "#":
                    surface.blit(self.wall_img, pos)
                elif char == ".":
                    surface.blit(self.floor_img, pos)

    def get_ground_rects(self):
        rects = []
        for y, row in enumerate(self.map):
            for x, char in enumerate(row):
                if char == "#" or char == ".":
                    rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return rects

    def get_player_spawn(self):
        for y, row in enumerate(self.map):
            for x, char in enumerate(row):
                if char == "P":
                    return (x * TILE_SIZE, y * TILE_SIZE)
        return (0, 0)

    def get_enemy_spawns(self):
        result = []
        for y, row in enumerate(self.map):
            for x, char in enumerate(row):
                if char == "E":
                    result.append((x * TILE_SIZE, y * TILE_SIZE))
        return result
