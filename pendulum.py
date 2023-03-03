from vpython import *


length = 2  # metry
mass = 1  #kilogramy
gravity = 9.81
damping = 0.05  #tłumienie(do wywalenia później)

ceiling = box(pos=vector(0, 0, 0), size=vector(0.2, 0.2, 0.2), color=color.white)
arm = cylinder(pos=vector(0, 0, 0), axis=vector(length, 0, 0), radius=0.01, color=color.green)
bob = sphere(pos=vector(length, 0, 0), radius=0.1, color=color.red)


theta = 1  # wychylenie wahadła w radianach
omega = 0  # prędkość kątowa wahadła w radianach na sekundę
dt = 0.01  # czas trwania kroku symulacji w sekundach

while True:
    rate(100)  # 100fps
    alpha = -gravity/length * sin(theta) - damping*omega  # przyspieszenie kątowe wahadła z uwzględnieniem tłumienia
    omega += alpha*dt  # aktualizujemy prędkość kątową
    theta += omega*dt  # aktualizujemy położenie kątowe
    bob.pos = vector(length*sin(theta), -length*cos(theta), 0)  # aktualizujemy położenie wahadła
    arm.axis = bob.pos  # aktualizujemy położenie ramienia