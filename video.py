import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# 1. Загружаем данные
try:
    history = np.load('orbit_data.npy')
    print("Данные загружены, начинаю рендер видео... м-ня! 🐾")
except FileNotFoundError:
    print("Ошибка: Сначала запусти просчет (main.py), чтобы создать orbit_data.npy")
    exit()

steps, n_bodies, _ = history.shape

# 2. Настройка графики (как в дисплее, но чуть строже)
fig, ax = plt.subplots(figsize=(10, 10), dpi=100) # dpi=100 даст 1000x1000 пикселей
ax.set_aspect('equal')
ax.set_facecolor('black')
fig.patch.set_facecolor('black') # Цвет рамки вокруг графика

# Масштаб (подбери под свои данные)
limit = 1.6e11 
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)

# Оформление (убираем оси для красоты)
ax.axis('off')

colors = ['yellow', 'deepskyblue', 'white']
sizes = [20, 8, 4]
dots = []
lines = []

for i in range(n_bodies):
    line, = ax.plot([], [], '-', color=colors[i], alpha=0.2, lw=1)
    dot, = ax.plot([], [], 'o', color=colors[i], ms=sizes[i])
    dots.append(dot)
    lines.append(line)

def update(frame):
    # Ускоряем видео: берем каждый 50-й шаг просчета
    idx = frame * 50
    if idx >= steps: idx = steps - 1
    
    for i in range(n_bodies):
        x, y = history[idx, i]
        dots[i].set_data([x], [y])
        
        # Длинный хвост для видео
        start = max(0, idx - 2000)
        lines[i].set_data(history[start:idx, i, 0], history[start:idx, i, 1])
        
    return dots + lines

# 3. Настройка записи
metadata = dict(title='Orbital Simulation', artist='Miki & Yarik')
writer = FFMpegWriter(fps=30, metadata=metadata, bitrate=2000)

# frames = общее кол-во шагов / шаг пропуска
total_frames = steps // 50

ani = FuncAnimation(fig, update, frames=total_frames, blit=True)

# Сохраняем
print(f"Рендер {total_frames} кадров. Пожалуйста, подожди...")
ani.save("planetary_system.mp4", writer=writer)
print("Видео готово! Теперь точно все афигеют Nya! ✨")
