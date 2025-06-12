import pygame
import os

from config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, LEVEL_FILE, PLAYER_IMAGE, ENEMY_IMAGE
from player import Player
from enemy import Enemy
from level import Level
from camera import Camera
from background import TerminalBackground
from engine import ScoreManager
from ui import Scoreboard

class Game:
    def __init__(self, screen, player_name="hackerman", music_on=True, sound_on=True):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.player_name = player_name

        font_path = os.path.join("assets", "fonts", "UbuntuMono-R.ttf")
        font = pygame.font.Font(font_path, 18)
        command_file = "assets/data/commands.txt"

        # Level i kafelki
        self.level = Level(LEVEL_FILE)
        self.ground_rects = self.level.get_ground_rects()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        # Pozycja startowa gracza z pliku levela
        px, py = self.level.get_player_spawn()
        self.player = Player((px, py))
        self.all_sprites = pygame.sprite.Group(self.player)

        # Dodaj przeciwników z levela (np. 'E' w pliku)
        for ex, ey in self.level.get_enemy_spawns():
            self.enemies.add(Enemy((ex, ey)))

        # Kamera
        self.camera = Camera(self.level.pixel_width, self.level.pixel_height, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Terminal w tle (wywołanie bez przesunięcia)
        self.terminal_bg = TerminalBackground(SCREEN_WIDTH, SCREEN_HEIGHT, font, command_file, SCREEN_HEIGHT , player_name)

        # UI
        self.hud = Scoreboard()
        self.score_manager = ScoreManager(self.hud, points_per_kill=100)

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                new_proj = self.player.handle_event(event)
                if new_proj:
                    self.projectiles.add(new_proj)

    def update(self):
        self.player.update(pygame.key.get_pressed(), self.ground_rects)
        self.enemies.update(self.ground_rects)

        self.projectiles.update(self.enemies, self.level.get_ground_rects())

        self.camera.update(self.player.rect)
        self.terminal_bg.update()

        self.score_manager.handle_hits(self.projectiles, self.enemies)

    def draw(self):
        # Tło terminala (nie podlega kamerze)
        self.terminal_bg.draw(self.screen, self.camera.x, self.camera.y)

        # Rysuj level (kafelki)
        self.level.draw(self.screen, self.camera)
        # Rysuj gracza
        self.screen.blit(self.player.image, self.camera.apply(self.player.rect))

        # Rysowanie przeciwników
        for e in self.enemies: e.draw(self.screen, self.camera)
        for p in self.projectiles: self.screen.blit(p.image, self.camera.apply(p.rect))

        # Rysowanie HUD'a
        self.hud.draw(self.screen)
        pygame.display.flip()