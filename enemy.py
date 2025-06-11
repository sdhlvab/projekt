import pygame
from select import select

from config import TILE_SIZE

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        image = pygame.image.load("assets/img/bugzilla.png").convert_alpha()
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))  # <-- KLUCZ!
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = pygame.math.Vector2(0, 0)
        self.gravity = 0.7
        self.direction = 1
        self.speed = 2
        self.on_ground = False

    def update(self, ground_rects):
        # self.rect.x += self.direction * self.speed
        # self.apply_gravity()
        # if self.on_ground:
        #     self.velocity.x = self.direction * self.speed
        # else:
        #     self.velocity.x = 0
        # # Odbijaj się od krawędzi/ścian
        # for tile in ground_rects:
        #     if self.rect.colliderect(tile):
        #         if self.direction > 0:
        #             self.rect.right = tile.left
        #         else:
        #             self.rect.left = tile.right
        #         self.direction *= -1

        if self.on_ground:
            self.velocity.x = self.direction * self.speed
        else:
            self.velocity.x = 0

        self.apply_gravity()

        self.rect.x += self.velocity.x
        for tile in ground_rects:
            if self.rect.colliderect(tile):
                if self.velocity.x > 0:
                    self.rect.right = tile.left
                    self.direction *= -1
                elif self.velocity.x < 0:
                    self.rect.left = tile.right
                    self.direction *= -1

        self.rect.y += self.velocity.y
        self.on_ground = False
        for tile in ground_rects:
            if self.rect.colliderect(tile):
                if self.velocity.y > 0:
                    self.rect.bottom = tile.top
                    self.velocity.y = 0
                    self.on_ground = True
                elif self.velocity.y < 0:
                    self.rect.top = tile.bottom
                    self.velocity.y = 0

    def apply_gravity(self):
        self.velocity.y += self.gravity
        if self.velocity.y > 10:
            self.velocity.y = 10