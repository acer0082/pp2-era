import pygame

class Ball:
    def __init__(self, x, y, radius=25):
        self.x      = x
        self.y      = y
        self.radius = radius
        self.speed  = 20
        self.color  = (220, 50, 50)

    def move(self, dx, dy, screen_w, screen_h):
        new_x = self.x + dx
        new_y = self.y + dy
        # Проверка границ
        if self.radius <= new_x <= screen_w - self.radius:
            self.x = new_x
        if self.radius <= new_y <= screen_h - self.radius:
            self.y = new_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        # Блик
        pygame.draw.circle(screen, (255, 120, 120),
                           (self.x - 8, self.y - 8), 8)