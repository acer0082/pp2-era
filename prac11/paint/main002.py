import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock  = pygame.time.Clock()
font   = pygame.font.SysFont("Arial", 16, bold=True)

PALETTE = [
    (0,0,0),(255,255,255),(220,50,50),(50,200,80),
    (50,100,220),(255,215,0),(200,100,200),(255,140,0),
    (0,200,200),(139,69,19),
]

# Все инструменты включая новые фигуры
TOOLS = ["Pencil","Eraser","Rect","Square","Circle",
         "RTriangle","EqTriangle","Rhombus"]

current_color = (0, 0, 0)
current_tool  = "Pencil"
brush_size    = 5
drawing       = False
start_pos     = None
canvas        = pygame.Surface((WIDTH, HEIGHT-80))
canvas.fill((255,255,255))


def draw_toolbar(surface):
    """Рисует панель инструментов"""
    pygame.draw.rect(surface, (40,40,40), (0,0,WIDTH,80))

    # Палитра
    for i, color in enumerate(PALETTE):
        x = 10 + i*36
        pygame.draw.rect(surface, color, (x,10,30,30), border_radius=4)
        if color == current_color:
            pygame.draw.rect(surface, (255,255,255), (x,10,30,30), 2, border_radius=4)

    # Текущий цвет
    pygame.draw.rect(surface, current_color, (378,10,36,30), border_radius=4)
    pygame.draw.rect(surface, (180,180,180), (378,10,36,30), 2, border_radius=4)

    # Инструменты (2 ряда по 4)
    for i, tool in enumerate(TOOLS):
        col = i % 4
        row = i // 4
        x   = 10 + col * 100
        y   = 44 + row * 18
        active = (tool == current_tool)
        color  = (80,130,200) if active else (65,65,65)
        pygame.draw.rect(surface, color, (x, y, 92, 15), border_radius=3)
        txt = pygame.font.SysFont("Arial", 11, bold=True).render(tool, True, (255,255,255))
        surface.blit(txt, (x+46-txt.get_width()//2, y+2))

    # Размер
    surface.blit(font.render(f"Sz:{brush_size}", True, (200,200,200)), (430,46))
    pygame.draw.rect(surface, (70,70,70), (480,44,22,14), border_radius=3)
    pygame.draw.rect(surface, (70,70,70), (505,44,22,14), border_radius=3)
    surface.blit(pygame.font.SysFont("Arial",12,bold=True).render("+",True,(255,255,255)), (487,44))
    surface.blit(pygame.font.SysFont("Arial",12,bold=True).render("-",True,(255,255,255)), (512,44))

    # Clear
    pygame.draw.rect(surface, (160,40,40), (535,44,55,30), border_radius=4)
    surface.blit(font.render("Clear", True, (255,255,255)), (542,52))


def handle_toolbar_click(pos):
    """Обработка кликов по тулбару"""
    global current_color, current_tool, brush_size, canvas
    x, y = pos

    # Палитра
    if 10 <= y <= 40:
        for i, color in enumerate(PALETTE):
            cx = 10 + i*36
            if cx <= x <= cx+30:
                current_color = color

    # Инструменты
    for i, tool in enumerate(TOOLS):
        col = i % 4
        row = i // 4
        tx  = 10 + col*100
        ty  = 44 + row*18
        if tx <= x <= tx+92 and ty <= y <= ty+15:
            current_tool = tool

    # Размер
    if 480 <= x <= 502 and 44 <= y <= 58: brush_size = min(50, brush_size+2)
    if 505 <= x <= 527 and 44 <= y <= 58: brush_size = max(1,  brush_size-2)

    # Clear
    if 535 <= x <= 590 and 44 <= y <= 74:
        canvas.fill((255,255,255))


def draw_shape_on(surface, tool, p1, p2, color, size):
    """
    Рисует фигуру на поверхности.
    p1 = начало, p2 = конец (мышь)
    """
    x1,y1 = p1
    x2,y2 = p2
    w = x2 - x1
    h = y2 - y1

    if tool == "Rect":
        # Произвольный прямоугольник
        pygame.draw.rect(surface, color, (x1,y1,w,h), size)

    elif tool == "Square":
        # Квадрат — сторона = min(|w|,|h|) с сохранением знака
        side = min(abs(w), abs(h))
        sx   = x1 + (side if w >= 0 else -side)
        sy   = y1 + (side if h >= 0 else -side)
        pygame.draw.rect(surface, color,
                         (min(x1,sx), min(y1,sy), side, side), size)

    elif tool == "Circle":
        cx = (x1+x2)//2
        cy = (y1+y2)//2
        r  = max(abs(w), abs(h))//2
        pygame.draw.circle(surface, color, (cx,cy), r, size)

    elif tool == "RTriangle":
        # Прямоугольный треугольник: прямой угол в p1
        pts = [(x1,y1), (x2,y1), (x1,y2)]
        pygame.draw.polygon(surface, color, pts, size)

    elif tool == "EqTriangle":
        # Равносторонний треугольник, основание = ширина
        mid_x = (x1+x2)//2
        h_tri = int(abs(w) * math.sqrt(3)/2)
        top_y = y1 - h_tri if h >= 0 else y1 + h_tri
        pts = [(x1,y1), (x2,y1), (mid_x, top_y)]
        pygame.draw.polygon(surface, color, pts, size)

    elif tool == "Rhombus":
        # Ромб: 4 точки по диагоналям
        cx = (x1+x2)//2
        cy = (y1+y2)//2
        pts = [(cx,y1),(x2,cy),(cx,y2),(x1,cy)]
        pygame.draw.polygon(surface, color, pts, size)


def main():
    global drawing, start_pos, canvas, current_color, current_tool, brush_size

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < 80:
                    handle_toolbar_click((x,y))
                else:
                    drawing   = True
                    start_pos = (x, y-80)

            if event.type == pygame.MOUSEBUTTONUP and drawing:
                x, y    = event.pos
                end_pos = (x, y-80)
                if current_tool == "Pencil" or current_tool == "Eraser":
                    pass  # уже нарисовано в MOUSEMOTION
                else:
                    draw_shape_on(canvas, current_tool,
                                  start_pos, end_pos,
                                  current_color, brush_size)
                drawing = False

            if event.type == pygame.MOUSEMOTION and drawing:
                x, y = event.pos
                if y >= 80:
                    cur = (x, y-80)
                    if current_tool == "Pencil":
                        pygame.draw.circle(canvas, current_color, cur, brush_size)
                    elif current_tool == "Eraser":
                        pygame.draw.circle(canvas, (255,255,255), cur, brush_size*3)

        # Отрисовка
        screen.fill((255,255,255))
        draw_toolbar(screen)
        screen.blit(canvas, (0,80))

        # Предпросмотр фигуры
        if drawing and start_pos and current_tool not in ("Pencil","Eraser"):
            mx, my  = pygame.mouse.get_pos()
            preview = canvas.copy()
            draw_shape_on(preview, current_tool,
                          start_pos, (mx, my-80),
                          current_color, brush_size)
            screen.blit(preview, (0,80))

        pygame.display.flip()


if __name__ == "__main__":
    main()