import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Hackerman vs Bugzilla")
    game = Game(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game.update()
        game.draw()
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
    pygame.quit()
if __name__ == "__main__":
    main()
