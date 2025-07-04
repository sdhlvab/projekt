import sys
import re
import os
import pygame
import glob

from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, LEVEL_FILE, LEVEL_DIR, FONT_PATH, CMD_FILE
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.systems.level import Level
from src.systems.camera import Camera
from src.systems.background import TerminalBackground
from src.engine import Engine
from src.systems.ui import Scoreboard, HealthBar, MainMenu, CurrentLevel, VictoryScreen
from src.entities.coin import Coin
from src.systems.audio import Music, Sound


class Game:
    def __init__(self, screen, player_name="", music_on=True, sound_on=True):
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
        self.state = "MENU"
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
        self.all_sprites = pygame.sprite.Group(self.player)

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
        self.engine = Engine(self.hud, points_per_kill=100, sfx=self.sfx)
        self.health_bar = HealthBar(self.player)
        self.clvl = CurrentLevel(self.screen, self.current_level)

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
                self.music.handle_event(e)


            if self.state =="MENU":
                self.menu.player_name = self.player_name
                self.menu.active = False
                self.menu.running = True
                self.menu.run()
                self.player_name = self.menu.player_name
                self.selected_img = self.menu.sprite_keys[self.menu.sprite_idx]
                self.music_on = self.menu.music_on
                self.sound_on = self.menu.sound_on
                self.music.set_music_on(self.music_on)
                self.sfx.set_sound_on(self.sound_on)
                self.reset()
                self.player.image_path = self.selected_img
                self.state = "PLAY"
                continue

            if self.state == "PLAY":
                # normalna pętla gry
                self.handle_events(events)
                self.update()
                self.draw()
                # wykrycie przegranej
                if self.player.hp <= 0:
                    self.sfx.play("dead")
                    self.state = "GAME_OVER"
                    continue
                # # wykrycie wygranej - ukończenie wszystkich poziomów
                # if self.current_level >self.max_level:
                #     self.sfx.play("win")
                #     self.state = "VICTORY"
                #     continue

            if self.state == "VICTORY":
                vs = VictoryScreen(self.screen, self.hud.score)
                vs.show()
                pygame.mixer.stop()
                pygame.mixer.music.unpause()
                # reset do menu
                self.current_level = 1
                self.level_file = os.path.join(LEVEL_DIR, LEVEL_FILE)
                self.clvl = CurrentLevel(self.screen, self.current_level)
                self.state = "MENU"
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
            self.music.handle_event(event)

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

        #self.enemies.update(self.ground_rects)
        # wrogowie odbijają się od wszystkich kfelków
        all_solid = self.ground_rects + self.level.get_exit_rects()
        self.enemies.update(all_solid)

        self.projectiles.update(self.level.get_ground_rects())

        self.camera.update(self.player.rect)
        self.terminal_bg.update()

        self.engine.handle_hits(self.projectiles, self.enemies)
        self.engine.handle_player_collisions(self.player, self.enemies)

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

        # prosta pauza
    def _draw_pause(self):
        # ciemne tło
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        pause = pygame.font.Font(None, 72).render("PAUZA", True, (255, 255, 0))
        self.screen.blit(pause, ((SCREEN_WIDTH - pause.get_width()) // 2, 200))
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

        # czekamy na decyzje
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
                        self.current_level= 1
                        self.level_file = os.path.join(LEVEL_DIR, LEVEL_FILE)
                        self.clvl = CurrentLevel(self.screen, self.current_level)
                        self.state = "MENU"
                        waiting = False
            self.clock.tick(10)

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
