import pygame
import math
import datetime

class MickeysClock:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width  = width
        self.height = height
        self.cx     = width  // 2
        self.cy     = height // 2

    def draw_hand(self, angle_deg, length, width, color):
        """Рисует стрелку как линию с кружком на конце"""
        angle_rad = math.radians(angle_deg - 90)
        end_x = self.cx + int(length * math.cos(angle_rad))
        end_y = self.cy + int(length * math.sin(angle_rad))
        pygame.draw.line(self.screen, color,
                         (self.cx, self.cy), (end_x, end_y), width)
        pygame.draw.circle(self.screen, color, (end_x, end_y), width + 4)

    def draw_clock_face(self):
        """Рисует циферблат"""
        self.screen.fill((255, 255, 220))

        # Внешний круг
        pygame.draw.circle(self.screen, (180, 140, 80),
                           (self.cx, self.cy), 200, 6)

        # Деления
        for i in range(60):
            angle = math.radians(i * 6 - 90)
            if i % 5 == 0:
                r1, r2, w = 175, 195, 3
            else:
                r1, r2, w = 185, 195, 1
            x1 = self.cx + int(r1 * math.cos(angle))
            y1 = self.cy + int(r1 * math.sin(angle))
            x2 = self.cx + int(r2 * math.cos(angle))
            y2 = self.cy + int(r2 * math.sin(angle))
            pygame.draw.line(self.screen, (80, 60, 30), (x1, y1), (x2, y2), w)

        # Цифры
        font = pygame.font.SysFont("Arial", 30, bold=True)
        for i in range(1, 13):
            angle = math.radians(i * 30 - 90)
            x = self.cx + int(150 * math.cos(angle))
            y = self.cy + int(150 * math.sin(angle))
            text = font.render(str(i), True, (50, 30, 10))
            rect = text.get_rect(center=(x, y))
            self.screen.blit(text, rect)

        # Голова Микки (3 круга)
        pygame.draw.circle(self.screen, (20, 20, 20),
                           (self.cx, self.cy - 60), 45)           # голова
        pygame.draw.circle(self.screen, (20, 20, 20),
                           (self.cx - 38, self.cy - 95), 28)      # левое ухо
        pygame.draw.circle(self.screen, (20, 20, 20),
                           (self.cx + 38, self.cy - 95), 28)      # правое ухо
        # Лицо
        pygame.draw.circle(self.screen, (255, 220, 180),
                           (self.cx, self.cy - 58), 35)
        # Глаза
        pygame.draw.circle(self.screen, (20, 20, 20),
                           (self.cx - 12, self.cy - 68), 5)
        pygame.draw.circle(self.screen, (20, 20, 20),
                           (self.cx + 12, self.cy - 68), 5)
        # Нос
        pygame.draw.circle(self.screen, (20, 20, 20),
                           (self.cx, self.cy - 55), 4)

        # Центральная точка
        pygame.draw.circle(self.screen, (30, 30, 30),
                           (self.cx, self.cy), 8)

    def draw(self):
        now     = datetime.datetime.now()
        minutes = now.minute
        seconds = now.second

        min_angle = minutes * 6        # минутная стрелка
        sec_angle = seconds * 6        # секундная стрелка

        self.draw_clock_face()
        # Минутная стрелка (правая рука — длиннее, синяя)
        self.draw_hand(min_angle, length=120, width=6, color=(30, 80, 180))
        # Секундная стрелка (левая рука — короче, красная)
        self.draw_hand(sec_angle, length=100, width=4, color=(200, 40, 40))

        # Время текстом
        font = pygame.font.SysFont("Arial", 24)
        time_str = now.strftime("%H:%M:%S")
        text = font.render(time_str, True, (60, 60, 60))
        self.screen.blit(text, (self.cx - text.get_width()//2, self.cy + 130))