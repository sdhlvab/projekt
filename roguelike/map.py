import pygame

TILE_SIZE = 32

def load_map_from_txt(filename):
    with open(filename, 'r') as f:
        data = [line.strip() for line in f.readlines()]
    map_data = []
    for row in data:
        map_data.append([char for char in row])
    return map_data

class Map:
    def __init__(self, map_data):
        self.map_data = map_data
        self.height = len(map_data)
        self.width = len(map_data[0]) if self.height > 0 else 0

    def draw(self, screen, floor_img, wall_img):
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile == 'W':  # Wall
                    screen.blit(wall_img, (x * TILE_SIZE, y * TILE_SIZE))
                else:  # Floor by default
                    screen.blit(floor_img, (x * TILE_SIZE, y * TILE_SIZE))
