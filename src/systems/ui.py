import sys
from turtledemo.nim import COLOR

import pygame
from pygame.event import set_keyboard_grab

from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_PATH, PLAYER, TILE_SIZE, COLORS, FONT_SIZE_XL, FONT_SIZE_M, \
    FONT_SIZE_L, GAMEOVER_DELAY, FONT_SIZE_XS, PADDING, BAR_W, BAR_H


class MainMenu:
    def __init__(self, screen, music_controller, sfx_controller):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_PATH, 28)
        self.big_font = pygame.font.Font(FONT_PATH, 48)
        self.input_box = pygame.Rect(250, 220, 300, 40)
        self.player_name = ""
        self.music = music_controller
        self.sfx = sfx_controller
        self.music_on = True
        self.sound_on = True
        self.active = False
        self.selected = 0  # 0: Nick, 1: Avatar 2: Muzyka, 3: Dźwięki, 4: Start, 5: Wyjdź
        self.running = True
        self.sprite_keys = list(PLAYER.keys())
        self.sprite_map = PLAYER
        self.sprite_list = [info["image"] for info in PLAYER.values()]
        self.sprite_idx = 0

    def draw(self):
        # tytuł
        self.screen.fill((0, 0, 0))
        title = self.big_font.render("Hackerman vs Bugzilla", True, (0, 255, 0))
        self.screen.blit(title, (80, 60))

        # ksywka
        if self.selected == 0:
            label = self.font.render("Nazwa gracza:", True, (0, 255, 0))
        else:
            label = self.font.render("Nazwa gracza:", True, (160, 160, 160))

        self.screen.blit(label, (250, 180))
        pygame.draw.rect(self.screen, (30, 30, 30), self.input_box, border_radius=6)

        # zmiana koloru ramki jeżeli jest pusty nick
        if not len(self.player_name) == 0:
            if self.active:
                color = (0, 255, 0)
                # print("COŚ JEST, AKTYWNY: " + str(color))
            else:
                color = (100, 100, 100)
                # print("COŚ JEST, NIEAKTYWNY: " + str(color))
        else:
            if self.active:
                color = (0, 255, 0)
                # print("PUSTY, AKTYWNY: " + str(color))
            else:
                color = (255, 0, 0)
                # print("PUSTY, NIEAKTYWNY: " + str(color))

        pygame.draw.rect(self.screen, color, self.input_box, 2, border_radius=6)

        # color = (0, 255, 0) if self.active else (100, 100, 100)
        # pygame.draw.rect(self.screen, color, self.input_box, 2, border_radius=6)

        txt_surface = self.font.render(self.player_name or "Twoja ksywka...", True, color)

        # avatar
        key = self.sprite_keys[self.sprite_idx]
        path = self.sprite_map[key]["image"]
        color = COLORS["green"] if self.selected == 1 else COLORS["dark_grey"]
        label = self.font.render("Avatar:", True, color)
        self.screen.blit(label, (250, 290))
        # podgląd grafiki
        surf = pygame.image.load(path).convert_alpha()
        surf = pygame.transform.scale(surf, (TILE_SIZE, TILE_SIZE))
        # ramka jeśli wybrany
        preview_rect = pygame.Rect(400, 290 - TILE_SIZE/4, TILE_SIZE, TILE_SIZE)
        self.screen.blit(surf, preview_rect.topleft)
        if self.selected == 1:
            pygame.draw.rect(self.screen, COLORS["green"], preview_rect, 2)

        self.screen.blit(txt_surface, (self.input_box.x + 8, self.input_box.y + 5))

        # opcje menu
        options = [
            f"Muzyka: {'Włączona' if self.music_on else 'Wyłączona'}",
            f"Dźwięki: {'Włączone' if self.sound_on else 'Wyłączone'}",
            "Start gry",
            "Wyjdź"
        ]
        for i, option in enumerate(options):
            color = COLORS["green"] if self.selected == i + 2 else COLORS["dark_grey"]
            surf = self.font.render(option, True, color)
            self.screen.blit(surf, (250, 340 + 45 * i))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.music.handle_event(event)
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    self.sfx.play("menu")
                    if self.active:
                        if event.key == pygame.K_RETURN:
                            self.active = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        elif len(self.player_name) < 16 and event.unicode.isprintable():
                            self.player_name += event.unicode
                    else:
                        if event.key in [pygame.K_DOWN, pygame.K_TAB]:
                            self.selected = (self.selected + 1) % 6
                        if event.key == pygame.K_UP:
                            self.selected = (self.selected - 1) % 6

                        # zmiana avatara strzałka prawo/lewo
                        if self.selected == 1 and event.key == pygame.K_LEFT:
                            self.sprite_idx = (self.sprite_idx - 1) % len(self.sprite_list)
                        if self.selected == 1 and event.key == pygame.K_RIGHT:
                            self.sprite_idx = (self.sprite_idx + 1) % len(self.sprite_list)

                        if event.key == pygame.K_RETURN:
                            if self.selected == 0:
                                self.active = True
                            elif self.selected == 2:
                                self.music_on = not self.music_on
                                self.music.set_music_on(self.music_on)
                            elif self.selected == 3:
                                self.sound_on = not self.sound_on
                                self.sfx.set_sound_on(self.sound_on)
                            elif self.selected == 4:
                                if self.player_name.strip():
                                    self.running = False
                            elif self.selected == 5:
                                exit()

            self.draw()
            pygame.display.flip()
            self.clock.tick(30)


