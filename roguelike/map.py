import pygame

TILE_SIZE = 32

def load_map_from_txt(filepath):
    """Wczytaj mapę z pliku tekstowego. Każdy znak to kafelek."""
    with open(filepath, encoding="utf-8") as f:
        return [list(line.strip()) for line in f if line.strip()]

class Map:
    def __init__(self, map_data):
        self.map_data = map_data
        self.height = len(map_data)
        self.width = max(len(row) for row in map_data)

    def draw(self, surface, floor_img, wall_img):
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                pos = (x * TILE_SIZE, y * TILE_SIZE)
                if tile == "#":
                    surface.blit(wall_img, pos)
                elif tile == ".":
                    surface.blit(floor_img, pos)
                # tu można dodać inne typy kafelków
