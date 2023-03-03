from tkinter import *
import math


LENGTH = 200 # Długość nici wahadła
RADIUS = 10   # Promień kuli wahadła
GRAVITY = 9.81 # Przyspieszenie ziemskie
czas=[x for x in range(0, 100000)]
kat_poczatkowy=math.pi/4
theta=kat_poczatkowy*math.cos(math.sqrt(GRAVITY/LENGTH)*czas[0])
x0=960
y0=700
# Inicjalizacja okna Tkinter
root = Tk()
root.title("Animacja wahadła")

# Ustawienia dla płótna, na którym będzie rysowane wahadło
canvas = Canvas(root, width=1920, height=1080, bg='white')
canvas.pack()

# Utworzenie kuli reprezentującej wahadło
ball = canvas.create_oval(250-RADIUS, 100-RADIUS, 250+RADIUS, 100+RADIUS, fill='blue')

# Funkcja do rysowania wahadła w nowej pozycji
def animate(angle, time):
    x=x0+LENGTH*math.sin(angle)
    y=y0+LENGTH*math.cos(angle)
    canvas.coords(ball, x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS)
    new_angle = theta * math.cos(math.sqrt(GRAVITY / LENGTH) * time[0])
    time=time[1:]
    root.after(50, animate, new_angle, time)

animate(theta, czas)

# Uruchomienie pętli głównej programu
root.mainloop()