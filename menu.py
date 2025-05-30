import pygame
import os

class Menu:
    def __init__(self, screen):
        self.screen = screen
        font_path = os.path.join("assets", "fonts", "UbuntuMono-R.ttf")
        self.font = pygame.font.Font(font_path, 32)
        self.nick = ""
        self.nick_active = True
        self.menu_music_on = True
        self.menu_sound_on = True
        self.clock = pygame.time.Clock()

        # Ładuj muzykę (opcjonalnie)
        music_path = os.path.join("assets", "sound", "menu_music.ogg")
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)
        else:
            print("Menu music not found:", music_path)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and self.nick_active:
                    if event.key == pygame.K_RETURN and self.nick.strip():
                        pygame.mixer.music.stop()
                        return {
                            "nick": self.nick,
                            "music": self.menu_music_on,
                            "sound": self.menu_sound_on
                        }
                    elif event.key == pygame.K_BACKSPACE:
                        self.nick = self.nick[:-1]
                    elif len(self.nick) < 15 and event.unicode.isprintable():
                        self.nick += event.unicode
                if event.type == pygame.KEYDOWN and not self.nick_active:
                    if event.key == pygame.K_m:
                        self.menu_music_on = not self.menu_music_on
                        if self.menu_music_on:
                            pygame.mixer.music.play(-1)
                        else:
                            pygame.mixer.music.stop()
                    if event.key == pygame.K_s:
                        self.menu_sound_on = not self.menu_sound_on

            self.draw()
            self.clock.tick(30)

    def draw(self):
        self.screen.fill((20, 20, 20))
        title = self.font.render("Hackerman vs. Bugzilla", True, (0, 255, 0))
        self.screen.blit(title, (100, 70))

        prompt = self.font.render("Podaj nick i Enter, by zacząć:", True, (255, 255, 255))
        self.screen.blit(prompt, (100, 200))

        nicktxt = self.font.render(self.nick + "|", True, (0, 255, 0))
        self.screen.blit(nicktxt, (100, 250))

        mus = "Muzyka: ON (M)" if self.menu_music_on else "Muzyka: OFF (M)"
        snd = "Dźwięki: ON (S)" if self.menu_sound_on else "Dźwięki: OFF (S)"
        mus_surface = self.font.render(mus, True, (0,255,0) if self.menu_music_on else (120,120,120))
        snd_surface = self.font.render(snd, True, (0,255,0) if self.menu_sound_on else (120,120,120))
        self.screen.blit(mus_surface, (100, 330))
        self.screen.blit(snd_surface, (100, 370))

        instr = self.font.render("M - przełącz muzykę | S - przełącz dźwięki", True, (180, 180, 180))
        self.screen.blit(instr, (100, 420))

        pygame.display.flip()
