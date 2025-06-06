import pygame
import random
from config import FONT_PATH, COLOR_TERMINAL

PROMPT = "hackerman@debian:~$"

class TerminalBackground:
    def __init__(self, width, height, font, command_file, ground_top):
        self.width = width
        self.height = height
        self.font = font
        self.line_height = font.get_linesize()
        self.terminal_height = ground_top
        self.num_lines = (self.terminal_height - 10) // self.line_height
        self.commands = self.load_commands(command_file)
        self.lines = [self._get_random_line() for _ in range(self.num_lines - 1)]
        self.last_cursor_switch = pygame.time.get_ticks()
        self.cursor_visible = True

    def load_commands(self, filename):
        with open(filename, encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines

    def _get_random_line(self):
        return random.choice(self.commands) if self.commands else ""

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_cursor_switch > 500:
            self.cursor_visible = not self.cursor_visible
            self.last_cursor_switch = now

    def draw(self, surface):
        surface.fill((0, 0, 0))
        for i, line in enumerate(self.lines):
            text = f"{PROMPT} {line}"
            txt = self.font.render(text, False, COLOR_TERMINAL)
            surface.blit(txt, (10, i * self.line_height))
        # prompt z kursorem na ostatniej linii
        cursor = "_" if self.cursor_visible else " "
        prompt_line = f"{PROMPT} {cursor}"
        prompt_y = (self.num_lines - 1) * self.line_height
        txt = self.font.render(prompt_line, False, COLOR_TERMINAL)
        surface.blit(txt, (10, prompt_y))
