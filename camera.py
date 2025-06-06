# camera.py
from config import WINDOW_WIDTH, WINDOW_HEIGHT
import pygame

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, target):
        return target.rect.move(-self.camera.x, -self.camera.y)

    def update(self, target):
        x = target.rect.centerx - WINDOW_WIDTH // 2
        y = target.rect.centery - WINDOW_HEIGHT // 2

        x = max(0, min(x, self.width - WINDOW_WIDTH))
        y = max(0, min(y, self.height - WINDOW_HEIGHT))

        self.camera = pygame.Rect(x, y, self.width, self.height)
