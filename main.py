import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from game import Game
from menu import MainMenu

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Hackerman vs. Bugzilla")
    clock = pygame.time.Clock()

    # Menu startowe (pobieramy nazwę gracza i ustawienia)
    #menu = MainMenu(screen)
    #menu.run()
    #player_name = menu.player_name or "test"
    #music_on = menu.music_on
    #sound_on = menu.sound_on

    player_name = "test"
    music_on, sound_on = False, False

    # Start gry
    game = Game(screen, player_name=player_name, music_on=music_on, sound_on=sound_on)
    while game.running:
        game.handle_events()
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
