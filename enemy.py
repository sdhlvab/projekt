# enemy.py

import pygame
from config import TILE_SIZE, BUGZILLA_IMG

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path=BUGZILLA_IMG, speed=2):
        super().__init__()
        raw = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(raw, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.direction = 1  # 1 = prawo, -1 = lewo

    def update(self, ground_rects):
        # Prosty patrol lewo-prawo po platformie
        self.rect.x += self.direction * self.speed
        # Zmień kierunek na krawędzi ekranu/mapy
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = 1
        if self.rect.right > 3000:  # <-- ustaw max szerokość planszy (albo podmień na Level.width*TILE_SIZE)
            self.rect.right = 3000
            self.direction = -1
        # Trzymaj na ziemi!
        if ground_rects:
            hits = [tile for tile in ground_rects if self.rect.colliderect(tile.move(0, 1))]
            if hits:
                self.rect.bottom = hits[0].top
            else:
                self.rect.y += 5  # spadaj jeśli nie stoisz na ziemi
