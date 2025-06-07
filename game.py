# game.py

import pygame
from config import (TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, FLOOR_IMG, WALL_IMG)
from level import Level
from player import Player
from enemy import Enemy
from background import TerminalBackground  # Zakładam, że masz taki moduł!

class Game:
    def __init__(self, screen, player_name="", music_on=True, sound_on=True):
        self.screen = screen
        self.player_name = player_name
        self.music_on = music_on
        self.sound_on = sound_on

        # Tło terminala
        font_path = "assets/fonts/UbuntuMono-R.ttf"
        font = pygame.font.Font(font_path, 18)
        self.background = TerminalBackground(WINDOW_WIDTH, WINDOW_HEIGHT, font, "assets/data/commands.txt", ground_top=WINDOW_HEIGHT)

        # Poziom
        self.level = Level("level1.txt")
        self.ground_rects = self.level.get_ground_rects()

        # Kafelki do podania do draw
        self.tile_images = {
            'floor': pygame.image.load(FLOOR_IMG).convert_alpha(),
            'wall': pygame.image.load(WALL_IMG).convert_alpha(),
        }

        # Gracz
        self.player = Player((TILE_SIZE, TILE_SIZE * (self.level.height - 2)))
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        # Przeciwnicy (ustaw na podłodze w levelu)
        self.enemies = pygame.sprite.Group()
        for y, row in enumerate(self.level.tiles):
            for x, char in enumerate(row):
                if char == 'B':  # 'B' to Bugzilla w pliku txt
                    world_x, world_y = x * TILE_SIZE, y * TILE_SIZE
                    self.enemies.add(Enemy(world_x, world_y))

        # Kamera
        self.camera_x = 0
        self.camera_y = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.all_sprites.update(self.ground_rects)
        self.enemies.update(self.ground_rects)
        # Kamera śledzi gracza
        player_center_x = self.player.rect.centerx
        self.camera_x = max(0, player_center_x - WINDOW_WIDTH // 2)
        self.camera_y = 0  # Jeśli chcesz, dodaj pionową kamerę

    def draw(self):
        self.background.draw(self.screen)
        self.level.draw(self.screen, camera_x=self.camera_x, camera_y=self.camera_y, tile_images=self.tile_images)
        self.enemies.draw(self.screen)
        self.all_sprites.draw(self.screen)
