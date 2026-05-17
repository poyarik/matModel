import pygame
import json
import sys

# Настройки окна
WIDTH, HEIGHT = 1024, 768
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🌌 N-Body Universe Editor — М-ня! 🐾")
clock = pygame.time.Clock()

# Цвета
BLACK = (10, 10, 15)
WHITE = (240, 240, 245)
GREEN = (50, 205, 50)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
YELLOW = (255, 215, 0)

# Реальные масштабы для космоса (перевод пикселей в метры)
# Центр экрана (512, 384) будет нашим нулем (Солнцем)
SCALE = 5e8  # 1 пиксель = 500 000 километров
VEL_SCALE = 100 # Масштаб стрелочки скорости (1 пиксель длины = 100 м/с)

bodies = []
current_color = "deepskyblue"
current_mass = 5.972e24 # По умолчанию масса Земли
current_name = "Planet"

# Состояние мышки
creating_body = None
mouse_pos = (0, 0)

def to_simulation_coords(px, py):
    # Перевод пикселей экрана в метры физического движка относительно центра
    x = (px - WIDTH // 2) * SCALE
    y = (py - HEIGHT // 2) * SCALE
    return x, y

def save_to_json():
    config = {
        "settings": {"G": 6.6743e-11, "dt": 3600, "steps": 20000},
        "bodies": bodies
    }
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
    print("🛸 Конфиг успешно сохранен в config.json! Муррр!")
running = True
while running:
    screen.fill(BLACK)
    mouse_pos = pygame.mouse.get_pos()
    
    # Меняем заголовок окна динамически, чтобы выводить инфу без использования шрифтов!
    status_text = f"Selected: {current_name} ({current_mass:.1e} kg) | '1'-Sun '2'-Earth '3'-Moon | Press 'S' to SAVE"
    pygame.display.set_caption(f"🌌 N-Body Editor — {status_text} 🐾")
    
    # Рисуем сетку (космические координаты)
    pygame.draw.line(screen, (30, 30, 40), (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    pygame.draw.line(screen, (30, 30, 40), (0, HEIGHT//2), (WIDTH, HEIGHT//2))

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Левый клик: ставим планету
                cx, cy = to_simulation_coords(mouse_pos[0], mouse_pos[1])
                creating_body = {
                    "name": f"{current_name}_{len(bodies)+1}",
                    "m": current_mass,
                    "x": cx, "y": cy,
                    "vx": 0.0, "vy": 0.0,
                    "color": current_color, "size": 10
                }
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and creating_body:
                start_x = (creating_body["x"] / SCALE) + WIDTH // 2
                start_y = (creating_body["y"] / SCALE) + HEIGHT // 2
                
                creating_body["vx"] = (mouse_pos[0] - start_x) * VEL_SCALE
                creating_body["vy"] = (mouse_pos[1] - start_y) * VEL_SCALE
                
                bodies.append(creating_body)
                creating_body = None
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s: # Нажать S для сохранения
                save_to_json()
            elif event.key == pygame.K_1:
                current_color, current_mass, current_name = "yellow", 1.989e30, "Sun"
            elif event.key == pygame.K_2:
                current_color, current_mass, current_name = "deepskyblue", 5.972e24, "Earth"
            elif event.key == pygame.K_3:
                current_color, current_mass, current_name = "white", 7.347e22, "Moon"

    # Отрисовка уже созданных тел
    for b in bodies:
        px = int((b["x"] / SCALE) + WIDTH // 2)
        py = int((b["y"] / SCALE) + HEIGHT // 2)
        
        col = YELLOW if b["color"] == "yellow" else (BLUE if b["color"] == "deepskyblue" else WHITE)
        pygame.draw.circle(screen, col, (px, py), b["size"])
        
        vx_line = int(px + b["vx"] / VEL_SCALE)
        vy_line = int(py + b["vy"] / VEL_SCALE)
        pygame.draw.line(screen, GREEN, (px, py), (vx_line, vy_line), 2)

    # Отрисовка тела, которое ТЯНЕМ прямо сейчас
    if creating_body:
        px = int((creating_body["x"] / SCALE) + WIDTH // 2)
        py = int((creating_body["y"] / SCALE) + HEIGHT // 2)
        pygame.draw.circle(screen, RED, (px, py), 8)
        pygame.draw.line(screen, RED, (px, py), mouse_pos, 2)

    # МУР! Строчки с font.render и screen.blit(img_s...) полностью удаляем!

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
