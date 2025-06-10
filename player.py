import pygame
from config import TILE_SIZE, PLAYER_IMAGE

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

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        raw = pygame.image.load(PLAYER_IMAGE).convert_alpha()
        cropped = crop_to_visible_area(raw)
        scaled = scale_to_height(cropped, TILE_SIZE)
        self.base_image = crop_to_visible_area(pygame.image.load(PLAYER_IMAGE).convert_alpha())
        #self.base_image = scale_to_height(self.base_image, TILE_SIZE)
        #self.image_right = pygame.transform.scale(self.base_image, (TILE_SIZE, TILE_SIZE))  # <-- KLUCZ!
        self.image_right = scaled
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.speed = 4
        self.jump_strength = -12
        self.velocity = pygame.math.Vector2(0, 0)
        self.gravity = 0.7
        self.on_ground = False
        self.facing_right = True

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
            if self.facing_right:
                self.facing_right = False
                self.image = self.image_left
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            if not self.facing_right:
                self.facing_right = True
                self.image = self.image_right
        if keys[pygame.K_UP] and self.on_ground:
            self.velocity.y = self.jump_strength

    def apply_gravity(self):
        self.velocity.y += self.gravity
        if self.velocity.y > 12:
            self.velocity.y = 12

    def update(self, tiles):
        self.handle_input()
        self.apply_gravity()
        self.rect.x += self.velocity.x
        self.collide(tiles, 'x')
        self.rect.y += self.velocity.y
        self.collide(tiles, 'y')

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

    def shoot(self, group):
        from projectile import Projectile
        x, y = self.rect.center
        direction = 1 if self.facing_right else -1
        proj = Projectile(x, y, direction=direction)
        group.add(proj)
