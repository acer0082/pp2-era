import pygame
import random
import sys
import time

pygame.init()

WIDTH, HEIGHT = 600, 600
CELL          = 20
COLS          = WIDTH  // CELL
ROWS          = HEIGHT // CELL
FPS_BASE      = 8

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock  = pygame.time.Clock()

font       = pygame.font.SysFont("Arial", 22, bold=True)
font_large = pygame.font.SysFont("Arial", 48, bold=True)

BG      = (15, 15, 15)
GRID_C  = (30, 30, 30)
SNAKE_C = (50, 200, 80)
SNAKE_H = (30, 160, 50)
WALL_C  = (100, 100, 120)
TEXT_C  = (220, 220, 220)
GOLD    = (255, 215, 0)

# Типы еды: (цвет, очки, время_жизни_сек, вероятность)
FOOD_TYPES = [
    {"color": (220, 50,  50),  "points": 1,  "lifetime": 8.0,  "prob": 0.60},  # обычная
    {"color": (50,  180, 220), "points": 3,  "lifetime": 5.0,  "prob": 0.28},  # синяя
    {"color": (255, 215, 0),   "points": 7,  "lifetime": 3.0,  "prob": 0.12},  # золотая
]

def pick_food_type():
    """Выбирает тип еды по вероятности"""
    r, cum = random.random(), 0
    for ft in FOOD_TYPES:
        cum += ft["prob"]
        if r <= cum:
            return ft
    return FOOD_TYPES[0]


class Food:
    """Еда с весом и таймером исчезновения"""
    def __init__(self, snake):
        ft             = pick_food_type()
        self.color     = ft["color"]
        self.points    = ft["points"]
        self.lifetime  = ft["lifetime"]
        self.spawn_time= time.time()
        self.pos       = self._random_pos(snake)

    def _random_pos(self, snake):
        while True:
            pos = (random.randint(1, COLS-2), random.randint(1, ROWS-2))
            if pos not in snake:
                return pos

    def is_expired(self):
        """Проверяет истёк ли таймер"""
        return time.time() - self.spawn_time > self.lifetime

    def time_left(self):
        return max(0, self.lifetime - (time.time() - self.spawn_time))

    def draw(self, surface):
        x, y = self.pos
        rect = pygame.Rect(x*CELL+1, y*CELL+1, CELL-2, CELL-2)
        pygame.draw.rect(surface, self.color, rect, border_radius=10)

        # Таймер — уменьшающийся круг
        ratio = self.time_left() / self.lifetime
        r     = int((CELL//2 - 2) * ratio)
        if r > 0:
            pygame.draw.circle(surface, (255,255,255),
                               (x*CELL + CELL//2, y*CELL + CELL//2), r, 2)

        # Очки рядом
        f   = pygame.font.SysFont("Arial", 11, bold=True)
        txt = f.render(f"+{self.points}", True, (255,255,255))
        surface.blit(txt, (x*CELL + CELL, y*CELL))


def draw_grid(surface):
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(surface, GRID_C, (x,0), (x,HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(surface, GRID_C, (0,y), (WIDTH,y))


def draw_cell(surface, pos, color, radius=4):
    rect = pygame.Rect(pos[0]*CELL+1, pos[1]*CELL+1, CELL-2, CELL-2)
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def game_over_screen(score, level):
    screen.fill((10,10,10))
    t1 = font_large.render("GAME OVER", True, (220,50,50))
    t2 = font.render(f"Score: {score}   Level: {level}", True, TEXT_C)
    t3 = font.render("R — restart    Q — quit", True, (120,120,120))
    screen.blit(t1, (WIDTH//2-t1.get_width()//2, 220))
    screen.blit(t2, (WIDTH//2-t2.get_width()//2, 310))
    screen.blit(t3, (WIDTH//2-t3.get_width()//2, 380))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: return True
                if event.key == pygame.K_q: pygame.quit(); sys.exit()


def main():
    while True:
        snake      = [(COLS//2, ROWS//2),
                      (COLS//2-1, ROWS//2),
                      (COLS//2-2, ROWS//2)]
        direction  = (1, 0)
        next_dir   = (1, 0)
        foods      = [Food(snake)]   # список еды
        score      = 0
        level      = 1
        food_eaten = 0
        fps        = FPS_BASE

        running = True
        while running:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP    and direction != (0, 1):  next_dir = (0,-1)
                    if event.key == pygame.K_DOWN  and direction != (0,-1):  next_dir = (0, 1)
                    if event.key == pygame.K_LEFT  and direction != (1, 0):  next_dir = (-1,0)
                    if event.key == pygame.K_RIGHT and direction != (-1,0):  next_dir = (1, 0)

            direction = next_dir
            head      = (snake[0][0]+direction[0], snake[0][1]+direction[1])

            # Столкновение со стеной
            if head[0] <= 0 or head[0] >= COLS-1 or \
               head[1] <= 0 or head[1] >= ROWS-1:
                running = False; continue

            # Столкновение с собой
            if head in snake:
                running = False; continue

            snake.insert(0, head)

            # Проверка еды
            eaten = False
            for food in foods[:]:
                if head == food.pos:
                    score      += food.points * level
                    food_eaten += 1
                    foods.remove(food)
                    foods.append(Food(snake))  # новая еда
                    eaten = True
                    # Уровень каждые 3 еды
                    if food_eaten % 3 == 0:
                        level += 1
                        fps    = FPS_BASE + (level-1)*2

            if not eaten:
                snake.pop()

            # Удаляем просроченную еду, добавляем новую
            for food in foods[:]:
                if food.is_expired():
                    foods.remove(food)
                    foods.append(Food(snake))

            # Иногда добавляем вторую еду
            if len(foods) < 2 and random.random() < 0.01:
                foods.append(Food(snake))

            # Отрисовка
            screen.fill(BG)
            draw_grid(screen)

            # Стены
            for x in range(COLS):
                draw_cell(screen, (x,0),      WALL_C, 2)
                draw_cell(screen, (x,ROWS-1), WALL_C, 2)
            for y in range(ROWS):
                draw_cell(screen, (0,y),      WALL_C, 2)
                draw_cell(screen, (COLS-1,y), WALL_C, 2)

            # Змейка
            for i, seg in enumerate(snake):
                draw_cell(screen, seg, SNAKE_H if i==0 else SNAKE_C)

            # Еда
            for food in foods:
                food.draw(screen)

            # HUD
            screen.blit(font.render(f"Score: {score}", True, TEXT_C), (10, 5))
            screen.blit(font.render(f"Level: {level}", True, GOLD),
                        (WIDTH - font.size(f"Level: {level}")[0] - 10, 5))

            pygame.display.flip()

        if not game_over_screen(score, level):
            break


if __name__ == "__main__":
    main()