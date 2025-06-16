import sys
from time import sleep

import pygame
import os

from select import select

from config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, LEVEL_FILE, PLAYER_IMAGE, ENEMY_IMAGE
from player import Player
from enemy import Enemy
from level import Level
from camera import Camera
from background import TerminalBackground
from engine import Engine
from ui import Scoreboard, HealthBar, MainMenu


class Game:
    def __init__(self, screen, player_name="", music_on=True, sound_on=True):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.player_name = player_name

        # początkowy stan gry
        self.state = "PLAY"
        self.menu = MainMenu(self.screen)

        font_path = os.path.join("assets", "fonts", "UbuntuMono-R.ttf")
        self.font = pygame.font.Font(font_path, 18)
        self.command_file = "assets/data/commands.txt"

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
        self.terminal_bg = TerminalBackground(SCREEN_WIDTH, SCREEN_HEIGHT, self.font, self.command_file, SCREEN_HEIGHT , self.player_name)

        # UI
        self.hud = Scoreboard()
        self.engine = Engine(self.hud, points_per_kill=100)
        self.health_bar = HealthBar(self.player)

    def reset(self):
        # przywrócenie stanu początkowego gry
        # odtworzenie poziomu i kafli
        self.level = Level(LEVEL_FILE)
        self.ground_rects = self.level.get_ground_rects()
        # gracz
        px, py = self.level.get_player_spawn()
        self.player = Player((px, py))
        # wrogowie
        self.enemies = pygame.sprite.Group()
        for ex, ey in self.level.get_enemy_spawns():
            self.enemies.add(Enemy((ex, ey)))
        # pociski
        self.projectiles = pygame.sprite.Group()
        # kamera
        self.camera = Camera(self.level.pixel_width, self.level.pixel_height, SCREEN_WIDTH, SCREEN_HEIGHT)
        # reset ui
        self.hud.reset()
        self.health_bar = HealthBar(self.player)
        # reset stanu i zegara
        self.clock.tick()
        self.state = "PLAY"
        # reset tła (linii komend)
        self.terminal_bg = TerminalBackground(SCREEN_WIDTH, SCREEN_HEIGHT, self.font, self.command_file, SCREEN_HEIGHT , self.player_name)

    def run(self):
        while self.running and self.state != "EXIT":
            self.clock.tick(60)
            events = pygame.event.get()

            for e in events:
                if e.type == pygame.QUIT:
                    self.running = False
                    self.state = "EXIT"
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    if self.state == "PLAY":
                        self.state = "PAUSE"
                    elif self.state == "PAUSE":
                        self.state = "PLAY"


            if self.state =="MENU":
                self.menu.player_name = self.player_name
                self.menu.active = False
                self.menu.run()
                self.player_name = self.menu.player_name
                self.reset()
                self.state = "PLAY"
                continue

            if self.state == "PLAY":
                # normalna pętla gry
                self.handle_events(events)
                self.update()
                self.draw()
                # wykrycie przegranej
                if self.player.hp <= 0:
                    self.state = "GAME_OVER"
                continue

            if self.state == "PAUSE":
                # pauza - rysowanie wszystkiego, ale bez update'u
                self.draw()
                self._draw_pause()
                continue

            if self.state == "GAME_OVER":
                self._draw_game_over()
                # # powrót do menu
                # self.state = "MENU"
                continue

            # self.handle_events()
            # self.update()
            # self.draw()

    def handle_events(self, events):
        for event in events:
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
        paused = True
        while paused:
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    paused = False
                    self.state = "PLAY"
                elif e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.clock.tick(10)

    def _draw_game_over(self):
        # ciemne tło
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180);
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        # napis game over
        go = pygame.font.Font(None, 72).render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(go, ((SCREEN_WIDTH - go.get_width()) // 2, (SCREEN_HEIGHT - go.get_height()) // 2 - 60))
        # wynik
        font_med = pygame.font.Font(None, 48)
        score_txt = font_med.render(f"Twój wynik: {self.hud.score}", True, (255, 255, 255))
        self.screen.blit(score_txt, ((SCREEN_WIDTH - score_txt.get_width()) // 2,
                                     (SCREEN_HEIGHT - score_txt.get_height()) // 2 + 20))
        # pytanie o restart
        font_sm = pygame.font.Font(None, 36)
        txt = font_sm.render("Czy chcesz zrestartować? (T)ak/(N)ie", True, (200, 200, 200))
        self.screen.blit(txt, ((SCREEN_WIDTH - txt.get_width()) // 2,
                               (SCREEN_HEIGHT - txt.get_height()) // 2 + 80))

        pygame.display.flip()

        #czekamy na decyzje
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_t: # tak = restart
                        self.reset()
                        self.state = "PLAY"
                        waiting = False
                    elif e.key == pygame.K_n: # nie = menu
                        self.reset()
                        self.state = "MENU"
                        waiting = False
            self.clock.tick(10)

        # pygame.time.wait(2000)
        # self.__init__(self.screen, self.player_name)
        # self.state = "MENU"