import os
from config import LEVEL_DIR

class Level:
    def __init__(self, filename):
        self.tiles = []
        self.player_start = None
        self.enemy_starts = []
        path = os.path.join(LEVEL_DIR, filename)
        with open(path) as f:
            for y, line in enumerate(f):
                row = []
                for x, ch in enumerate(line.rstrip("\n")):
                    if ch == "#":
                        row.append("wall")
                    else:
                        row.append(None)
                    if ch == "P":
                        self.player_start = (x, y)
                    if ch == "E":
                        self.enemy_starts.append((x, y))
                self.tiles.append(row)

    def get_ground_rects(self, tile_size):
        rects = []
        for y, row in enumerate(self.tiles):
            for x, t in enumerate(row):
                if t == "wall":
                    rects.append((x * tile_size, y * tile_size, tile_size, tile_size))
        return rects
