import pygame
from config import *
from player import Player
from enemy import Enemy
from level import Level
from background import TerminalBackground

class Game:
    def __init__(self, screen, player_name="hackerman", music_on=True, sound_on=True):
        self.screen = screen

        self.terminal_font = pygame.font.Font(FONT_PATH, TERMINAL_FONT_SIZE)
        self.terminal_background = TerminalBackground(
            SCREEN_WIDTH, SCREEN_HEIGHT, self.terminal_font, DATA_COMMANDS_PATH, TERMINAL_HEIGHT
        )

        self.level = Level(LEVEL_PATH)
        self.ground_rects = self.level.get_ground_rects()

        self.all_sprites = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        spawn_x, spawn_y = self.level.player_spawn
        self.player = Player((spawn_x, spawn_y), self.projectiles)
        self.all_sprites.add(self.player)

        for ex, ey in self.level.enemy_spawns:
            enemy = Enemy(ex, ey)
            self.enemies.add(enemy)

        self.camera_x = 0
        self.camera_y = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def update(self):
        self.all_sprites.update(self.ground_rects)
        self.projectiles.update(self.enemies, self.ground_rects)
        self.enemies.update(self.ground_rects)
        self._update_camera()

    def _update_camera(self):
        px, py = self.player.rect.center
        # Zawsze w środku ekranu, chyba że na końcach mapy
        self.camera_x = max(0, min(px - SCREEN_WIDTH // 2, self.level.pixel_width - SCREEN_WIDTH))
        self.camera_y = max(0, min(py - SCREEN_HEIGHT // 2, self.level.pixel_height - SCREEN_HEIGHT))

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.terminal_background.draw(self.screen, self.camera_x, self.camera_y)
        self.level.draw(self.screen, self.camera_x, self.camera_y)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, (sprite.rect.x - self.camera_x, sprite.rect.y - self.camera_y))
        for proj in self.projectiles:
            self.screen.blit(proj.image, (proj.rect.x - self.camera_x, proj.rect.y - self.camera_y))
        for enemy in self.enemies:
            self.screen.blit(enemy.image, (enemy.rect.x - self.camera_x, enemy.rect.y - self.camera_y))
