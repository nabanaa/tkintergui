import tkinter as tk
import math
import tkinter.ttk as ttk
from tkinter import font as tkfont
import os, sys
import threading
import multiprocessing
from multiprocessing import Pipe, Process, Value, Array
import numpy as np
import time
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from functools import partial


class StopThread(StopIteration):
    pass


threading.SystemExit = SystemExit, StopThread


class Thread2(threading.Thread):

    def stop(self):
        self.__stop = True

    def _bootstrap(self):
        if threading._trace_hook is not None:
            raise ValueError('Cannot run thread with tracing!')
        self.__stop = False
        sys.settrace(self.__trace)
        super()._bootstrap()

    def __trace(self, frame, event, arg):
        if self.__stop:
            raise StopThread()
        return self.__trace


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        # self.attributes("-fullscreen", 1)
        self.geometry("1900x1060+0+0")
        self.bind('<Escape>', lambda event: self.koncz())
        self.style = ttk.Style()
        self.style.configure("BW.TLabel", foreground="black", background="green")
        self.container = tk.Frame(self, width=1900, height=1060)
        self.container.place(x=0, y=0)
        self.containers = {}
        self.cokolwiek = {}

        self.containers[1] = tk.Frame(self, width=1900, height=1060, bg="green")
        self.containers[1].place(x=1 * 0, y=0)
        tk.Label(self.containers[1], text=f"{1}").place(x=200, y=20)
        self.cokolwiek[1] = klasa_cokolwiek(parent=self.containers[1], controller=self, address=1 + 1)
        self.cokolwiek[1].place(x=0, y=0)

    def koncz(self):
        self.quit()


