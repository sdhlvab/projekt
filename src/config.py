ASSETS_DIR = "../assets/"
IMG_DIR = ASSETS_DIR + "img/"
ENEMIES_DIR = IMG_DIR + "enemies/"
PLAYERS_DIR = IMG_DIR + "players/"
MUSIC_DIR = ASSETS_DIR + "music/"
SFX_DIR = ASSETS_DIR + "sfx/"

CMD_FILE = ASSETS_DIR + "data/commands.txt"

FLOOR_TILE = IMG_DIR + "floor2_tile.png"
WALL_TILE = IMG_DIR + "wall3_tile.png"
EXIT_TILE = IMG_DIR + "level_tile.png"

#PLAYER_IMAGE = IMG_DIR + "hackerman_brown.png"
#PLAYER_IMAGE = PLAYERS_DIR + "hackerman2.png"
COIN_IMAGE = IMG_DIR + "boost1.png"
CD_IMAGE = IMG_DIR + "cd.png"

#gracz
PLAYER = {
    "player1": {
        "image": PLAYERS_DIR + "hackerman1.png",
        "tolerance": 10,
    },
    "player2": {
        "image": PLAYERS_DIR + "hackerman2.png",
        "tolerance": 20,
    },
    "player3": {
        "image": PLAYERS_DIR + "hackerman3.png",
        "tolerance": 20,
    },
}
#muzyka
MUSIC = [MUSIC_DIR + "theme1.mp3",
         MUSIC_DIR + "theme2.mp3",
         MUSIC_DIR + "theme3.mp3",
         MUSIC_DIR + "theme4.mp3",
         MUSIC_DIR + "theme5.mp3"]

#sfx
SFX = {
    "coin": SFX_DIR + "coin.mp3",
    "dead": SFX_DIR + "dead.mp3",
    "jump": SFX_DIR + "jump.mp3",
    "kill": SFX_DIR + "kill.mp3",
    "levelup": SFX_DIR + "levelup.mp3",
    "powerup": SFX_DIR + "powerup.mp3",
    "shoot": SFX_DIR + "shoot.mp3",
    "menu": SFX_DIR + "menu.mp3",
    "win": SFX_DIR + "win.mp3",
}

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



# plik z poziomem
LEVEL_FILE = "level1.txt"
LEVEL_DIR = ASSETS_DIR + "levels"

# podstawowe ustawienia
TILE_SIZE = 64
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
FPS = 60

# inne configi
FONT_PATH = ASSETS_DIR + "fonts/UbuntuMono-R.ttf"
FONT_SIZE = 20
