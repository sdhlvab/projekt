import pygame

from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from src.game import Game

def main():
    pygame.init()
    pygame.mixer.init()
    # większa ilość kanałów - czasami nie odtwarzało niektórych dźwięków
    pygame.mixer.set_num_channels(32)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    #flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
    #screen = pygame.display.set_mode((0, 0), flags)
    # do fullscreena trzeba dodać nadpisywanie wartości SCREEN_WIDTH, SCREEN_HEIGHT z configa!!
    pygame.display.set_caption("Hackerman vs Bugzilla")
    game = Game(screen)
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()
