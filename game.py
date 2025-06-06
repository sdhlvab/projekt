import pygame
import os
from config import WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, LEVEL_DIR, FPS
from level import Level
from player import Player
from enemy import Enemy
from background import TerminalBackground

class Game:
    def __init__(self, screen, player_name="hackerman", music_on=True, sound_on=True):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.level = Level("level1.txt")
        self.tile_size = TILE_SIZE
        self.tile_images = {
            'ground': pygame.image.load(os.path.join("assets", "img", "tile_floor.png")).convert_alpha(),
        }
        # Czcionka terminala
        font_path = os.path.join("assets", "fonts", "UbuntuMono-R.ttf")
        self.font = pygame.font.Font(font_path, 18)
        self.background = TerminalBackground(WINDOW_WIDTH, WINDOW_HEIGHT, self.font, "assets/data/commands.txt", ground_top=WINDOW_HEIGHT - TILE_SIZE*1)

        self.camera_x = 0
        self.camera_y = 0

        self.ground_rects = self.level.get_ground_rects()
        self.player = Player((100, 400))
        self.all_sprites = pygame.sprite.Group(self.player)

        self.enemies = pygame.sprite.Group()
        for (ex, ey) in self.level.get_enemy_positions():
            self.enemies.add(Enemy(ex, ey))

    def update(self):
        self.background.update()
        self.all_sprites.update(self.ground_rects)
        self.enemies.update(self.ground_rects)
        # Kamera podąża za graczem (X)
        self.camera_x = max(0, self.player.rect.centerx - WINDOW_WIDTH // 2)
        self.camera_y = 0  # Brak pionowego scrolla

    def draw(self):
        self.background.draw(self.screen)
        self.level.draw(self.screen, camera_x=self.camera_x, camera_y=self.camera_y, tile_images=self.tile_images)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, (sprite.rect.x - self.camera_x, sprite.rect.y - self.camera_y))
        for enemy in self.enemies:
            self.screen.blit(enemy.image, (enemy.rect.x - self.camera_x, enemy.rect.y - self.camera_y))
