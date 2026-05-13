import json
from body import Body
from math import sqrt
from variables import *
import numpy as np

# Параметры
def load_config(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    config_bodies = []
    for b in data['bodies']:
        new_body = Body(
            x=b['x'], y=b['y'], 
            m=b['m'], 
            vx=b['vx'], vy=b['vy']
        )
        # Можно временно сохранить цвет и размер прямо в объект, 
        # чтобы потом использовать при рендере
        new_body.color = b['color']
        new_body.size = b['size']
        config_bodies.append(new_body)
        
    return config_bodies, data['settings']

# Использование:
bodies, settings = load_config('config.json')
G = settings['G']
dt = settings['dt']
steps = settings['steps']

def calculate_total_energy(bodies_list):
    k_energy = 0
    p_energy = 0
    
    # 1. Считаем кинетическую энергию
    for b in bodies_list:
        v_sq = b.vx**2 + b.vy**2
        k_energy += 0.5 * b.m * v_sq
        
    # 2. Считаем потенциальную энергию (пары тел)
    for i in range(len(bodies_list)):
        for j in range(i + 1, len(bodies_list)):
            b1 = bodies_list[i]
            b2 = bodies_list[j]
            dx = b2.x - b1.x
            dy = b2.y - b1.y
            r = sqrt(dx**2 + dy**2)
            p_energy -= (G * b1.m * b2.m) / r
            
    return k_energy + p_energy

def update(dt):
    for i in bodies:
        i.x = i.x + i.vx*dt + 0.5*i.ax*dt**2
        i.y = i.y + i.vy*dt + 0.5*i.ay*dt**2

        i.vx = i.vx + 0.5*i.ax*dt
        i.vy = i.vy + 0.5*i.ay*dt

    for i in bodies:
        ax_total = 0
        ay_total = 0
        for j in bodies:
            if i == j: continue
    
            dx = j.x - i.x
            dy = j.y - i.y
            r = sqrt(dx**2 + dy**2)

            if r <= 0.5:
                exit() #FIX
            
            f = G * j.m / r**3
            
            ax_total += f * dx
            ay_total += f * dy

        i.ax = ax_total
        i.ay = ay_total
    
    for i in bodies:
        i.vx = i.vx + 0.5*i.ax*dt
        i.vy = i.vy + 0.5*i.ay*dt

    

energy_history = np.zeros(steps)
history = np.zeros((steps, len(bodies), 2))

for i in range(steps):
    update(dt)
    for b_idx, body in enumerate(bodies):
        history[i, b_idx] = [body.x, body.y]
    energy_history[i] = calculate_total_energy(bodies)

np.save('orbit_data.npy', history)
np.save('energy_history.npy', energy_history)
print("Просчет окончен, м-ня! 🐾")
