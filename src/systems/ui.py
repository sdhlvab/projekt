import sys

import pygame

from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_PATH, PLAYER, TILE_SIZE


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
        color = (0, 255, 0) if self.selected == 1 else (160, 160, 160)
        label = self.font.render("Avatar:", True, color)
        self.screen.blit(label, (250, 290))
        # podgląd grafiki
        surf = pygame.image.load(path).convert_alpha()
        surf = pygame.transform.scale(surf, (TILE_SIZE, TILE_SIZE))
        # ramka jeśli wybrany
        preview_rect = pygame.Rect(400, 290 - TILE_SIZE/4, TILE_SIZE, TILE_SIZE)
        self.screen.blit(surf, preview_rect.topleft)
        if self.selected == 1:
            pygame.draw.rect(self.screen, (0, 255, 0), preview_rect, 2)

        self.screen.blit(txt_surface, (self.input_box.x + 8, self.input_box.y + 5))

        # opcje menu
        options = [
            f"Muzyka: {'Włączona' if self.music_on else 'Wyłączona'}",
            f"Dźwięki: {'Włączone' if self.sound_on else 'Wyłączone'}",
            "Start gry",
            "Wyjdź"
        ]
        for i, option in enumerate(options):
            color = (0, 255, 0) if self.selected == i + 2 else (160, 160, 160)
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
    PADDING = 16
    BG_COLOR = (0, 0, 0, 180)
    TEXT_COLOR = (255, 255, 255)

    def __init__(self, initial_score=0, font_size=24):
        # ładowanie fontu
        self.font = pygame.font.Font(FONT_PATH, font_size)
        self.score = initial_score

    def add_points(self, pts):
        self.score += pts

    def reset(self):
        self.score = 0

    def draw(self, surface):
        text = f"Punkty: {self.score}"
        surf = self.font.render(text, True, self.TEXT_COLOR)
        bg_rect = surf.get_rect(topright=(SCREEN_WIDTH - self.PADDING, self.PADDING + 30)).inflate(8, 4)
        # półprzezroczyste tło
        bg = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
        bg.fill(self.BG_COLOR)
        surface.blit(bg, bg_rect.topright)
        txt_pos = (bg_rect.right - surf.get_width() - 4, bg_rect.y + 2)
        surface.blit(surf, txt_pos)


class HealthBar:
    PADDING = 16
    BAR_W = 200
    BAR_H = 20
    BORDER_COL = (255, 255, 255)
    FILL_COL   = (200,   0,   0)
    BG_COL     = (0,     0,   0,  180)

    def __init__(self, player):
        self.player = player
        # pozycja prawego górnego rogu
        self.pos = (SCREEN_WIDTH - self.PADDING - self.BAR_W, self.PADDING)

    def draw(self, surface):
        # wypełnienie tłem
        bg_surf = pygame.Surface((self.BAR_W, self.BAR_H), pygame.SRCALPHA)
        bg_surf.fill(self.BG_COL)
        surface.blit(bg_surf, self.pos)

        # oblicz % życia
        ratio = self.player.hp / self.player.max_hp
        fill_w = int(self.BAR_W * ratio)
        fill_rect = pygame.Rect(self.pos[0], self.pos[1], fill_w, self.BAR_H)
        pygame.draw.rect(surface, self.FILL_COL, fill_rect)

        # obrys
        border_rect = pygame.Rect(self.pos[0], self.pos[1], self.BAR_W, self.BAR_H)
        pygame.draw.rect(surface, self.BORDER_COL, border_rect, 2)

class GameOverScreen:
    FONT_SIZE = 72
    OVERLAY_ALPHA = 180

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, self.FONT_SIZE)

    def show(self):
        # półprzezroczyste tło
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(self.OVERLAY_ALPHA)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # napis "Game Over"
        text = self.font.render("GAME OVER", True, (255, 0, 0))
        x = (SCREEN_WIDTH - text.get_width()) // 2
        y = (SCREEN_HEIGHT - text.get_height()) // 2
        self.screen.blit(text, (x, y))
        pygame.display.flip()
        pygame.time.wait(2000)

