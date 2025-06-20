import pygame

from config import TILE_SIZE, PLAYER_IMAGE
from projectile import Projectile
from character import Character
from audio import Sound

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
    def __init__(self, pos, hp=None):
        raw = pygame.image.load(PLAYER_IMAGE).convert_alpha()
        cropped = crop_to_visible_area(raw)
        self.image = scale_to_height(cropped, TILE_SIZE)
        super().__init__(self.image, pos, speed=5, max_hp=100, hp=hp)

        self.direction = 1 # 1 prawo, -1 lewo
        self.shoot_cooldown = 0
        self.def_shoot_cooldown = 5
        self.shoot_speed = 12
        self.shoot_damage = 10

        self.invincible_time = 0
        self.def_invincible_time = 100

        # audio
        self.old_y = self.rect.y
        self.sfx = Sound()

    def update(self, keys, tiles):
        #zmiana pozycji y
        old_y = self.rect.y

        was_on_ground = self.on_ground

        #obsługa klawiszy
        self.handle_input()

        #cooldown ataku
        if self.shoot_cooldown > 0: self.shoot_cooldown -= 1

        #fizyka
        self.apply_gravity()
        self.move_collide(tiles)

        new_y = self.rect.y

        if (was_on_ground and not self.on_ground) and new_y != self.old_y:
            self.sfx.play("jump")

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.sfx.play("shoot")
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
            self.set_facing(-1)
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            self.direction = 1
            self.set_facing(1)
        if keys[pygame.K_UP] and self.on_ground:
            # self.sfx.play("jump")
            self.velocity.y = self.jump_strength
            # if self != self.rect.y:
            #     print("OLD_Y: ", self.old_y)
            #     print("Y: ", self.rect.y)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            proj = self.shoot()
            return proj
        return None

    def take_damage(self, damage):
        now = pygame.time.get_ticks()
        # jeśli nadal w czasie nietykalności, nic nie rób
        if now < self.invincible_time:
            return
        # ustaw nowe okno nietykalności
        self.invincible_time = now + self.def_invincible_time
        # wywołaj bazową logikę (hp-=, show_hp, kill() jeśli hp≤0)
        super().take_damage(damage)