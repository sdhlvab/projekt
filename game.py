import pygame
import os

from pygame.examples.midi import key_images

from config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, LEVEL_FILE, PLAYER_IMAGE, ENEMY_IMAGE
from player import Player
from enemy import Enemy
from level import Level
from camera import Camera
from background import TerminalBackground
from engine import Engine
from ui import Scoreboard, HealthBar

class Game:
    def __init__(self, screen, player_name="hackerman", music_on=True, sound_on=True):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.player_name = player_name

        self.state = "PLAY"

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
        self.engine = Engine(self.hud, points_per_kill=100)
        self.health_bar = HealthBar(self.player)

    def run(self):
        while self.running and self.state != "EXIT":
            self.clock.tick(60)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                    self.state = "EXIT"
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    if self.state == "PLAY":
                        self.state = "PAUSE"
                    elif self.state == "PAUSE":
                        self.state = "PLAY"

            if self.state == "MENU":
                keys = pygame.key.get_pressed()
                #enter ptrzechfi do gry
                # ENTER przechodzi do gry
                +
                if keys[pygame.K_RETURN]:
                    +                    self.state = "PLAY"
                +                self._draw_menu()
                +
                continue
                +
                +
                if self.state == "PLAY":
                    +  # normalna pętla gry
                +                self.handle_events()
                +                self.update()
                +                self.draw()
                +  # wykrycie przegranej
                +
                if self.player.hp <= 0:
                    +                    self.state = "GAME_OVER"
                +
                continue
                +
                +
                if self.state == "PAUSE":
                    +  # rysujemy pauzę, ale nie update’ujemy świata
                +                self.draw()  # rysujemy świat, żeby mieć tło
                +                self._draw_pause()
                +
                continue
                +
                +
                if self.state == "GAME_OVER":
                    +                self._draw_game_over()
                +  # petla się zakończy przez state=="EXIT"
                +
                continue
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

        self.projectiles.update(self.level.get_ground_rects())

        self.camera.update(self.player.rect)
        self.terminal_bg.update()

        self.engine.handle_hits(self.projectiles, self.enemies)
        self.engine.handle_player_collisions(self.player, self.enemies)

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
        self.health_bar.draw(self.screen)
        pygame.display.flip()

    # Prosste menu
    def _draw_menu(self):
        # tu np. prosty napis „PRESS ENTER TO START”
        font = pygame.font.Font(None, 48)
        txt = font.render("Press ENTER to Start", True, (0, 255, 0))
        x = (SCREEN_WIDTH - txt.get_width()) // 2
        y = (SCREEN_HEIGHT - txt.get_height()) // 2
        self.screen.fill((0, 0, 0))
        self.screen.blit(txt, (x, y))
        pygame.display.flip()

        # prosta pauza
    def _draw_pause(self):
        pause = pygame.font.Font(None, 72).render("PAUSE", True, (255, 255, 0))
        self.screen.blit(pause, ((SCREEN_WIDTH - pause.get_width()) // 2, 20))
        pygame.display.flip()

    def _draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180);
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        go = pygame.font.Font(None, 72).render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(go, ((SCREEN_WIDTH - go.get_width()) // 2, (SCREEN_HEIGHT - go.get_height()) // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        self.state = "EXIT"