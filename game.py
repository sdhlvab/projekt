import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, LEVEL_FILE, PLAYER_IMAGE, ENEMY_IMAGE
from player import Player
from enemy import Enemy
from projectile import Projectile
from level import Level
from camera import Camera
from background import TerminalBackground
from character import Character
import os

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
        #self.player = Character(PLAYER_IMAGE, self.level.get_player_spawn(), speed = 7, controllable=True)
        self.all_sprites = pygame.sprite.Group(self.player)

        # Dodaj przeciwników z levela (np. 'E' w pliku)
        for ex, ey in self.level.get_enemy_spawns():
            self.enemies.add(Enemy(ex, ey))
            #self.enemies.add(Character(ENEMY_IMAGE, ((ex, ey))))

        # Kamera
        self.camera = Camera(self.level.pixel_width, self.level.pixel_height, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Terminal w tle (wywołanie bez przesunięcia)
        self.terminal_bg = TerminalBackground(SCREEN_WIDTH, SCREEN_HEIGHT, font, command_file, SCREEN_HEIGHT , player_name)

        self.shoot_cooldown = 0

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for eventG in pygame.event.get():
            if eventG.type == pygame.QUIT:
                self.running = False
            elif eventG.type == pygame.KEYDOWN:
                #print("KEYDOWN")
                if eventG.key == pygame.K_SPACE: # and self.shoot_cooldown == 0:
                    projectile = self.player.shoot()
                    self.projectiles.add(projectile)
                    self.shoot_cooldown = 15
                    #print("SPACE GAME LOOP")

    def update(self):
        #print(self.player.attack_cooldown ,'              ',self.shoot_cooldown)
        #print('EVENT.TYPE:  ', event.type)
        self.player.update(self.ground_rects)
        self.enemies.update(self.ground_rects)
        #self.projectiles.update(self.level.get_ground_rects(), self.enemies)
        self.projectiles.update()
        self.camera.update(self.player.rect)
        self.terminal_bg.update()

        #cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        #kolizje pocisków

        for projectile in self.projectiles:
            hits = pygame.sprite.spritecollide(projectile, self.enemies, True)
            if hits:
                projectile.kill()

    def draw(self):
        # Tło terminala (nie podlega kamerze)
        self.terminal_bg.draw(self.screen, self.camera.x, self.camera.y)
        # Rysuj level (kafelki)
        self.level.draw(self.screen, self.camera)
        # Rysuj gracza
        self.screen.blit(self.player.image, self.camera.apply(self.player.rect))
        # Rysuj przeciwników
        for enemy in self.enemies:
            self.screen.blit(enemy.image, self.camera.apply(enemy.rect))
        # Rysuj pociski
        for proj in self.projectiles:
            self.screen.blit(proj.image, self.camera.apply(proj.rect))
        pygame.display.flip()
