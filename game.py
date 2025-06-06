import pygame
from config import *
from level import Level
from camera import Camera
from player import Player
from enemy import Enemy
from background import TerminalBackground

class Game:
    def __init__(self, screen, player_name="hackerman", music_on=True, sound_on=True):
        self.screen = screen
        self.player_name = player_name
        self.music_on = music_on
        self.sound_on = sound_on

        self.level = Level("level1.txt")
        self.tiles = self.level.get_tiles()
        self.enemies = pygame.sprite.Group()
        for ex, ey in self.level.get_enemies():
            self.enemies.add(Enemy(ex, ey))
        self.player = Player(self.level.get_player_start())

        # Tło terminalowe
        self.font = pygame.font.Font(FONT_PATH, 18)
        self.background = TerminalBackground(WINDOW_WIDTH, WINDOW_HEIGHT, self.font, TERMINAL_COMMANDS, ground_top=WINDOW_HEIGHT)

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.enemies)
        self.camera = Camera(self.level.map_width * TILE_SIZE, self.level.map_height * TILE_SIZE)
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.background.update()
        self.all_sprites.update(self.tiles)
        self.enemies.update(self.tiles)
        self.camera.update(self.player)

    def draw(self):
        self.background.draw(self.screen)
        for tile in self.tiles:
            self.screen.blit(tile.image, self.camera.apply(tile))
        for enemy in self.enemies:
            self.screen.blit(enemy.image, self.camera.apply(enemy))
        self.screen.blit(self.player.image, self.camera.apply(self.player))
