import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 500, 700
FPS           = 60
screen        = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock         = pygame.time.Clock()

font       = pygame.font.SysFont("Arial", 24, bold=True)
font_large = pygame.font.SysFont("Arial", 48, bold=True)


def draw_car(surface, x, y, color, direction="down"):
    """Рисует машину с направлением up/down"""
    w, h = 50, 80
    pygame.draw.rect(surface, color, (x, y, w, h), border_radius=10)
    hood = tuple(max(0, c - 40) for c in color)
    if direction == "up":
        pygame.draw.rect(surface, hood, (x+5, y, w-10, 20), border_radius=6)
        pygame.draw.rect(surface, (180,230,255), (x+8, y+22, w-16, 22), border_radius=4)
        pygame.draw.ellipse(surface, (255,255,150), (x+5,      y+3,    12, 8))
        pygame.draw.ellipse(surface, (255,255,150), (x+w-17,   y+3,    12, 8))
        pygame.draw.ellipse(surface, (200,30,30),   (x+5,      y+h-11, 12, 8))
        pygame.draw.ellipse(surface, (200,30,30),   (x+w-17,   y+h-11, 12, 8))
    else:
        pygame.draw.rect(surface, hood, (x+5, y+h-20, w-10, 20), border_radius=6)
        pygame.draw.rect(surface, (180,230,255), (x+8, y+h-44, w-16, 22), border_radius=4)
        pygame.draw.ellipse(surface, (255,255,150), (x+5,      y+h-11, 12, 8))
        pygame.draw.ellipse(surface, (255,255,150), (x+w-17,   y+h-11, 12, 8))
        pygame.draw.ellipse(surface, (200,30,30),   (x+5,      y+3,    12, 8))
        pygame.draw.ellipse(surface, (200,30,30),   (x+w-17,   y+3,    12, 8))
    for wx, wy in [(x-10,y+12),(x+w,y+12),(x-10,y+h-32),(x+w,y+h-32)]:
        pygame.draw.rect(surface, (25,25,25),    (wx, wy, 10, 20), border_radius=4)
        pygame.draw.rect(surface, (180,180,180), (wx+2, wy+4, 6, 12), border_radius=2)
    stripe = tuple(min(255, c+60) for c in color)
    pygame.draw.rect(surface, stripe, (x+w//2-3, y+10, 6, h-20))


class PlayerCar:
    def __init__(self):
        self.w, self.h = 50, 80
        self.x     = WIDTH//2 - 25
        self.y     = HEIGHT - 120
        self.speed = 5
        self.color = (30, 144, 255)

    def draw(self, surface):
        draw_car(surface, self.x, self.y, self.color, "up")

    def move(self, keys):
        if keys[pygame.K_LEFT]  and self.x > 52:            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH-52-self.w: self.x += self.speed

    def get_rect(self):
        return pygame.Rect(self.x+5, self.y+5, self.w-10, self.h-10)


class EnemyCar:
    """Машина врага — едет вниз"""
    COLORS = [(220,50,50),(50,180,80),(200,150,30),(160,50,200),(200,100,50)]

    def __init__(self, speed):
        self.w, self.h = 50, 80
        self.x     = random.randint(55, WIDTH-105)
        self.y     = -self.h
        self.speed = speed
        self.color = random.choice(self.COLORS)

    def draw(self, surface):
        draw_car(surface, self.x, self.y, self.color, "down")

    def update(self): self.y += self.speed

    def get_rect(self):
        return pygame.Rect(self.x+5, self.y+5, self.w-10, self.h-10)


# Типы монет: (цвет, вес_очков, вероятность, радиус, метка)
COIN_TYPES = [
    {"label": "$",  "color": (255,215,0),   "points": 1,  "prob": 0.60, "r": 14},  # обычная
    {"label": "$$", "color": (192,192,192), "points": 3,  "prob": 0.30, "r": 16},  # серебро
    {"label": "$$$","color": (255,100,100), "points": 7,  "prob": 0.10, "r": 18},  # редкая
]

def pick_coin_type():
    """Выбирает тип монеты по вероятности"""
    r = random.random()
    cumulative = 0
    for ct in COIN_TYPES:
        cumulative += ct["prob"]
        if r <= cumulative:
            return ct
    return COIN_TYPES[0]


class Coin:
    """Монета с разным весом (очками)"""
    def __init__(self, speed):
        ct         = pick_coin_type()
        self.r     = ct["r"]
        self.color = ct["color"]
        self.points= ct["points"]
        self.label = ct["label"]
        self.x     = random.randint(60, WIDTH-60)
        self.y     = -self.r
        self.speed = speed

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.r)
        pygame.draw.circle(surface, tuple(max(0,c-60) for c in self.color),
                           (self.x, self.y), self.r, 3)
        f    = pygame.font.SysFont("Arial", 11, bold=True)
        txt  = f.render(self.label, True, (80,50,0))
        surface.blit(txt, (self.x - txt.get_width()//2,
                           self.y - txt.get_height()//2))

    def update(self): self.y += self.speed

    def get_rect(self):
        return pygame.Rect(self.x-self.r, self.y-self.r, self.r*2, self.r*2)


class Road:
    def __init__(self):
        self.line_y = 0
        self.speed  = 5

    def draw(self, surface):
        surface.fill((70,70,70))
        pygame.draw.rect(surface, (34,120,34), (0, 0, 52, HEIGHT))
        pygame.draw.rect(surface, (34,120,34), (WIDTH-52, 0, 52, HEIGHT))
        pygame.draw.rect(surface, (220,220,220), (50, 0, 4, HEIGHT))
        pygame.draw.rect(surface, (220,220,220), (WIDTH-54, 0, 4, HEIGHT))
        for i in range(-1, HEIGHT//80+2):
            y = (self.line_y + i*80) % (HEIGHT+80) - 80
            pygame.draw.rect(surface, (255,255,255), (WIDTH//2-4, y, 8, 50))

    def update(self):
        self.line_y = (self.line_y + self.speed) % 80


def game_over_screen(score, coins):
    screen.fill((15,15,15))
    t1 = font_large.render("GAME OVER", True, (220,50,50))
    t2 = font.render(f"Score: {score}", True, (220,220,220))
    t3 = font.render(f"Coins: {coins}", True, (255,215,0))
    t4 = font.render("R — restart    Q — quit", True, (120,120,120))
    screen.blit(t1, (WIDTH//2-t1.get_width()//2, 200))
    screen.blit(t2, (WIDTH//2-t2.get_width()//2, 300))
    screen.blit(t3, (WIDTH//2-t3.get_width()//2, 340))
    screen.blit(t4, (WIDTH//2-t4.get_width()//2, 420))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: return True
                if event.key == pygame.K_q: pygame.quit(); sys.exit()


def main():
    while True:
        player       = PlayerCar()
        road         = Road()
        enemies      = []
        coins        = []
        score        = 0
        coin_count   = 0   # очки от монет
        enemy_timer  = 0
        coin_timer   = 0
        # Порог монет для ускорения врагов
        SPEED_THRESHOLD = 5
        enemy_bonus     = 0  # дополнительная скорость врагов

        running = True
        while running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()

            keys = pygame.key.get_pressed()
            player.move(keys)

            score      += 1
            game_speed  = 5 + score // 300

            # Увеличиваем скорость врагов каждые SPEED_THRESHOLD монет
            enemy_bonus = (coin_count // SPEED_THRESHOLD)

            # Спавн врагов
            enemy_timer += 1
            if enemy_timer > max(40, 80 - score//100):
                enemies.append(EnemyCar(game_speed + 1 + enemy_bonus))
                enemy_timer = 0

            # Спавн монет
            coin_timer += 1
            if coin_timer > 100:
                if random.random() < 0.65:
                    coins.append(Coin(game_speed))
                coin_timer = 0

            road.speed = game_speed
            road.update()

            for enemy in enemies[:]:
                enemy.speed = game_speed + 1 + enemy_bonus
                enemy.update()
                if enemy.y > HEIGHT:
                    enemies.remove(enemy)
                elif player.get_rect().colliderect(enemy.get_rect()):
                    running = False

            for coin in coins[:]:
                coin.speed = game_speed
                coin.update()
                if coin.y > HEIGHT:
                    coins.remove(coin)
                elif player.get_rect().colliderect(coin.get_rect()):
                    coin_count += coin.points  # добавляем очки монеты
                    coins.remove(coin)

            # Отрисовка
            road.draw(screen)
            for e in enemies: e.draw(screen)
            for c in coins:   c.draw(screen)
            player.draw(screen)

            # HUD
            screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10, 10))
            screen.blit(font.render(f"Coins: {coin_count}", True, (255,215,0)),
                        (WIDTH - font.size(f"Coins: {coin_count}")[0] - 10, 10))
            screen.blit(font.render(f"Spd+{enemy_bonus}", True, (255,100,100)),
                        (WIDTH//2 - 30, 10))

            pygame.display.flip()

        if not game_over_screen(score, coin_count):
            break


if __name__ == "__main__":
    main()