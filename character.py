import pygame
from select import select

from config import TILE_SIZE
from projectile import Projectile

def crop_to_visible_area(image, tolerance=10):
    mask = pygame.mask.from_surface(image, tolerance)
    rects = mask.get_bounding_rects()
    if rects:
        crop_rect = rects[0]
        cropped = image.subsurface(crop_rect).copy()
        return cropped
    return image

def scale_to_height(image, target_height):
    w, h = image.get_size()
    scale = target_height / h
    new_w = int(w * scale)
    return pygame.transform.scale(image, (new_w, target_height))

class Character(pygame.sprite.Sprite):
    def __init__(self, image, pos, speed=4, controllable=False):
        super().__init__()
        # Wczytanie i obrobienie grafiki postaci
        raw = pygame.image.load(image).convert_alpha()
        cropped = crop_to_visible_area(raw)
        scaled = scale_to_height(cropped, TILE_SIZE)

        # Odbicie grafiki
        self.image_right = scaled
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right

        # Pozycja
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        # Atrybuty
        self.speed = speed
        self.velocity = pygame.math.Vector2(0, 0)
        self.gravity = 0.7
        self.attack_cooldown = 0
        self.jump_strength = -12
        self.facing_right = True
        self.on_ground = False
        self.controllable = controllable
        self.direction = 1 if self.facing_right else -1


    # Ograniczenie prędkości spadania
    def apply_gravity(self):
        self.velocity.y += self.gravity
        if self.velocity.y > 10:
            self.velocity.y = 10

    # Obsługa klawiatury
    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        match keys:
            case pygame.K_LEFT:
                self.velocity.x = -self.speed
                if self.facing_right:
                    self.facing_right = False
                    self.image = self.image_left
            case pygame.K_RIGHT:
                self.velocity.x = self.speed
                if not self.facing_right:
                    self.facing_right = True
                    self.image = self.image_right
            case pygame.K_UP if self.on_ground:
                self.velocity.y = self.jump_strength
            case pygame.K_SPACE if self.attack_cooldown <= 0:
                self.attack_cooldown = 20

    # Wykrywanie kolizji
    def collide(self, tiles, direction):
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile):
                if direction == 'x':
                    if self.velocity.x > 0:
                        self.rect.right = tile.left
                    elif self.velocity.x < 0:
                        self.rect.left = tile.right
                elif direction == 'y':
                    if self.velocity.y > 0:
                        self.rect.bottom = tile.top
                        self.velocity.y = 0
                        self.on_ground = True
                    elif self.velocity.y < 0:
                        self.rect.top = tile.bottom
                        self.velocity.y = 0
    # Dodanie strzelania
    def shoot(self):
        x, y = self.rect.center
        direction = 1 if self.facing_right else -1
        return Projectile(x, y, direction)



    # Odświeżanie postaci
    def update(self, tiles):
        if self.controllable:
            self.handle_input()
            self.apply_gravity()
            self.rect.x += self.velocity.x
            self.collide(tiles, 'x')
            self.rect.y += self.velocity.y
            self.collide(tiles, 'y')
        else:
            self.apply_gravity()
            self.rect.x += self.direction * self.speed
            for tile in tiles:
                if self.rect.colliderect(tile):
                    if self.direction > 0:
                        self.rect.right = tile.left
                    else:
                        self.rect.left = tile.right
                    self.direction *= -1



