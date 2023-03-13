import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import tkinter as tk

# Tworzenie okna tkinter
root = tk.Tk()
root.title("Animowany wykres sinusa")

# Tworzenie wykresu
fig, ax = plt.subplots()
x = np.arange(0, 2*np.pi, 0.01)
line, = ax.plot(x, np.sin(x))

# Funkcja animacji
def animate(i):
    line.set_ydata(np.sin(x + i/10.0))  # aktualizacja danych wykresu
    return line,

# Uruchamianie animacji
ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), interval=25, blit=True)

# Uruchomienie pętli zdarzeń
plt.show()
tk.mainloop()