import pygame
from roguelike.map import Map, TILE_SIZE

def main():
    pygame.init()
    WIDTH, HEIGHT = 25, 18
    screen = pygame.display.set_mode((TILE_SIZE * WIDTH, TILE_SIZE * HEIGHT))
    pygame.display.set_caption("Hackerman: Roguelike")
    clock = pygame.time.Clock()

    # Wczytaj grafiki kafelków
    tile_images = {
        '#': pygame.image.load("assets/img/tile_wall.png").convert(),
        '.': pygame.image.load("assets/img/tile_floor.png").convert(),
    }

    game_map = Map(WIDTH, HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        game_map.draw(screen, tile_images)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
