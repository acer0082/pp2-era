import pygame
import sys
from player import MusicPlayer

WIDTH, HEIGHT = 500, 350

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Music Player")
    clock  = pygame.time.Clock()
    player = MusicPlayer()

    font_title  = pygame.font.SysFont("Arial", 32, bold=True)
    font_medium = pygame.font.SysFont("Arial", 22)
    font_small  = pygame.font.SysFont("Arial", 18)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  player.play()
                if event.key == pygame.K_s:  player.stop()
                if event.key == pygame.K_n:  player.next_track()
                if event.key == pygame.K_b:  player.prev_track()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        # Фон
        screen.fill((20, 20, 40))

        # Заголовок
        title = font_title.render("🎵 Music Player", True, (255, 220, 50))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 40))

        # Трек
        track = font_medium.render(f"♪  {player.get_track_name()}", True, (200, 200, 255))
        screen.blit(track, (WIDTH//2 - track.get_width()//2, 120))

        # Номер трека
        num = font_small.render(f"Трек: {player.get_track_number()}", True, (150, 150, 150))
        screen.blit(num, (WIDTH//2 - num.get_width()//2, 165))

        # Статус
        color  = (80, 255, 80) if player.playing else (255, 80, 80)
        status = font_medium.render(player.get_status(), True, color)
        screen.blit(status, (WIDTH//2 - status.get_width()//2, 210))

        # Разделитель
        pygame.draw.line(screen, (80, 80, 120), (40, 260), (460, 260), 1)

        # Управление
        controls = [
            "P — Play      S — Stop",
            "N — Next      B — Previous",
            "Q — Quit"
        ]
        for i, line in enumerate(controls):
            text = font_small.render(line, True, (120, 120, 160))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 275 + i * 22))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()