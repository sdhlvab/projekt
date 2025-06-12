import pygame
import random

from config import TILE_SIZE

PROMPT = "hackerman@debian:~$"
CURSOR_CHARS = ["_", " "]

class TerminalBackground:
    def __init__(self, width, height, font, command_file, terminal_height, player_name="aaa"):
        self.width = width
        self.height = height
        self.font = font
        self.line_height = font.get_linesize()
        self.terminal_height = terminal_height - TILE_SIZE
        self.player_name = player_name
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

    def draw(self, surface, camera_x, camera_y):
        # Terminal zawsze na górze, bez przesuwania
        surface.fill((0, 0, 0), (0, 0, self.width, self.terminal_height))
        for i, line in enumerate(self.lines):
            text = f"{PROMPT} {line}"
            txt = self.font.render(text, False, (0, 255, 0))
            surface.blit(txt, (10, i * self.line_height))
        # prompt z kursorem na ostatniej linii
        cursor = CURSOR_CHARS[0] if self.cursor_visible else CURSOR_CHARS[1]
        prompt_line = f"{PROMPT} {cursor}"
        prompt_y = (self.num_lines - 1) * self.line_height
        txt = self.font.render(prompt_line, False, (0, 255, 0))
        surface.blit(txt, (10, prompt_y))
