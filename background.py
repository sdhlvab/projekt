import pygame

class TerminalBackground:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.Font("assets/fonts/UbuntuMono-R.ttf", 20)
        self.lines = [
            "hackerman@debian:~$ cd /home/hackerman/dev/",
            "hackerman@debian:~$ sudo apt install python3-pygame",
            # ... możesz ładować z pliku!
        ]

    def draw(self, surface, offset_x=0):
        bg = pygame.Surface((self.width, self.height))
        bg.fill((0, 0, 0))
        for i, line in enumerate(self.lines):
            txt = self.font.render(line, True, (0, 255, 0))
            bg.blit(txt, (10, i * 22))
        surface.blit(bg, (-offset_x // 6, 0))  # Parallax: tło przesuwa się wolniej
