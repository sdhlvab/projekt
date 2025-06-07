import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Hackerman vs Bugzilla")

    clock = pygame.time.Clock()
    game = Game(screen)

    running = True
    while running:
        game.handle_events()
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
