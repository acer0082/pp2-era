import pygame
import sys
from ball import Ball

WIDTH, HEIGHT = 600, 600
FPS = 60

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball")
    clock = pygame.time.Clock()
    ball  = Ball(WIDTH // 2, HEIGHT // 2)

    font = pygame.font.SysFont("Arial", 18)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball.move(0, -ball.speed, WIDTH, HEIGHT)
                if event.key == pygame.K_DOWN:
                    ball.move(0,  ball.speed, WIDTH, HEIGHT)
                if event.key == pygame.K_LEFT:
                    ball.move(-ball.speed, 0, WIDTH, HEIGHT)
                if event.key == pygame.K_RIGHT:
                    ball.move( ball.speed, 0, WIDTH, HEIGHT)

        screen.fill((255, 255, 255))
        ball.draw(screen)

        hint = font.render("Стрелки = движение", True, (150, 150, 150))
        screen.blit(hint, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()