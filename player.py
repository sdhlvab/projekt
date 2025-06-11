import pygame

from config import TILE_SIZE, PLAYER_IMAGE
from projectile import Projectile
from character import Character

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

class Player(Character):
    def __init__(self, pos):
        raw = pygame.image.load(PLAYER_IMAGE).convert_alpha()
        cropped = crop_to_visible_area(raw)
        self.image = scale_to_height(cropped, TILE_SIZE)
        self.image_right = self.image
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        super().__init__(self.image_right, pos, speed=7, max_hp=100)

        self.direction = 1 # 1 prawo, -1 lewo
        self.shoot_cooldown = 0
        self.def_shoot_cooldown = 5
        self.shoot_speed = 12
        self.shoot_damage = 10

    def update(self, keys, tiles):
        #obsługa klawiszy
        self.handle_input()

        #cooldown ataku
        if self.shoot_cooldown > 0: self.shoot_cooldown -= 1

        #fizyka
        self.apply_gravity()
        self.move_collide(tiles)

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = self.def_shoot_cooldown
            x, y = self.rect.center
            return Projectile(x, y, direction=self.direction, speed=self.shoot_speed, damage=self.shoot_damage)
        else: return None

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
            self.direction = -1
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            self.direction = 1

        # odwracanie grafiki w zależności od kierunku ruchu
        self.image = self.image_left if self.direction == -1 else self.image_right

        if keys[pygame.K_UP] and self.on_ground:
            self.velocity.y = self.jump_strength

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            proj = self.shoot()
            return proj
        return None