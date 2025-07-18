import pygame

from src.config import TILE_SIZE, PLAYER, INVINCIBLE_TIME, SHOOT_CD, SHOOT_DMG, SHOOT_SPEED, MAX_HP, SPEED
from src.entities.projectile import Projectile
from src.entities.character import Character

def crop_to_visible_area(image, image_path):
    mask = pygame.mask.from_surface(image, image_path["tolerance"])
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
    def __init__(self, pos, hp=None, image_path=None, sfx=None):
        if isinstance(image_path, dict):
            image_info = image_path
        else:
            image_info = PLAYER[image_path]
        path = image_path or PLAYER
        raw = pygame.image.load(image_info["image"]).convert_alpha()
        cropped = crop_to_visible_area(raw, image_info)
        self.image = scale_to_height(cropped, TILE_SIZE)
        super().__init__(self.image, pos, speed=SPEED, max_hp=MAX_HP, hp=hp)

        self.direction = 1 # 1 prawo, -1 lewo
        self.shoot_cooldown = 0
        self.def_shoot_cooldown = SHOOT_CD
        self.shoot_speed = SHOOT_SPEED
        self.shoot_damage = SHOOT_DMG

        self.invincible_time = 0
        self.def_invincible_time = INVINCIBLE_TIME

        # audio
        self.old_y = self.rect.y
        self.sfx = sfx

    def update(self, keys, tiles):
        # zmiana pozycji y (potrzebne do prawidłowego odtworzenia dźwięku skoku)
        old_y = self.rect.y
        was_on_ground = self.on_ground

        # obsługa klawiszy
        self.handle_input()

        # cooldown ataku
        if self.shoot_cooldown > 0: self.shoot_cooldown -= 1

        # fizyka
        self.apply_gravity()
        self.move_collide(tiles)

        # zmiana pozycji y (potrzebne do prawidłowego odtworzenia dźwięku skoku)
        new_y = self.rect.y
        # dźwięk skoku
        if (was_on_ground and not self.on_ground) and new_y != old_y:
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
            self.velocity.y = self.jump_strength

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
        # wywołaj bazową logikę
        super().take_damage(damage)