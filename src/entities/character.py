import pygame

from src.config import COLORS


class Character(pygame.sprite.Sprite):
    def __init__(self, image, pos, speed = 3, max_hp = 50, hp = None):
        super().__init__()
        # odbicie grafiki
        self.image_right = image
        self.image_left = pygame.transform.flip(image, True, False)
        self.image = self.image_right

        # pozycja
        self.rect = self.image.get_rect(topleft = pos)

        # atrybuty
        self.speed = speed
        self.velocity = pygame.math.Vector2(0, 0)
        self.gravity = 0.7
        self.jump_strength = -16
        self.on_ground = False

        self.max_hp = max_hp
        # przy przejściu do kolejnego poziomu, ilość hp zostaje taka sama, po uruchomieniu = max_hp
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
        # sprawdzenie pozycji sprite na ekranie
        screen_rect = camera.apply(self.rect)
        # rysowanie sprite'a
        surface.blit(self.image, screen_rect)

        # rysowanie paska życia tylko po otrzymaniu obrażeń
        now = pygame.time.get_ticks()
        if now < self.show_hp_time:
            # szerokość sprite'a = szerokość paska
            bar_w = screen_rect.width
            bar_h = 4
            # pasek nad sprite’em
            bar_x = screen_rect.x
            bar_y = screen_rect.y - bar_h - 2

            # wypełnienie: proporcja hp
            ratio = max(0.0, min(1.0, self.hp / self.max_hp))
            fill_w = int(bar_w * ratio)
            fill_w = max(0, min(bar_w, fill_w))

            inner_rect = pygame.Rect(bar_x, bar_y, fill_w, bar_h)
            outer_rect = pygame.Rect(bar_x, bar_y, bar_w, bar_h)

            # rysowanie
            pygame.draw.rect(surface, COLORS["red"], inner_rect)
            pygame.draw.rect(surface, COLORS["white"], outer_rect, 1)

    # obracanie grafiki w zależności od kierunku
    def set_facing(self, direction:int):
        # direction: 1 = prawo, -1 = lewo
        if direction not in (-1, 1):
            return
        self.image = self.image_left if direction < 0 else self.image_right

