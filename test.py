from tkinter import *
import math


LENGTH = 300 # Długość nici wahadła
RADIUS = 5   # Promień kuli wahadła
GRAVITY = 0.981 # Przyspieszenie ziemskie
czas=[x for x in range(0, 100000)]
kat_poczatkowy=math.pi/4
theta=kat_poczatkowy*math.cos(math.sqrt(GRAVITY/LENGTH)*czas[0])
x0=250
y0=10
# Inicjalizacja okna Tkinter
root = Tk()
root.title("Animacja wahadła")

# Ustawienia dla płótna, na którym będzie rysowane wahadło
canvas = Canvas(root, width=500, height=400, bg='white')
canvas.pack()

# Utworzenie kuli reprezentującej wahadło
ball = canvas.create_oval(250-RADIUS, 100-RADIUS, 250+RADIUS, 100+RADIUS, fill='blue')
ceil = canvas.create_rectangle(230, 10, 270, 11, fill='black')
rod = canvas.create_line(250, 10, 250, 310)

# Funkcja do rysowania wahadła w nowej pozycji
def animate(angle, time):
    x=x0+LENGTH*math.sin(angle)
    y=y0+LENGTH*math.cos(angle)
    canvas.coords(ball, x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS)
    canvas.coords(rod, 250, 10, x, y)
    new_angle = theta * math.cos(math.sqrt(GRAVITY / LENGTH) * time[0])
    time=time[1:]
    root.after(35, animate, new_angle, time)

animate(theta, czas)

# Uruchomienie pętli głównej programu
root.mainloop()
