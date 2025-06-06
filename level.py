import pygame

TILE_SIZE = 48

TILE_TYPES = {
    "#": "wall",
    ".": "empty",
    "H": "player",
    "B": "enemy"
}

class Level:
    def __init__(self, filename):
        self.tiles = []
        self.player_start = None
        self.enemies = []
        self.load_from_file(filename)

    def load_from_file(self, filename):
        with open(filename, encoding='utf-8') as f:
            lines = [line.rstrip('\n') for line in f if line.strip()]

        for y, line in enumerate(lines):
            row = []
            for x, char in enumerate(line):
                if char == "H":
                    self.player_start = (x * TILE_SIZE, y * TILE_SIZE)
                    row.append(".")
                elif char == "B":
                    self.enemies.append((x * TILE_SIZE, y * TILE_SIZE))
                    row.append(".")
                else:
                    row.append(char)
            self.tiles.append(row)

    def get_tile(self, x, y):
        if 0 <= y < len(self.tiles) and 0 <= x < len(self.tiles[0]):
            return self.tiles[y][x]
        return None

    def width(self):
        return len(self.tiles[0]) * TILE_SIZE

    def height(self):
        return len(self.tiles) * TILE_SIZE
