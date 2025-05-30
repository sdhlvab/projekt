import pygame
import os
from background import TerminalBackground
from player import Player
from enemy import Enemy

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        # Czcionka UbuntuMono-R.ttf
        font_path = os.path.join("assets", "fonts", "UbuntuMono-R.ttf")
        self.font = pygame.font.Font(font_path, 18)

        # NAJPIERW zdefiniuj ziemię!
        self.ground_rects = [
            pygame.Rect(0, 550, 800, 50),  # ziemia
        ]

        ground_top = self.ground_rects[0].top

        # Komendy z pliku
        self.background = TerminalBackground(
            800, 600, self.font, "assets/data/commands.txt", ground_top, "test"
        )

        self.player = Player((100, 486))
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.enemies = pygame.sprite.Group()
        self.enemies.add(Enemy(300, self.ground_rects[0]))

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
