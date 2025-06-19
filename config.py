# Ścieżki do assetów
ASSETS_DIR = "assets/"
IMG_DIR = ASSETS_DIR + "img/"
ENEMIES_DIR = IMG_DIR + "enemies/"
FLOOR_TILE = IMG_DIR + "floor2_tile.png"
WALL_TILE = IMG_DIR + "wall3_tile.png"
PLAYER_IMAGE = IMG_DIR + "hackerman_brown.png"
EXIT_TILE = IMG_DIR + "level_tile.png"

COIN_IMAGE = IMG_DIR + "boost2.png"

#przeciwnicy
ENEMY_TYPES = {
    "bugzilla": {
        "image": ENEMIES_DIR + "bugzilla.png",
        "speed": 4,
        "hp": 50,
    },
    "kernelpanic": {
        "image": ENEMIES_DIR + "kernelpanic.png",
        "speed": 5,
        "hp": 80,
    },
    "malwareslime": {
        "image": ENEMIES_DIR + "malwareslime.png",
        "speed": 2,
        "hp": 100,
    },
    "nullpointer": {
        "image": ENEMIES_DIR + "nullpointer.png",
        "speed": 6,
        "hp": 75,
    },
    "phishingbot": {
        "image": ENEMIES_DIR + "phishingbot.png",
        "speed": 5,
        "hp": 40,
    },
    "rootdeamon": {
        "image": ENEMIES_DIR + "rootdeamon.png",
        "speed": 2,
        "hp": 150,
    },
    "segfault": {
        "image": ENEMIES_DIR + "segfault.png",
        "speed": 4,
        "hp": 85,
    },
    "syntaxterror": {
        "image": ENEMIES_DIR + "syntaxterror.png",
        "speed": 7,
        "hp": 25,
    },
    "trojanhorse": {
        "image": ENEMIES_DIR + "trojanhorse.png",
        "speed": 6,
        "hp": 125,
    },
    "virusworm": {
        "image": ENEMIES_DIR + "virusworm.png",
        "speed": 1,
        "hp": 200,
    },
}

#BUGZILLA_IMAGE = ENEMIES_DIR + "bugzilla.png"



# Plik levela
LEVEL_FILE = "level1.txt"
LEVEL_DIR = ASSETS_DIR + "levels"

# Podstawowe ustawienia
TILE_SIZE = 64
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
FPS = 60

# inne configi, np. czcionka
FONT_PATH = ASSETS_DIR + "fonts/UbuntuMono-R.ttf"
FONT_SIZE = 20
