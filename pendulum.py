from vpython import *

# ustalamy parametry symulacji
length = 2  # długość wahadła w metrach
mass = 1  # masa wahadła w kilogramach
gravity = 9.81  # przyspieszenie ziemskie w m/s^2
damping = 0.1  # współczynnik tłumienia

# tworzymy obiekty graficzne
ceiling = box(pos=vector(0, 0, 0), size=vector(0.2, 0.2, 0.2), color=color.white)
arm = cylinder(pos=vector(0, 0, 0), axis=vector(length, 0, 0), radius=0.01, color=color.green)
bob = sphere(pos=vector(length, 0, 0), radius=0.1, color=color.red)

# ustalamy początkowe warunki
theta = 1  # wychylenie wahadła w radianach
omega = 0  # prędkość kątowa wahadła w radianach na sekundę
dt = 0.01  # czas trwania kroku symulacji w sekundach

# tworzymy pętlę animacji
while True:
    rate(100)  # ograniczamy szybkość animacji do 100 klatek na sekundę
    alpha = -gravity/length * sin(theta) - damping*omega  # przyspieszenie kątowe wahadła z uwzględnieniem tłumienia
    omega += alpha*dt  # aktualizujemy prędkość kątową
    theta += omega*dt  # aktualizujemy położenie kątowe
    bob.pos = vector(length*sin(theta), -length*cos(theta), 0)  # aktualizujemy położenie wahadła
    arm.axis = bob.pos  # aktualizujemy położenie ramienia