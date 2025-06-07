import pygame
from config import *
import os

class Level:
    def __init__(self, path):
        self.tiles = []
        self.ground_rects = []
        self.enemy_spawns = []
        self.player_spawn = (TILE_SIZE, TILE_SIZE * 4)
        self.pixel_width = 0
        self.pixel_height = 0
        self._load_map(path)

    def _load_map(self, path):
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f.readlines()]
        self.tiles = []
        self.enemy_spawns = []
        for y, line in enumerate(lines):
            row = []
            for x, char in enumerate(line):
                if char == "#":
                    row.append("wall")
                elif char == ".":
                    row.append("floor")
                elif char == "P":
                    self.player_spawn = (x * TILE_SIZE, y * TILE_SIZE)
                    row.append(None)  # brak kafla pod graczem!
                elif char == "E":
                    self.enemy_spawns.append((x * TILE_SIZE, y * TILE_SIZE))
                    row.append(None)  # brak kafla pod przeciwnikiem!
                else:
                    row.append(None)
            self.tiles.append(row)
        self.pixel_width = len(self.tiles[0]) * TILE_SIZE
        self.pixel_height = len(self.tiles) * TILE_SIZE

    def draw(self, surface, camera_x, camera_y):
        wall_img = pygame.image.load(os.path.join(IMG_DIR, "wall_tile.png")).convert_alpha()
        floor_img = pygame.image.load(os.path.join(IMG_DIR, "floor_tile.png")).convert_alpha()
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                px = x * TILE_SIZE - camera_x
                py = y * TILE_SIZE - camera_y
                if tile == "wall":
                    surface.blit(wall_img, (px, py))
                elif tile == "floor":
                    surface.blit(floor_img, (px, py))

    def get_ground_rects(self):
        ground = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile == "wall" or tile == "floor":
                    ground.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return ground
