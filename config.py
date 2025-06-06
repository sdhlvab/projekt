# config.py
import os

# Paths
ASSETS_DIR = os.path.join("assets")
IMG_DIR = os.path.join(ASSETS_DIR, "img")
FONT_DIR = os.path.join(ASSETS_DIR, "fonts")
LEVEL_DIR = os.path.join("levels")
DATA_DIR = os.path.join(ASSETS_DIR, "data")

FLOOR_IMG = os.path.join(IMG_DIR, "tile_floor.png")
WALL_IMG = os.path.join(IMG_DIR, "tile_wall.png")
PLAYER_IMG = os.path.join(IMG_DIR, "hackerman_brown.png")
BUGZILLA_IMG = os.path.join(IMG_DIR, "bugzilla.png")

FONT_PATH = os.path.join(FONT_DIR, "UbuntuMono-R.ttf")
TERMINAL_COMMANDS = os.path.join(DATA_DIR, "commands.txt")

# Window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Map/Tile
TILE_SIZE = 64

# Gameplay
PLAYER_SPEED = 5
PLAYER_JUMP = -12
GRAVITY = 0.5

ENEMY_SPEED = 2

# Colors
BLACK = (0, 0, 0)
COLOR_TERMINAL = (0, 255, 0)
GROUND_COLOR = (50, 50, 50)
