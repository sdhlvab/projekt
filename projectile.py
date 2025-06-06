import pygame
from config import DISK_IMG

class Disk(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        img = pygame.image.load(DISK_IMG).convert_alpha()
        self.image_right = pygame.transform.scale(img, (32, 32))
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right if direction == 1 else self.image_left
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 12

    def update(self, camera_x):
        self.rect.x += self.speed * self.direction
        if self.rect.right < 0 or self.rect.left > 2000:
            self.kill()
