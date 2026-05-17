import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 1. Загружаем координаты (физику)
try:
    history = np.load('orbit_data.npy')
    steps, n_bodies, _ = history.shape
except FileNotFoundError:
    print("Ошибка: Не найден файл orbit_data.npy! Сначала запусти просчет в main.py м-ня 🐾")
    exit()

# 2. Загружаем визуальные настройки из конфига
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    config = {"bodies": []} # пустой дефолт, если конфига нет

# Собираем списки цветов и размеров прямо из сейва
colors = []
sizes = []
for b in config.get('bodies', []):
    colors.append(b.get('color', 'white'))
    sizes.append(b.get('size', 5))

# 3. Настройка графика
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')
ax.set_facecolor('black') 
fig.patch.set_facecolor('black') # Делаем рамку вокруг графика тоже черной

# Ограничиваем оси под масштаб из конфига (1.8e11 метров — это до орбиты Земли)
limit = 1.8e11 
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)

# Убираем серые оси и деления, чтобы был чистый космос
ax.axis('off')

# 4. Безопасное создание объектов для каждой планеты (защита от IndexError)
dots = []
lines = []

for i in range(n_bodies):
    # Если в json планет меньше, чем в просчитанном npy, берем дефолты
    if i < len(colors):
        b_color = colors[i]
        b_size = sizes[i]
    else:
        b_color = 'white'
        b_size = 5
        
    # Сама точка планеты
    dot, = ax.plot([], [], 'o', color=b_color, ms=b_size, markeredgecolor='none')
    dots.append(dot)
    
    # Линия траектории (хвост)
    line, = ax.plot([], [], '-', color=b_color, alpha=0.2, lw=1)
    lines.append(line)

def init():
    for dot in dots:
        dot.set_data([], [])
    for line in lines:
        line.set_data([], [])
    return dots + lines

def update(frame):
    # Пропускаем шаги, чтобы анимация шла быстрее
    idx = frame * 10 
    if idx >= steps: idx = steps - 1
    
    for i in range(n_bodies):
        # Текущая позиция
        x, y = history[idx, i]
        dots[i].set_data([x], [y])
        
        # Хвост (последние 1000 шагов для красивого шлейфа)
        start = max(0, idx - 1000)
        trail_x = history[start:idx, i, 0]
        trail_y = history[start:idx, i, 1]
        lines[i].set_data(trail_x, trail_y)
        
    return dots + lines

# Запускаем анимацию!
ani = FuncAnimation(fig, update, frames=steps // 10, 
                    init_func=init, blit=True, interval=20)

plt.title("N-Body Simulation: Custom Universe", color='white', fontsize=14)
plt.show()