class klasa_cokolwiek(tk.Frame):
    def __init__(self, parent, controller, address=1):

        tk.Frame.__init__(self, parent, height=1060, width=1900)
        self.parent = parent
        self.controller = controller
        self.address = address
        self.c = tk.Canvas(self, width=1890, height=1050, highlightthickness=5, bg="#8F8F8F")
        self.c.place(x=0, y=0)
        self.ready = False
        self.LENGTH = 125  # Długość nici wahadła
        self.RADIUS = 5  # Promień kuli wahadła
        self.GRAVITY = 0.981  # Przyspieszenie ziemskie
        self.czas = [x for x in range(0, 100000)]
        self.kat_poczatkowy = math.pi / 4
        self.theta = self.kat_poczatkowy * math.cos(math.sqrt(self.GRAVITY / self.LENGTH) * self.czas[0])
        self.x0 = 240
        self.y0 = 10
        self.__xtimer = 0
        self.__xtimer2 = 0
        self.__xtimer3 = 0
        self.__xtimer4 = 0

        self.start_time = tk.StringVar(self, "0", "my_Var")
        self.stop_time = tk.StringVar(self, "0", "my_Var2")
        self.window()

    def start(self):
        self.t = Thread2(target=self.dodaj_pkt, args=())
        self.t.daemon = True
        self.t.start()
        self.set_but["state"] = "disabled"

    def clear_plot(self):
        self.scatter0.set_offsets(np.c_[[], []])
        self.scatter1.set_offsets(np.c_[[], []])
        self.canvas.draw()

    def p_grid(self):
        self.ax.grid()
        self.canvas.draw()
    def stop(self):
        if self.ready == True:
            self.set_but["state"] = "normal"
            self.t.stop()
            self.ready = False
    def set_params(self):
        if self.ready == True:
            self.ready = False
        self.ready = True
        self.start_but["state"] = "normal"
        self.clear_plot()
        self.canvas.draw()

    def dodaj_pkt(self):
        for k in range(1000):
            for u in range(10):
                x = self.scatter0.get_offsets()[:, 0].tolist()
                y = self.scatter0.get_offsets()[:, 1].tolist()
                z = self.scatter1.get_offsets()[:, 1].tolist()
                if len(x) == 0:
                    x.append(0)
                else:
                    x.append(time.time() - self.__xtimer)
                zmi=np.sin(time.time()*7)
                y.append(zmi)
                z.append(-zmi)
                xx = np.c_[x, y]
                yy = np.c_[x, z]
                self.scatter0.set_offsets(xx)
                self.scatter1.set_offsets(yy)
                self.axs[0].set_xlim(x[-1]-3, x[-1] + 1)
                self.axs[1].set_xlim(x[-1]-3, x[-1] + 1)
            
            z=z[11:]
            x=x[11:]
            y=y[11:]
            self.canvas.draw()


    def plot_Energia(self):
        self.fig = Figure(figsize=(2, 1))
        self.axs = self.fig.subplots(2, 1)
        self.scatter0 = self.axs[0].scatter([], [])  # potencjalna liniowa
        self.axs[0].set_title("potencja")
        self.axs[0].set_ylim(-2, 2)

        self.scatter1 = self.axs[1].scatter([], [])  # kinetyczna liniowa
        self.axs[1].set_title("potencja")
        self.axs[1].sharey(self.axs[0])

        self.axs[0].grid(True)
        self.axs[1].grid(True)
        self.fig.subplots_adjust(bottom=0.20)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=120, y=150, width=750, height=600)


    def animacja(self, angle, time):

        self.x = self.x0 + self.LENGTH * math.sin(angle)
        self.y = self.y0 + self.LENGTH * math.cos(angle)
        self.animacjaBox.coords(self.ball, self.x - self.RADIUS, self.y - self.RADIUS, self.x + self.RADIUS,
                                self.y + self.RADIUS)
        self.animacjaBox.coords(self.rod, 250, 10, self.x, self.y)
        self.new_angle = self.theta * math.cos(math.sqrt(self.GRAVITY / self.LENGTH) * time[0])
        time = time[1:]
        self.after(35, self.animacja, self.new_angle, time)
        # Definicje przyciskow

    def rectangle_animation(self):
        #canvas = self.slupekBox
        #canvas.pack()
        rect1 = None
        rect2 = None
        value1 = 0
        value2 = 0

        def animate():
            nonlocal rect1, rect2, value1, value2
            value1 += 1
            value2 += 2
            if rect1:
                self.slupekBox.delete(rect1)
            if rect2:
                self.slupekBox.delete(rect2)
            rect1 = self.slupekBox.create_rectangle(160, 450-value1, 210 , 470, fill="red")
            rect2 = self.slupekBox.create_rectangle(100, 450-value2, 150, 470, fill="blue")
            self.after(50, animate)

        animate()
    def window(self):
        """look and feel"""
        self.name_label = tk.Label(self, text=f"App")
        fontSize = 16
        self.Xpos = tk.Label(self, text=f"X = ", font=("Arial", fontSize), anchor="w", padx=20)
        self.Ypos = tk.Label(self, text=f"Y = ", font=("Arial", fontSize))
        self.EnergiaPotencjalna = tk.Label(self, text=f"Energia potencjalna = ", font=("Arial", fontSize))
        self.EnergiaKinetyczna = tk.Label(self, text=f"Energia Kinetyczna = ", font=("Arial", fontSize))
        self.Predkosc = tk.Label(self, text=f"Predkosc = ", font=("Arial", fontSize))
        self.Przyspieszenie = tk.Label(self, text=f"Przyspieszenie = ", font=("Arial", fontSize))
        self.dlugosc = tk.Label(self, text=f"Podaj dlugosc ", font=("Arial", fontSize))
        self.waga = tk.Label(self, text=f"Podaj wage ", font=("Arial", fontSize))
        self.autorzy = tk.Label(self, text=f"marcin, blazej", font=("Arial", fontSize))
        self.animacjaBox = tk.Canvas(self, width=500, height=400, bg="white")
        self.set_but = tk.Button(self, text=f"unlock start button", command=lambda: self.set_params(),
                                 font=("Arial", fontSize))
        self.start_but = tk.Button(self, text=f"Start experiment", command=lambda: self.start(),
                                   font=("Arial", fontSize))
        self.start_but["state"] = "disabled"
        self.stop_but = tk.Button(self, text=f"STOP", command=lambda: self.stop(), fg="red", font=("Arial", fontSize))
        self.clear_plot_but = tk.Button(self, text=f"Clear plot", command=lambda: self.clear_plot(), font=("Arial", fontSize))
        self.slupekBox = tk.Canvas(self, width=500, height=400, bg="white")
        self.ball = self.animacjaBox.create_oval(250 - self.RADIUS, 100 - self.RADIUS, 250 + self.RADIUS, 100 + self.RADIUS, fill='blue')
        self.ceil = self.animacjaBox.create_rectangle(230, 10, 270, 11, fill='black')
        self.rod = self.animacjaBox.create_line(250, 10, 250, 310)
        #self.slup_potencja= self.slupekBox.
        self.rect2 = None
        self.value1 = 0
        self.value2 = 0
        #self.animate()
        self.animacja(self.theta, self.czas)
        self.plot_Energia()
        self.__place_all()
    def __place_all(self):
        self.name_label.place(anchor=tk.NW, x=10, y=10, width=1900, height=30)
        Upheight = 80
        Upwidth = 260
        UpXpos = 60
        UpYpos = 50
        self.Xpos.place(anchor=tk.NW, x=UpXpos, y=UpYpos, width=Upwidth, height=Upheight)
        self.Ypos.place(anchor=tk.NW, x=UpXpos + 300, y=UpYpos, width=Upwidth, height=Upheight)
        self.EnergiaPotencjalna.place(anchor=tk.NW, x=UpXpos + 600, y=UpYpos, width=Upwidth, height=Upheight)
        self.EnergiaKinetyczna.place(anchor=tk.NW, x=UpXpos + 900, y=UpYpos, width=Upwidth, height=Upheight)
        self.Predkosc.place(anchor=tk.NW, x=UpXpos + 1200, y=UpYpos, width=Upwidth, height=Upheight)
        self.Przyspieszenie.place(anchor=tk.NW, x=UpXpos + 1500, y=UpYpos, width=Upwidth, height=Upheight)
        self.dlugosc.place(anchor=tk.NW, x=40, y=800, width=200, height=50)
        self.waga.place(anchor=tk.NW, x=40, y=900, width=200, height=50)
        self.animacjaBox.place(anchor=tk.NW, x=1000, y=150, width=500, height=280)
        self.slupekBox.place(anchor=tk.NW, x=1000, y=470, width=500, height=280)
        self.autorzy.place(anchor=tk.NW, x=1600, y=820, width=200, height=100)
        self.set_but.place(anchor=tk.NW, x=1650, y=310, width=200, height=60)
        self.start_but.place(x=1650, y=390, anchor=tk.NW, width=200, height=60)
        self.stop_but.place(x=1650, y=470, anchor=tk.NW, width=200, height=60)
        self.clear_plot_but.place(x=1650, y=550, anchor=tk.NW, width=200, height=60)
if __name__ == "__main__":
    app = App()
    # Thread(app.drive).start()
    # app.bind('<Escape>',lambda event: app.destroy())
    app.mainloop()