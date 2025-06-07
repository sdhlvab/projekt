# config.py

import os

# Ścieżki
ASSETS_DIR = "assets"
IMG_DIR = os.path.join(ASSETS_DIR, "img")
FONT_DIR = os.path.join(ASSETS_DIR, "fonts")
LEVEL_DIR = "levels"
DATA_DIR = "assets/data"

FLOOR_IMG = os.path.join(IMG_DIR, "floor_tile.png")
WALL_IMG = os.path.join(IMG_DIR, "wall_tile.png")
PLAYER_IMG = os.path.join(IMG_DIR, "hackerman_brown.png")
BUGZILLA_IMG = os.path.join(IMG_DIR, "bugzilla.png")

FONT_PATH = os.path.join(FONT_DIR, "UbuntuMono-R.ttf")
TERMINAL_COMMANDS = os.path.join(DATA_DIR, "commands.txt")

# Rozmiary
TILE_SIZE = 64
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

# Kolory
BG_COLOR = (0, 0, 0)
