import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('TkAgg')

energy = np.load('energy_history.npy')
time = np.arange(len(energy))

plt.figure(figsize=(10, 5))
plt.plot(time, energy, color='green', label='Total Energy')

# Нюанс: чтобы увидеть колебания, нужно настроить масштаб осей
# Относительное изменение энергии (должно быть очень маленьким)
relative_error = (energy - energy[0]) / energy[0]
plt.plot(time, relative_error, color='red', label='Relative Error')

plt.title("Conservation of Energy (Stability Check)")
plt.xlabel("Time steps")
plt.ylabel("Energy / Relative Error")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
