import os
import pygame
from config import TILE_SIZE, LEVEL_DIR, FLOOR_TILE, WALL_TILE

class Level:
    def __init__(self, filename):
        self.tiles = []
        self.enemies_pos = []
        self.player_pos = None
        self.width = 0
        self.height = 0
        self._load_map(os.path.join(LEVEL_DIR, filename))

    def _load_map(self, path):
        with open(path) as f:
            lines = [line.rstrip('\n') for line in f if line.strip()]
        self.height = len(lines)
        self.width = max(len(line) for line in lines)
        self.tiles = []
        self.enemies_pos = []
        self.player_pos = None

        for y, line in enumerate(lines):
            row = []
            for x, char in enumerate(line):
                if char == "1":
                    row.append("wall")
                elif char == "0":
                    row.append("floor")
                elif char == "P":
                    row.append("floor")
                    self.player_pos = (x * TILE_SIZE, y * TILE_SIZE)
                elif char == "E":
                    row.append("floor")
                    self.enemies_pos.append((x * TILE_SIZE, y * TILE_SIZE))
                else:
                    row.append(None)
            self.tiles.append(row)

    def get_ground_rects(self):
        rects = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile in ("floor", "wall"):
                    rects.append(pygame.Rect(x * TILE_SIZE, self._offset_y() + y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return rects

    def _offset_y(self):
        # Pozycja startowa Y mapy (od dołu okna)
        import config
        map_height_px = self.height * TILE_SIZE
        return config.SCREEN_HEIGHT - map_height_px

    def draw(self, surface, camera=None):
        floor_img = pygame.image.load(FLOOR_TILE).convert_alpha()
        wall_img = pygame.image.load(WALL_TILE).convert_alpha()

        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                px = x * TILE_SIZE
                py = self._offset_y() + y * TILE_SIZE
                if camera:
                    px, py = camera.apply_point((px, py))
                if tile == "floor":
                    surface.blit(floor_img, (px, py))
                elif tile == "wall":
                    surface.blit(wall_img, (px, py))

    def get_player_spawn(self):
        return self.player_pos

    def get_enemy_spawns(self):
        return self.enemies_pos
