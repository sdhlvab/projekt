import pygame
from src.config import TILE_SIZE, LEVEL_DIR, FLOOR_TILE, WALL_TILE, EXIT_TILE, SCREEN_HEIGHT

class Level:
    def __init__(self, filename):
        self.tiles = []
        self.enemies_pos = []
        self.player_pos = None
        self.width = 0
        self.height = 0
        #self._load_map(os.path.join(LEVEL_DIR, filename))
        self._load_map(filename)
        self.pixel_width = self.width * TILE_SIZE
        self.pixel_height = self.height * TILE_SIZE

    def _load_map(self, path):
        with open(path, encoding="utf-8") as f:
            raw = [line.rstrip('\n') for line in f]
        # obetnij wiodące puste
        while raw and not raw[0].strip():
            raw.pop(0)
        # obetnij końcowe puste
        while raw and not raw[-1].strip():
            raw.pop()
        lines = raw
        self.height = len(lines)
        self.width = max(len(line) for line in lines)
        self.tiles = []
        self.enemies_pos = []
        self.player_pos = None
        self.exit_tiles = []
        self.coins = []

        for y, line in enumerate(lines):
            row = []
            for x, char in enumerate(line):
                if char == "#":
                    row.append("wall")
                elif char == ".":
                    row.append("floor")
                elif char == "P":
                    row.append(None)
                    self.player_pos = (x * TILE_SIZE, self._offset_y() + y * TILE_SIZE)
                elif char == "E":
                    row.append(None)
                    self.enemies_pos.append((x * TILE_SIZE, self._offset_y() + y * TILE_SIZE))
                elif char == "L":
                    row.append("exit")
                    self.exit_tiles.append((x, y))
                elif char == "C":
                    row.append("coin")
                    self.coins.append((x * TILE_SIZE, self._offset_y() + y * TILE_SIZE))
                else:
                    row.append(None)
            self.tiles.append(row)

    def get_ground_rects(self):
        rects = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile in ("floor", "wall"):
                    rects.append(pygame.Rect(x * TILE_SIZE, self._offset_y() + y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        # dodanie pionowych, niewidzialnych ścian przy pionowych krawędziach poziomu
        full_height = len(self.tiles) * TILE_SIZE + self._offset_y()
        level_width = self.width * TILE_SIZE
        # lewa krawędź: od y=0 do full_height
        rects.append(pygame.Rect(0, 0, 1, full_height))
        # prawa krawędź
        rects.append(pygame.Rect(level_width - 1, 0, 1, full_height))
        return rects

    def _offset_y(self):
        # podstawa rysowania zawsze >= 0, dla krótszych map push mapy w dół ekranu
        map_h_px = self.height * TILE_SIZE
        return max(0, SCREEN_HEIGHT - map_h_px)

    def draw(self, surface, camera=None):
        floor_img = pygame.image.load(FLOOR_TILE).convert_alpha()
        wall_img = pygame.image.load(WALL_TILE).convert_alpha()
        exit_img = pygame.image.load(EXIT_TILE).convert_alpha()

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
                elif tile == "exit":
                    surface.blit(exit_img, (px, py))

    def get_player_spawn(self):
        return self.player_pos

    def get_enemy_spawns(self):
        return self.enemies_pos

    def get_exit_rects(self):
        rects = []
        for x, y in self.exit_tiles:
            px = x * TILE_SIZE
            py = self._offset_y() + y * TILE_SIZE
            rects.append(pygame.Rect(px, py, TILE_SIZE, TILE_SIZE))
        return rects

    def get_coin_spawns(self):
        return self.coins
        # spawns = []
        # for y, row in enumerate(self.tiles):
        #     for x, tile in enumerate(row):
        #         if tile == "coin":
        #             spawns.append((x * TILE_SIZE, self._offset_y() + y * TILE_SIZE))
        # return spawns