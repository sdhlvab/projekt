import pygame

class Bugzilla(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (32, 32))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2

    def update(self, target_rect):
        if self.rect.x < target_rect.x:
            self.rect.x += self.speed
        elif self.rect.x > target_rect.x:
            self.rect.x -= self.speed
        if self.rect.y < target_rect.y:
            self.rect.y += self.speed
        elif self.rect.y > target_rect.y:
            self.rect.y -= self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)
