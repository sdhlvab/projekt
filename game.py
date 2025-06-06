import pygame
import os
from background import TerminalBackground
from player import Player
from enemy import Enemy
from level import Level

class Game:
    def __init__(self, screen, player_name="hackerman", music_on=True, sound_on=True):
        self.screen = screen
        self.running = True
        self.music_on = music_on
        self.sound_on = sound_on
        self.player_name = player_name

        # Czcionka terminala
        font_path = os.path.join("assets", "fonts", "UbuntuMono-R.ttf")
        self.font = pygame.font.Font(font_path, 18)

        # Wczytaj level z pliku
        self.level = Level("assets/levels/level1.txt")
        self.ground_rects = self.level.get_ground_rects()
        ground_top = self.ground_rects[0].top if self.ground_rects else 550

        self.background = TerminalBackground(800, 600, self.font, "assets/data/commands.txt", ground_top)

        # Player
        player_start = self.level.player_start or (100, 486)
        self.player = Player(player_start)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        # Enemies
        self.enemies = pygame.sprite.Group()
        for ex, ey in self.level.enemies:
            # Znajdź ziemię pod przeciwnikiem (najbliższy rect pod x,y)
            ground_rect = None
            for rect in self.ground_rects:
                if rect.collidepoint(ex, ey + 1):
                    ground_rect = rect
                    break
            if ground_rect is None and self.ground_rects:
                ground_rect = self.ground_rects[0]
            self.enemies.add(Enemy(ex, ground_rect))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.background.update()
        self.all_sprites.update(self.ground_rects)
        for enemy in self.enemies:
            enemy.update(self.ground_rects)

    def draw(self):
        self.background.draw(self.screen)
        for tile in self.ground_rects:
            pygame.draw.rect(self.screen, (50, 50, 50), tile)
        self.all_sprites.draw(self.screen)
        self.enemies.draw(self.screen)
