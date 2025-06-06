import pygame
from config import TILE_SIZE, IMG_DIR
from level import Level
from background import TerminalBackground
from player import Player
from enemy import Enemy

class Game:
    def __init__(self, screen, player_name, music_on=True, sound_on=True):
        self.screen = screen
        self.running = True

        # Wczytaj level
        self.level = Level("level1.txt")
        self.tile_size = TILE_SIZE

        # Tło terminalowe
        self.font = pygame.font.Font("assets/fonts/UbuntuMono-R.ttf", 18)
        self.background = TerminalBackground(
            self.screen.get_width(),
            self.screen.get_height(),
            self.font,
            "assets/data/commands.txt",
            self.screen.get_height()
        )

        # Platformy
        self.ground_rects = [
            pygame.Rect(x, y, w, h) for (x, y, w, h) in self.level.get_ground_rects(self.tile_size)
        ]

        # Gracz
        px, py = self.level.player_start if self.level.player_start else (1, 1)
        self.player = Player((px * self.tile_size, py * self.tile_size))
        self.all_sprites = pygame.sprite.Group(self.player)

        # Przeciwnicy
        self.enemies = pygame.sprite.Group()
        for (ex, ey) in self.level.enemy_starts:
            self.enemies.add(Enemy((ex * self.tile_size, ey * self.tile_size)))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.background.update()
        self.all_sprites.update(self.ground_rects)
        self.enemies.update(self.ground_rects)

    def draw(self):
        self.background.draw(self.screen)
        # Rysuj platformy (ściany)
        for rect in self.ground_rects:
            wall_img = pygame.image.load(f"{IMG_DIR}/wall_tile.png").convert_alpha()
            self.screen.blit(wall_img, rect)
        # Sprite’y
        self.all_sprites.draw(self.screen)
        self.enemies.draw(self.screen)
