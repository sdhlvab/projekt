import os
from config import TILE_SIZE, LEVEL_DIR, FLOOR_IMG, WALL_IMG
import pygame

class Level:
    def __init__(self, filename):
        self.tiles = []
        self.player_spawn = None
        self.enemy_spawns = []
        with open(os.path.join(LEVEL_DIR, filename)) as f:
            for y, line in enumerate(f):
                row = []
                for x, char in enumerate(line.strip()):
                    if char == "#":
                        row.append("wall")
                    elif char == ".":
                        row.append("floor")
                    elif char == "P":
                        row.append("floor")
                        self.player_spawn = (x * TILE_SIZE, y * TILE_SIZE)
                    elif char == "E":
                        row.append("floor")
                        self.enemy_spawns.append((x, y))
                    else:
                        row.append("empty")
                self.tiles.append(row)

    def get_ground_rects(self):
        rects = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile == "floor" or tile == "wall":
                    rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return rects

    def get_player_spawn(self):
        return self.player_spawn if self.player_spawn else (TILE_SIZE, TILE_SIZE)

    def get_enemy_spawns(self):
        return self.enemy_spawns

    def draw(self, surface, offset_x=0):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                draw_x = x * TILE_SIZE - offset_x
                draw_y = y * TILE_SIZE
                if tile == "wall":
                    img = pygame.image.load(WALL_IMG).convert_alpha()
                    surface.blit(img, (draw_x, draw_y))
                elif tile == "floor":
                    img = pygame.image.load(FLOOR_IMG).convert_alpha()
                    surface.blit(img, (draw_x, draw_y))
