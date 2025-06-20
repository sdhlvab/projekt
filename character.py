import pygame
from select import select


class Character(pygame.sprite.Sprite):
    def __init__(self, image, pos, speed=3, max_hp=50, hp=50):
        super().__init__()
        # Odbicie grafiki
        self.image_right = image
        self.image_left = pygame.transform.flip(image, True, False)
        self.image = self.image_right

        # Pozycja
        self.rect = self.image.get_rect(topleft=pos)

        # Atrybuty
        self.speed = speed
        self.velocity = pygame.math.Vector2(0, 0)
        self.gravity = 0.7
        self.jump_strength = -16
        self.on_ground = False

        self.max_hp = max_hp
        self.hp = hp if hp is not None else self.max_hp
        self.show_hp_time = 0
        self.def_show_hp_time = 1000


    # ograniczenie prędkości spadania
    def apply_gravity(self):
        self.velocity.y = min(self.velocity.y + self.gravity, 12)

    # wykrywanie kolizji
    def move_collide(self, tiles, on_horizontal_collision=None):
        # poziom
        self.rect.x += self.velocity.x
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.velocity.x > 0:
                    self.rect.right = tile.left
                if self.velocity.x < 0:
                    self.rect.left = tile.right
                if on_horizontal_collision:
                    on_horizontal_collision()

        # pion
        self.rect.y += self.velocity.y
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.velocity.y > 0:
                    self.rect.bottom = tile.top
                    self.velocity.y = 0
                    self.on_ground = True
                elif self.velocity.y < 0:
                    self.rect.top = tile.bottom
                    self.velocity.y = 0

    # otrzymywanie obrażeń
    def take_damage(self, damage):
        self.hp = max(self.hp - damage, 0)
        self.show_hp_time = pygame.time.get_ticks() + self.def_show_hp_time
        if self.hp == 0:
            self.kill()

    # rysowanie
    def draw(self, surface, camera):
        # sprite
        screen_rect = camera.apply(self.rect)
        surface.blit(self.image, screen_rect)
        # pasek życia
        now = pygame.time.get_ticks()
        if now < self.show_hp_time:
            w = self.rect.width
            h = 4
            x = self.rect.x
            y = self.rect.y - h - 2
            ratio = self.hp / self.max_hp
            inner_w = int(w * ratio)
            inner_rect = pygame.Rect(x, y, inner_w, h)
            outer_rect = pygame.Rect(x, y, w, h)
            pygame.draw.rect(surface, (255, 0, 0), inner_rect)
            pygame.draw.rect(surface, (255, 255, 255), outer_rect, 1)

    # obracanie grafiki w zależności od kierunku
    def set_facing(self, direction:int):
        # direction: 1 = prawo, -1 = lewo
        if direction not in (-1, 1):
            return
        self.image = self.image_left if direction < 0 else self.image_right

