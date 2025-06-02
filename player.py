import pygame

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

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
        # Wczytaj oryginał i wersję odbitą
        raw = pygame.image.load("assets/img/hackerman_brown.png").convert_alpha()
        cropped = crop_to_visible_area(raw)
        scaled = scale_to_height(cropped, 64)
        self.image_right = scaled
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right
        self.facing_right = True

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (pos[0], 550)
        self.speed = 5
        self.velocity = pygame.math.Vector2(0, 0)
        self.jump_strength = -10
        self.gravity = 0.5
        self.on_ground = True
        self.attack_cooldown = 0

    def handle_input(self, keys):
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
            self.image = self.image_left
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            self.image = self.image_right
            self.facing_right = True
        if keys[pygame.K_UP] and self.on_ground:
            self.velocity.y = self.jump_strength
        if keys[pygame.K_SPACE] and self.attack_cooldown <= 0:
            self.attack_cooldown = 20

    def apply_gravity(self):
        self.velocity.y += self.gravity
        if self.velocity.y > 10:
            self.velocity.y = 10

    def update(self, tiles):
        self.handle_input(pygame.key.get_pressed())
        self.apply_gravity()
        self.rect.x += self.velocity.x
        self.collide(tiles, 'x')
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        self.rect.y += self.velocity.y
        self.collide(tiles, 'y')
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.velocity.y = 0

        self.on_ground = False
        rect_below = self.rect.move(0, 1)
        for tile in tiles:
            if rect_below.colliderect(tile):
                self.on_ground = True
                break

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def collide(self, tiles, direction):
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
        if direction == 'y' and not any(self.rect.colliderect(tile) for tile in tiles):
            self.on_ground = False
