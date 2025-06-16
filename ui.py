import pygame
import os

from config import SCREEN_WIDTH, SCREEN_HEIGHT

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("assets/fonts/UbuntuMono-R.ttf", 28)
        self.big_font = pygame.font.Font("assets/fonts/UbuntuMono-R.ttf", 48)
        self.input_box = pygame.Rect(250, 220, 300, 40)
        self.player_name = ""
        self.music_on = True
        self.sound_on = True
        self.active = False
        self.selected = 0  # 0: Nick, 1: Muzyka, 2: Dźwięki, 3: Start, 4: Wyjdź
        self.running = True

    def draw(self):

        self.screen.fill((0, 0, 0))
        title = self.big_font.render("Hackerman vs. Bugzilla", True, (0, 255, 0))
        self.screen.blit(title, (80, 60))

        if self.selected == 0:
            label = self.font.render("Nazwa gracza:", True, (0, 255, 0))
        else:
            label = self.font.render("Nazwa gracza:", True, (160, 160, 160))

        self.screen.blit(label, (250, 180))
        pygame.draw.rect(self.screen, (30, 30, 30), self.input_box, border_radius=6)

        #zmiana koloru ramki jeżeli jest pusty nick
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



        self.screen.blit(txt_surface, (self.input_box.x + 8, self.input_box.y + 5))

        # Opcje menu
        options = [
            f"Muzyka: {'Włączona' if self.music_on else 'Wyłączona'}",
            f"Dźwięki: {'Włączone' if self.sound_on else 'Wyłączone'}",
            "Start gry",
            "Wyjdź"
        ]
        for i, option in enumerate(options):
            color = (0, 255, 0) if self.selected == i + 1 else (160, 160, 160)
            surf = self.font.render(option, True, color)
            self.screen.blit(surf, (250, 280 + 45 * i))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_RETURN:
                            self.active = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        elif len(self.player_name) < 16 and event.unicode.isprintable():
                            self.player_name += event.unicode
                    else:
                        if event.key in [pygame.K_DOWN, pygame.K_TAB]:
                            self.selected = (self.selected + 1) % 5
                        if event.key == pygame.K_UP:
                            self.selected = (self.selected - 1) % 5
                        if event.key == pygame.K_RETURN:
                            if self.selected == 0:
                                self.active = True
                            elif self.selected == 1:
                                self.music_on = not self.music_on
                            elif self.selected == 2:
                                self.sound_on = not self.sound_on
                            elif self.selected == 3:
                                if self.player_name.strip():
                                    self.running = False
                            elif self.selected == 4:
                                exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.active = True
                    else:
                        self.active = False
            self.draw()
            pygame.display.flip()
            self.clock.tick(30)


class Scoreboard:
    PADDING = 16
    BG_COLOR = (0, 0, 0, 180)
    TEXT_COLOR = (255, 255, 255)

    def __init__(self, initial_score=0, font_size=24, font_name="UbuntuMono-R.ttf"):
        # ładowanie fontu
        font_path = os.path.join("assets", "fonts", font_name)
        self.font = pygame.font.Font(font_path, font_size)
        self.score = initial_score

    def add_points(self, pts):
        self.score += pts

    def reset(self):
        self.score = 0

    def draw(self, surface):
        text = f"Score: {self.score}"
        surf = self.font.render(text, True, self.TEXT_COLOR)
        bg_rect = surf.get_rect(topright=(SCREEN_WIDTH - self.PADDING, self.PADDING + 30)).inflate(8, 4)
        # półprzezroczyste tło (jeśli masz display z ALPHA)
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


