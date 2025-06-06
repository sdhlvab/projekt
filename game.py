import pygame
from config import *
from player import Player
from enemy import Enemy
from background import TerminalBackground
from level import Level

class Game:
    def __init__(self, screen, player_name, music_on=True, sound_on=True):
        self.screen = screen
        self.running = True
        self.player_name = player_name
        self.music_on = music_on
        self.sound_on = sound_on

        # Wczytaj poziom
        self.level = Level(LEVEL_FILE)
        self.ground_rects = self.level.get_ground_rects()

        # Terminal jako tło
        font = pygame.font.Font(FONT_PATH, 18)
        self.background = TerminalBackground(WINDOW_WIDTH, WINDOW_HEIGHT, font, "assets/data/commands.txt", self.ground_rects[0].top)

        # Kamera (scroll X)
        self.camera_x = 0

        # Gracz i przeciwnicy
        self.player = Player(self.level.player_start, self)
        self.all_sprites = pygame.sprite.Group(self.player)
        self.enemies = pygame.sprite.Group()
        for ex, ey in self.level.enemy_starts:
            self.enemies.add(Enemy((ex, ey), self.ground_rects))
        self.all_sprites.add(self.enemies)

        # Ataki (np. dyskietki)
        self.attacks = pygame.sprite.Group()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                self.player.handle_keydown(event)

    def update(self):
        self.player.update(self.ground_rects, self.camera_x)
        self.enemies.update(self.ground_rects, self.camera_x)
        self.attacks.update(self.camera_x)
        # Kolizje ataku z wrogiem
        for attack in self.attacks:
            hit_list = pygame.sprite.spritecollide(attack, self.enemies, True)
            if hit_list:
                attack.kill()

        # Scrollowanie kamery – trzyma gracza mniej więcej na środku
        target_cx = self.player.rect.centerx - WINDOW_WIDTH // 2
        max_cx = max(0, self.level.width * TILE_SIZE - WINDOW_WIDTH)
        self.camera_x = max(0, min(target_cx, max_cx))

    def draw(self):
        self.background.draw(self.screen)
        self.level.draw(self.screen, self.camera_x)
        for tile in self.ground_rects:
            tile_copy = tile.copy()
            tile_copy.x -= self.camera_x
            pygame.draw.rect(self.screen, COLOR_PLATFORM, tile_copy)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, (sprite.rect.x - self.camera_x, sprite.rect.y))
        self.attacks.draw(self.screen)
