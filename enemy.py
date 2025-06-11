import pygame

from character import (Character)
from config import TILE_SIZE, ENEMY_IMAGE

class Enemy(Character):
    def __init__(self, pos):
        image = pygame.image.load(ENEMY_IMAGE).convert_alpha()
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))  # <-- KLUCZ!
        super().__init__(image, pos)
        self.direction = 1

    def update(self, tiles):
        if self.on_ground:
            self.velocity.x = self.direction * self.speed
        else:
            self.velocity.x = 0

        self.apply_gravity()
        self.move_collide(tiles)


# import pygame
#
# from config import TILE_SIZE
#
# class Enemy(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         image = pygame.image.load("assets/img/bugzilla.png").convert_alpha()
#         image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))  # <-- KLUCZ!
#         self.image = image
#         self.max_hp = 100
#         self.hp = self.max_hp
#         self.show_hp_time = 0
#         self.def_show_hp_time = 1000 #czas pokazywania paska życia w ms
#         self.rect = self.image.get_rect(topleft=(x, y))
#         self.velocity = pygame.math.Vector2(0, 0)
#         self.gravity = 0.7
#         self.direction = 1
#         self.speed = 2
#         self.on_ground = False
#
#     def update(self, ground_rects):
#         if self.on_ground:
#             self.velocity.x = self.direction * self.speed
#         else:
#             self.velocity.x = 0
#
#         self.apply_gravity()
#
#         self.rect.x += self.velocity.x
#         for tile in ground_rects:
#             if self.rect.colliderect(tile):
#                 if self.velocity.x > 0:
#                     self.rect.right = tile.left
#                     self.direction *= -1
#                 elif self.velocity.x < 0:
#                     self.rect.left = tile.right
#                     self.direction *= -1
#
#         self.rect.y += self.velocity.y
#         self.on_ground = False
#         for tile in ground_rects:
#             if self.rect.colliderect(tile):
#                 if self.velocity.y > 0:
#                     self.rect.bottom = tile.top
#                     self.velocity.y = 0
#                     self.on_ground = True
#                 elif self.velocity.y < 0:
#                     self.rect.top = tile.bottom
#                     self.velocity.y = 0
#
#     def apply_gravity(self):
#         self.velocity.y += self.gravity
#         if self.velocity.y > 10:
#             self.velocity.y = 10
#
#     def take_damage(self, damage):
#         self.hp -= damage
#         self.show_hp_time = pygame.time.get_ticks() + self.def_show_hp_time
#         if self.hp <= 0:
#             self.kill()