class Scoreboard:
    def __init__(self, initial_score=0, font_size=FONT_SIZE_XS):
        # ładowanie fontu
        self.font = pygame.font.Font(FONT_PATH, font_size)
        self.score = initial_score

    def add_points(self, pts):
        self.score += pts

    def reset(self):
        self.score = 0

    def draw(self, surface):
        text = f"Punkty: {self.score}"
        surf = self.font.render(text, True, COLORS["white"])
        bg_rect = surf.get_rect(topright=(SCREEN_WIDTH - PADDING, PADDING + 30)).inflate(8, 4)
        # półprzezroczyste tło
        bg = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
        bg.fill(COLORS["black_alpha"])
        surface.blit(bg, bg_rect.topright)
        txt_pos = (bg_rect.right - surf.get_width() - 4, bg_rect.y + 2)
        surface.blit(surf, txt_pos)


class HealthBar:
    def __init__(self, player):
        self.player = player
        # pozycja prawego górnego rogu
        self.pos = (SCREEN_WIDTH - PADDING - BAR_W, PADDING)

    def draw(self, surface):
        # wypełnienie tłem
        bg_surf = pygame.Surface((BAR_W, BAR_H), pygame.SRCALPHA)
        bg_surf.fill(COLORS["black_alpha"])
        surface.blit(bg_surf, self.pos)

        # oblicz % życia
        ratio = self.player.hp / self.player.max_hp
        fill_w = int(BAR_W * ratio)
        fill_rect = pygame.Rect(self.pos[0], self.pos[1], fill_w, BAR_H)
        pygame.draw.rect(surface, COLORS["red"], fill_rect)

        # obrys
        border_rect = pygame.Rect(self.pos[0], self.pos[1], BAR_W, BAR_H)
        pygame.draw.rect(surface, COLORS["white"], border_rect, 2)

class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE_XL)

    def show(self):
        # półprzezroczyste tło
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(COLORS["black"])
        self.screen.blit(overlay, (0, 0))

        # napis "Game Over"
        text = self.font.render("GAME OVER", True, COLORS["red"])
        x = (SCREEN_WIDTH - text.get_width()) // 2
        y = (SCREEN_HEIGHT - text.get_height()) // 2
        self.screen.blit(text, (x, y))
        pygame.display.flip()
        pygame.time.wait(GAMEOVER_DELAY)

