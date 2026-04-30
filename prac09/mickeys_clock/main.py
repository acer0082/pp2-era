import pygame
import sys
from clock import MickeysClock

WIDTH, HEIGHT = 500, 500
FPS = 1  # обновление раз в секунду

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey's Clock")
    clock  = pygame.time.Clock()
    mickey = MickeysClock(screen, WIDTH, HEIGHT)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        mickey.draw()
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()