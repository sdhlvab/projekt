import pygame
from config import *
from player import Player
from enemy import Enemy
from ui import draw_ui

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Hackerman vs. Bugzilla")
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player(100, HEIGHT // 2)
        self.enemies = [Enemy(WIDTH - 150, HEIGHT // 2)]
        self.font = pygame.font.SysFont(None, 30)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)

    def update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update(self.player.rect)

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        draw_ui(self.screen, self.player, self.font)
        pygame.display.flip()
