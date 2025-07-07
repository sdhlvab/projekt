import glob
import os
import re

import pygame

from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, LEVEL_DIR, LEVEL_FILE, CMD_FILE, FONT_PATH
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.systems.level import Level
from src.systems.camera import Camera
from src.systems.background import TerminalBackground
from src.systems.ui import MainMenu, Scoreboard, HealthBar, CurrentLevel, UIManager, VictoryScreen
from src.systems.collision_engine import CollisionEngine
from src.entities.coin import Coin
from src.systems.audio import Music, Sound

class Engine:
    def __init__(self, screen, player_name="", music_on=True, sound_on=True):
        """Przygotowuje całą grę: stany, audio, poziom, sprite’y, UI, kolizje itp."""
        # … tu wklejasz i dostosowujesz _tylko_ body __init__ z klasy Game
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.player_name = player_name
        self.level_file = os.path.join(LEVEL_DIR, LEVEL_FILE)

        # grafika gracza
        self.selected_img = "player1"

        # audio
        self.music_on = music_on
        self.sound_on = sound_on
        self.music = Music(self.music_on)
        if self.music_on:
            self.music.play()
        self.sfx = Sound(self.sound_on)

        # początkowy stan gry
        self.state = "PLAY"
        self.menu = MainMenu(self.screen, self.music, self.sfx)
        self.current_level = 1

        self.font = pygame.font.Font(FONT_PATH, 18)
        self.command_file = CMD_FILE

        # poziom i kafelki
        self.level = Level(self.level_file)
        self.ground_rects = self.level.get_ground_rects()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        # obliczanie maksymalnego poziomu na podstawie istniejących plików z poziomami
        pattern = os.path.join(LEVEL_DIR, LEVEL_FILE.replace("1", "*"))
        levels = glob.glob(pattern)
        self.max_level = len(levels)

        # pozycja startowa gracza z pliku
        px, py = self.level.get_player_spawn()
        self.player = Player((px, py), image_path = self.selected_img, sfx = self.sfx)
        #self.all_sprites = pygame.sprite.Group(self.player)

        # dodanie przeciwników z pliku
        for ex, ey in self.level.get_enemy_spawns():
            self.enemies.add(Enemy((ex, ey)))

        # "monety"
        self.coins = pygame.sprite.Group()
        for cx, cy in self.level.get_coin_spawns():
            self.coins.add(Coin(cx, cy))

        # kamera
        self.camera = Camera(self.level.pixel_width, self.level.pixel_height, SCREEN_WIDTH, SCREEN_HEIGHT)

        # terminal w tle (wywołanie bez przesunięcia)
        self.terminal_bg = TerminalBackground(SCREEN_WIDTH, SCREEN_HEIGHT, self.font, self.command_file, SCREEN_HEIGHT , self.player_name)

        # UI
        self.hud = Scoreboard()
        self.collision_engine = CollisionEngine(self.hud, points_per_kill=100, sfx=self.sfx)
        self.health_bar = HealthBar(self.player)
        self.clvl = CurrentLevel(self.screen, self.current_level)
        #self.victory = VictoryScreen

        # utwórz UIManager:
        self.ui = UIManager()

    def run(self):
        """Główna pętla gry: eventy, update, draw, stany."""
        while self.running and self.state != "EXIT":
            self.clock.tick(FPS)
            events = pygame.event.get()

            # 1) obsługa eventów (QUIT, ESC, strzały, muzyka)
            self.handle_events(events)

            # 2) logika gry / aktualizacje / przejścia stanów MENU, PLAY, PAUSE, VICTORY
            if self.state == "MENU":
                self.menu.run()
                self.reset(full_reset=True)
                self.state = "PLAY"
                continue

            if self.state == "PLAY":
                self.update()
                if self.player.hp <= 0:
                    self.sfx.play("dead")
                    self.state = "GAME_OVER"
                    continue

            elif self.state == "PAUSE":
                self.draw()
                self.ui.draw_pause(self.screen)
                continue

            elif self.state == "GAME_OVER":
                self.ui.draw_game_over(
                    self.screen,
                    self.hud,
                    reset_callback=lambda: self.reset(full_reset=True),
                    menu_callback=lambda: (
                        setattr(self, "current_level", 1),
                        setattr(self, "level_file", os.path.join(LEVEL_DIR, LEVEL_FILE)),
                        setattr(self, "clvl", CurrentLevel(self.screen, 1)),
                        setattr(self, "state", "MENU")
                    )
                )

                continue

            elif self.state == "VICTORY":
                VictoryScreen(self.screen, self.hud.score).show()
                #self.victory.show()
                self.reset(full_reset=True)
                self.state = "MENU"
                continue

            # 3) rysowanie i flip
            self.draw()

        pygame.quit()

    def handle_events(self, events):
        # wklej tu całą logikę z Game.handle_events oraz obsługę QUIT i ESC z Game.run
        for e in events:

            if e.type == pygame.QUIT:
                self.running = False
                self.state = "EXIT"

            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                if self.state == "PLAY":
                    self.state = "PAUSE"
                elif self.state == "PAUSE":
                    self.state = "PLAY"

            else:
                new_proj = self.player.handle_event(e)
                if new_proj:
                    self.projectiles.add(new_proj)
            self.music.handle_event(e)

    def update(self):
        # wykrycie dotknięcia L (exit_tile)
        self.player.update(pygame.key.get_pressed(), self.ground_rects)
        for rect in self.level.get_exit_rects():
            if self.player.rect.colliderect(rect):
                if self.next_level():
                    return
                else:
                    # ostatni poziom ukończony
                    pygame.mixer.music.pause()
                    self.sfx.play("win")
                    self.state = "VICTORY"
                    return
                self.state = "GAME_OVER"
                return

        # wykrycie zderzenia z monetami
        hits = pygame.sprite.spritecollide(self.player, self.coins, True)
        if hits:
            self.sfx.play("coin")
            self.hud.add_points(10)
            # bonus za zebranie wszystkich monet
            if not self.coins:
                self.sfx.play("powerup")
                self.hud.add_points(1000)

        # wrogowie odbijają się od wszystkich kfelków
        all_solid = self.ground_rects + self.level.get_exit_rects()
        self.enemies.update(all_solid)

        self.projectiles.update(self.level.get_ground_rects())

        self.camera.update(self.player.rect)
        self.terminal_bg.update()

        self.collision_engine.handle_hits(self.projectiles, self.enemies)
        self.collision_engine.handle_player_collisions(self.player, self.enemies)

        self.clvl.draw()

    def draw(self):
        # tło terminala (nie podlega kamerze)
        self.terminal_bg.draw(self.screen, self.camera.x, self.camera.y)

        # rysuj level (kafelki)
        self.level.draw(self.screen, self.camera)
        # rysuj gracza
        self.screen.blit(self.player.image, self.camera.apply(self.player.rect))

        # rysowanie przeciwników
        for e in self.enemies: e.draw(self.screen, self.camera)
        for p in self.projectiles: self.screen.blit(p.image, self.camera.apply(p.rect))

        # rysowanie HUD'a
        self.hud.draw(self.screen)
        self.health_bar.draw(self.screen)
        self.clvl.draw()

        # rysowanie "monet"
        for coin in self.coins:
            self.screen.blit(coin.image, self.camera.apply(coin.rect))

        pygame.display.flip()

    def next_level(self):
        # przejście do kolejnego pliku levelX.txt, jeśli istnieje
        base = os.path.basename(self.level_file)
        name, ext = os.path.splitext(base)
        m = re.match(r"(.*?)(\d+)$", name)
        if not m:
            return False
        prefix, num = m.groups()
        next_num = int(num) + 1
        next_file = os.path.join(
            os.path.dirname(self.level_file),
            f"{prefix}{next_num}{ext}"
        )
        if not os.path.exists(next_file):
            return False
        self.sfx.play("levelup")
        self.level_file = next_file
        self.reset(False)
        self.current_level += 1
        self.clvl = CurrentLevel(self.screen, self.current_level)
        return True

    def reset(self, full_reset=True):
        # przywrócenie stanu początkowego gry
        # odtworzenie poziomu i kafelków
        self.level = Level(self.level_file)
        self.ground_rects = self.level.get_ground_rects()
        # wrogowie
        self.enemies = pygame.sprite.Group()
        for ex, ey in self.level.get_enemy_spawns():
            self.enemies.add(Enemy((ex, ey)))
        # pociski
        self.projectiles = pygame.sprite.Group()
        # kamera
        self.camera = Camera(self.level.pixel_width, self.level.pixel_height, SCREEN_WIDTH, SCREEN_HEIGHT)
        # monety
        self.coins = pygame.sprite.Group()
        for cx, cy in self.level.get_coin_spawns():
            self.coins.add(Coin(cx, cy))
        # reset ui(nie resetuje przy przejściu do kolejnego poziomu)
        if full_reset:
            # gracz
            px, py = self.level.get_player_spawn()
            self.player = Player((px, py), image_path=self.selected_img, sfx=self.sfx)
            self.hud.reset()
            self.health_bar = HealthBar(self.player)
        else:
            px, py = self.level.get_player_spawn()
            self.player = Player((px, py), hp=self.player.hp, image_path=self.selected_img, sfx=self.sfx)
            self.health_bar = HealthBar(self.player)
        # reset stanu i zegara
        self.clock.tick()
        self.state = "PLAY"
        # reset tła (linii komend)
        self.terminal_bg = TerminalBackground(SCREEN_WIDTH, SCREEN_HEIGHT, self.font, self.command_file, SCREEN_HEIGHT , self.player_name)
