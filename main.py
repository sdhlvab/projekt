import pygame
import sys
from roguelike.map import Map, load_map_from_txt, TILE_SIZE

WIDTH, HEIGHT = 800, 600

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hackerman: Roguelike")
    clock = pygame.time.Clock()

    # Wczytaj kafelki
    floor_img = pygame.image.load("assets/img/tile_floor.png").convert_alpha()
    wall_img = pygame.image.load("assets/img/tile_wall.png").convert_alpha()

    # Wczytaj mapę z pliku
    map_data = load_map_from_txt("roguelike/maps/test_map.txt")
    game_map = Map(map_data)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        game_map.draw(screen, floor_img, wall_img)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
