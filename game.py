import pygame
from config import TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT
from level import Level
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
        self.ground_rects = self.level.get_ground_rects()
        self.terminal_bg = TerminalBackground(WINDOW_WIDTH, WINDOW_HEIGHT // 3)  # górna część terminala
        self.camera_offset = 0

        # Start Hackermana na najniższej podłodze przy lewej ścianie!
        spawn_x, spawn_y = self.level.get_player_spawn()
        self.player = Player((spawn_x, spawn_y))

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.enemies = pygame.sprite.Group()
        for ex, ey in self.level.get_enemy_spawns():
            self.enemies.add(Enemy(ex * TILE_SIZE, ey * TILE_SIZE + TILE_SIZE - 64))  # Dodajemy żeby stała na podłodze

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def update(self):
        self.all_sprites.update(self.ground_rects)
        self.enemies.update(self.ground_rects)
        # Kamera podąża za graczem
        self.camera_offset = max(0, self.player.rect.centerx - WINDOW_WIDTH // 2)

    def draw(self):
        # 1. Terminal w tle
        self.terminal_bg.draw(self.screen, offset_x=self.camera_offset)

        # 2. Rysuj mapę z przesunięciem kamery
        self.level.draw(self.screen, offset_x=self.camera_offset)

        # 3. Sprity
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, (sprite.rect.x - self.camera_offset, sprite.rect.y))
        for enemy in self.enemies:
            self.screen.blit(enemy.image, (enemy.rect.x - self.camera_offset, enemy.rect.y))
