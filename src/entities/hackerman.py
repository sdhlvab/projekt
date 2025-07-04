# import pygame
#
# class Hackerman(pygame.sprite.Sprite):
#     def __init__(self, x, y, image):
#         super().__init__()
#         self.image = pygame.transform.scale(image, (48, 48))
#         self.rect = self.image.get_rect(topleft=(x, y))
#         self.speed = 5
#         self.is_attacking = False
#
#     def update(self, keys):
#         if keys[pygame.K_LEFT]:
#             self.rect.x -= self.speed
#         if keys[pygame.K_RIGHT]:
#             self.rect.x += self.speed
#         if keys[pygame.K_UP]:
#             self.rect.y -= self.speed
#         if keys[pygame.K_DOWN]:
#             self.rect.y += self.speed
#         self.is_attacking = keys[pygame.K_SPACE]
#
#     def draw(self, surface):
#         surface.blit(self.image, self.rect)