class CurrentLevel:
    FONT_SIZE = 40

    def __init__(self, screen, level):
        self.screen = screen
        self.level = level

    def draw(self):
        # obecny poziom
        font = pygame.font.Font(FONT_PATH, FONT_SIZE_L)
        txt = font.render(f"Poziom: {self.level}", True, COLORS["white"])
        self.screen.blit(txt, ((SCREEN_WIDTH - txt.get_width()) // 2, 10))


class VictoryScreen:
    def __init__(self, screen, score):
        self.screen = screen
        self.score = score
        self.font  = pygame.font.Font(FONT_PATH, FONT_SIZE_XL)
        self.clock = pygame.time.Clock()

    def show(self):
        # półprzezroczyste tło
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(COLORS["black"])
        self.screen.blit(overlay, (0, 0))

        # napis "gratulacje!"
        title = self.font.render("Gratulacje! Jesteś zwycięzcą!", True, COLORS["green"])
        x = (SCREEN_WIDTH - title.get_width()) // 2
        y = (SCREEN_HEIGHT - title.get_height()) // 2 - 60
        self.screen.blit(title, (x, y))

        # napis z wynikiem
        score_font = pygame.font.Font(FONT_PATH, FONT_SIZE_L)
        score_text = score_font.render(f"Twój wynik: {self.score}", True, COLORS["white"])
        x2 = (SCREEN_WIDTH - score_text.get_width()) // 2
        y2 = y + title.get_height() + 20
        self.screen.blit(score_text, (x2, y2))

        # napis z informacją
        instr_font = pygame.font.Font(FONT_PATH, FONT_SIZE_M)
        instr = instr_font.render("Naciśnij dowolny klawisz, żeby wrócić do menu.", True, COLORS["grey"])
        x3 = (SCREEN_WIDTH - instr.get_width()) // 2
        y3 = y2 + score_text.get_height() + 20
        self.screen.blit(instr, (x3, y3))

        pygame.display.flip()

        # czekaj na dowolny klawisz
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    waiting = False
            self.clock.tick(10)


class UIManager:
    def __init__(self):
        self.clock = pygame.time.Clock()

    def draw_pause(self, screen):
        # ciemne tło
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(COLORS["black"])
        screen.blit(overlay, (0, 0))
        pause = pygame.font.Font(None, FONT_SIZE_XL).render("PAUZA", True, COLORS["yellow"])
        screen.blit(pause, ((SCREEN_WIDTH - pause.get_width()) // 2, 200))
        pygame.display.flip()

        # czekanie na ESC lub QUIT
        while True:
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    return
                elif e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.clock.tick(10)


    def draw_game_over(self, screen, hud, reset_callback, menu_callback):
        # ciemne tło
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180);
        overlay.fill(COLORS["black"])
        screen.blit(overlay, (0, 0))

        # napis game over
        go = pygame.font.Font(FONT_PATH, FONT_SIZE_XL).render("GAME OVER", True, COLORS["red"])
        screen.blit(go, ((SCREEN_WIDTH - go.get_width()) // 2, (SCREEN_HEIGHT - go.get_height()) // 2 - 60))

        # wynik
        font_med = pygame.font.Font(FONT_PATH, FONT_SIZE_L)
        score_txt = font_med.render(f"Twój wynik: {hud.score}", True, COLORS["white"])
        screen.blit(score_txt, ((SCREEN_WIDTH - score_txt.get_width()) // 2,
                                     (SCREEN_HEIGHT - score_txt.get_height()) // 2 + 20))

        # pytanie o restart
        font_sm = pygame.font.Font(FONT_PATH, FONT_SIZE_M)
        txt = font_sm.render("Czy chcesz zrestartować? (T)ak/(N)ie", True, COLORS["grey"])
        screen.blit(txt, ((SCREEN_WIDTH - txt.get_width()) // 2,
                               (SCREEN_HEIGHT - txt.get_height()) // 2 + 80))

        pygame.display.flip()

        # czekamy na decyzje
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_t:  # tak = restart
                        reset_callback()
                        return
                    elif e.key == pygame.K_n:  # nie = menu
                        menu_callback()
                        return
            self.clock.tick(10)



