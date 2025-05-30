import pygame
from menu import MainMenu
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Hackerman vs. Bugzilla")
    clock = pygame.time.Clock()
    menu = MainMenu(screen)
    menu.run()

    # Odbieramy nicka oraz opcje muzyki/dźwięków
    player_name = menu.player_name or "hackerman"
    music_on = menu.music_on
    sound_on = menu.sound_on

    game = Game(screen, player_name=player_name, music_on=music_on, sound_on=sound_on)
    while game.running:
        game.handle_events()
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
