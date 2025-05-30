import pygame
import numpy as np

WINDOW_WIDTH = 800

def crop_to_visible_area(image, tolerance=10):
    arr = pygame.surfarray.array_alpha(image)
    y_indices, x_indices = np.where(arr > tolerance)
    if len(x_indices) == 0 or len(y_indices) == 0:
        return image
    min_x, max_x = np.min(x_indices), np.max(x_indices)
    min_y, max_y = np.min(y_indices), np.max(y_indices)
    rect = pygame.Rect(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)
    return image.subsurface(rect).copy()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, ground_rect, image_path="assets/img/bugzilla.png", speed=2, target_height=64):
        super().__init__()
        try:
            raw = pygame.image.load(image_path).convert_alpha()
        except Exception as e:
            print(f"Error loading {image_path}: {e}")
            raw = pygame.Surface((64, 64), pygame.SRCALPHA)
            raw.fill((255, 0, 0, 128))

        cropped = crop_to_visible_area(raw)
        scale = target_height / cropped.get_height()
        w = int(cropped.get_width() * scale)
        scaled = pygame.transform.scale(cropped, (w, target_height))
        self.image = scaled
        self.rect = self.image.get_rect()

        # KLUCZ: STOPA Bugzilli dokładnie na GÓRZE ziemi!
        self.rect.midbottom = (x, ground_rect.top)

        self.direction = 1
        self.speed = speed

    def update(self, ground_rects):
        self.rect.x += self.direction * self.speed
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = 1
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
            self.direction = -1
        # Zawsze trzymaj na górze ziemi!
        if ground_rects:
            ground_rect = ground_rects[0]
            self.rect.bottom = ground_rect.top
