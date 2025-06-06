import pygame
import os
from background import TerminalBackground
from player import Player
from enemy import Enemy
from level import Level, TILE_SIZE

class Game:
    def __init__(self, screen, player_name="Hackerman", music_on=True, sound_on=True):
        self.screen = screen
        self.running = True
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "UbuntuMono-R.ttf"), 18)
        self.background = TerminalBackground(800, 600, self.font, "assets/data/commands.txt", 550)

        # --- Nowość: ładowanie poziomu ---
        self.level = Level("levels/level1.txt")
        self.tiles = pygame.sprite.Group()
        self.ground_rects = []

        # Załaduj kafelki z mapy
        for y, row in enumerate(self.level.tiles):
            for x, tile in enumerate(row):
                if tile == "#":
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    self.ground_rects.append(rect)
                    # Jeśli chcesz rysować ściany: możesz zrobić sprite albo sam rysować obrazek w draw()

        # Start gracza z mapy
        self.player = Player(self.level.player_start)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        # Przeciwnicy z mapy
        self.enemies = pygame.sprite.Group()
        for ex, ey in self.level.enemies:
            self.enemies.add(Enemy(ex, ey))

        # --- Kamera ---
        self.camera_x = 0
        self.screen_width = screen.get_width()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        # Kamera: Hackerman na środku, nie wyjeżdżamy poza mapę!
        px = self.player.rect.centerx
        max_scroll = self.level.width() - self.screen_width
        self.camera_x = max(0, min(px - self.screen_width // 2, max_scroll))

        self.all_sprites.update(self.ground_rects)
        for enemy in self.enemies:
            enemy.update(self.ground_rects)

    def draw(self):
        self.background.draw(self.screen)

        # Rysuj mapę (ziemia/ściany)
        for y, row in enumerate(self.level.tiles):
            for x, tile in enumerate(row):
                tile_img = None
                if tile == "#":
                    tile_img = pygame.image.load("assets/img/wall_tile.png")
                elif tile == ".":
                    tile_img = pygame.image.load("assets/img/floor_tile.png")
                if tile_img:
                    self.screen.blit(tile_img, (x * TILE_SIZE - self.camera_x, y * TILE_SIZE))

        # Gracz/przeciwnicy z przesunięciem kamery
        for sprite in self.all_sprites:
            sprite_rect = sprite.rect.copy()
            sprite_rect.x -= self.camera_x
            self.screen.blit(sprite.image, sprite_rect)
        for enemy in self.enemies:
            enemy_rect = enemy.rect.copy()
            enemy_rect.x -= self.camera_x
            self.screen.blit(enemy.image, enemy_rect)