class CurrentLevel:
    FONT_SIZE = 40

    def __init__(self, screen, level):
        self.screen = screen
        self.level = level
        self.font = pygame.font.Font(None, self.FONT_SIZE)

    def draw(self):
        # obecny poziom
        font = pygame.font.Font(None, 48)
        txt = font.render(f"Poziom: {self.level}", True, (255, 255, 255))
        self.screen.blit(txt, ((SCREEN_WIDTH - txt.get_width()) // 2, 10))
        #pygame.display.flip()

class VictoryScreen:
    FONT_SIZE = 72
    OVERLAY_ALPHA = 180

    def __init__(self, screen, score):
        self.screen = screen
        self.score = score
        self.font  = pygame.font.Font(None, self.FONT_SIZE)
        self.clock = pygame.time.Clock()

    def show(self):
        # półprzezroczyste tło
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(self.OVERLAY_ALPHA)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # napis "gratulacje!"
        title = self.font.render("Gratulacje! Jesteś zwycięzcą!", True, (0, 255, 0))
        x = (SCREEN_WIDTH - title.get_width()) // 2
        y = (SCREEN_HEIGHT - title.get_height()) // 2 - 60
        self.screen.blit(title, (x, y))

        # napis z wynikiem
        score_font = pygame.font.Font(None, 48)
        score_text = score_font.render(f"Twój wynik: {self.score}", True, (255, 255, 255))
        x2 = (SCREEN_WIDTH - score_text.get_width()) // 2
        y2 = y + title.get_height() + 20
        self.screen.blit(score_text, (x2, y2))

        # napis z informacją
        instr_font = pygame.font.Font(None, 36)
        instr = instr_font.render("Naciśnij dowolny klawisz, żeby wrócić do menu.", True, (200, 200, 200))
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
    def draw_pause(self, screen):
        """Wyświetla overlay pauzy i czeka na ESC"""
        # ciemne tło
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        pause = pygame.font.Font(None, 72).render("PAUZA", True, (255, 255, 0))
        screen.blit(pause, ((SCREEN_WIDTH - pause.get_width()) // 2, 200))
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

        # przenieś body metody Game._draw_pause tutaj (zmień self.screen → screen,
        # a self.clock na lokalny zegar czy przekazywaną instancję, albo przechowuj clock w UIManager)

    def draw_game_over(self, screen, hud, reset_callback, menu_callback):
        """Wyświetla Game Over, wynik, pyta o T/N i wywołuje zwrotnie reset/menu"""
        # ciemne tło
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180);
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        # napis game over
        go = pygame.font.Font(None, 72).render("GAME OVER", True, (255, 0, 0))
        screen.blit(go, ((SCREEN_WIDTH - go.get_width()) // 2, (SCREEN_HEIGHT - go.get_height()) // 2 - 60))
        # wynik
        font_med = pygame.font.Font(None, 48)
        score_txt = font_med.render(f"Twój wynik: {hud.score}", True, (255, 255, 255))
        screen.blit(score_txt, ((SCREEN_WIDTH - score_txt.get_width()) // 2,
                                     (SCREEN_HEIGHT - score_txt.get_height()) // 2 + 20))
        # pytanie o restart
        font_sm = pygame.font.Font(None, 36)
        txt = font_sm.render("Czy chcesz zrestartować? (T)ak/(N)ie", True, (200, 200, 200))
        screen.blit(txt, ((SCREEN_WIDTH - txt.get_width()) // 2,
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
                    if e.key == pygame.K_t:  # tak = restart
                        #self.reset()
                        reset_callback()
                        self.state = "PLAY"
                        waiting = False
                    elif e.key == pygame.K_n:  # nie = menu
                        self.current_level = 1
                        self.level_file = os.path.join(LEVEL_DIR, LEVEL_FILE)
                        self.clvl = CurrentLevel(self.screen, self.current_level)
                        #self.state = "MENU"
                        menu_callback()
                        waiting = False
            self.clock.tick(10)
        # tu przenieś Game._draw_game_over, ale zamiast self.reset() czy sys.exit()
        # wywołuj przekazane callbacki: reset_callback(), menu_callback()



