import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 1. Загружаем наши данные
# history имеет форму (steps, n_bodies, 2)
history = np.load('orbit_data.npy')
steps, n_bodies, _ = history.shape

# 2. Настройка графика
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')
ax.set_facecolor('black') # Космос же! м-ня 🐾

# Ограничиваем оси (подбери под свои данные, для СИ это будут огромные числа)
# Например, для системы Земля-Солнце:
limit = 1.6e11 
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)

# Создаем объекты для каждой планеты
# Разные цвета: Солнце - желтое, Земля - голубая, Луна - белая
colors = ['yellow', 'deepskyblue', 'white']
sizes = [15, 6, 3]
dots = []

for i in range(n_bodies):
    dot, = ax.plot([], [], 'o', color=colors[i], ms=sizes[i])
    dots.append(dot)

# Добавим линии траекторий (хвосты), чтобы было научненько
lines = []
for i in range(n_bodies):
    line, = ax.plot([], [], '-', color=colors[i], alpha=0.3, lw=1)
    lines.append(line)

def init():
    for dot in dots:
        dot.set_data([], [])
    for line in lines:
        line.set_data([], [])
    return dots + lines

def update(frame):
    # Пропускаем шаги, чтобы анимация шла быстрее (например, каждый 10-й шаг)
    idx = frame * 10 
    if idx >= steps: idx = steps - 1
    
    for i in range(n_bodies):
        # Текущая позиция
        x, y = history[idx, i]
        dots[i].set_data([x], [y])
        
        # Хвост (последние 500 шагов для красоты)
        start = max(0, idx - 500)
        trail_x = history[start:idx, i, 0]
        trail_y = history[start:idx, i, 1]
        lines[i].set_data(trail_x, trail_y)
        
    return dots + lines

# Запускаем! 
# frames — сколько кадров будет в анимации
ani = FuncAnimation(fig, update, frames=steps // 10, 
                    init_func=init, blit=True, interval=20)

plt.title("N-Body Simulation: Earth-Moon-Sun System", color='white')
plt.show()
