import pygame
import os
from background import TerminalBackground
from player import Player
from enemy import Enemy
from projectile import Projectile

class Game:
    def __init__(self, screen, player_name="hackerman", music_on=True, sound_on=True):
        self.screen = screen
        self.running = True
        font_path = os.path.join("assets", "fonts", "UbuntuMono-R.ttf")
        self.font = pygame.font.Font(font_path, 18)

        self.ground_rects = [
            pygame.Rect(0, 550, 800, 50),  # ziemia
        ]
        ground_rect = self.ground_rects[0]
        self.player_name = player_name
        self.music_on = music_on
        self.sound_on = sound_on

        # TerminalBackground z nickiem!
        self.background = TerminalBackground(
            800, 600, self.font, "assets/data/commands.txt", ground_rect.top, self.player_name
        )

        self.player = Player((100, 486))
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Enemy(300, ground_rect))

        self.projectiles = pygame.sprite.Group()
        self.shoot_cooldown = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and self.shoot_cooldown == 0:
                projectile = self.player.shoot()
                self.projectiles.add(projectile)
                self.shoot_cooldown = 15 # cooldown

    def update(self):
        self.background.update()
        self.all_sprites.update(self.ground_rects)
        for enemy in self.enemies:
            enemy.update(self.ground_rects)

        self.projectiles.update()

        #cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # kolizje pocisków z wrogami
        for projectile in self.projectiles:
            hits = pygame.sprite.spritecollide(projectile, self.enemies, True)
            if hits:
                projectile.kill() # płyta znika po trafieniu

    def draw(self):
        self.background.draw(self.screen)
        for tile in self.ground_rects:
            pygame.draw.rect(self.screen, (50, 50, 50), tile)
        self.all_sprites.draw(self.screen)
        self.enemies.draw(self.screen)

        self.projectiles.draw(self.screen)
