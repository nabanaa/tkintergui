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
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from scipy.interpolate import make_interp_spline
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
        self.LENGTH = 200  # D??ugo???? nici wahad??a
        self.RADIUS = 10  # Promie?? kuli wahad??a
        self.GRAVITY = 0.981  # Przyspieszenie ziemskie
        self.czas1 = [x for x in range(0, 100000)]
        self.kat_poczatkowy = math.pi / 4
        self.theta = self.kat_poczatkowy * math.cos(math.sqrt(self.GRAVITY / self.LENGTH) * self.czas1[0])
        self.x0 = 240
        self.y0 = 10
        self.__xtimer = 0
        self.wartosci_kinetyczna = [0]
        self.wartosci_potencjalna = [0]
        self.start_time = tk.StringVar(self, "0", "my_Var")
        self.stop_time = tk.StringVar(self, "0", "my_Var2")
        self.window()

    def start(self):
        self.t1 = Thread2(target=self.dodaj_pkt, args=())
        self.t1.daemon = True
        self.t1.start()
        self.t2 = Thread2(target=self.animacja, args=(self.theta, self.czas1))
        self.t2.daemon = True
        self.t2.start()
        self.set_but["state"] = "disabled"

    def stop(self):
        if self.ready == True:
            self.set_but["state"] = "normal"
            self.t1.stop()
            self.t2.stop()
            self.ready = False
    def clear_plot(self):
        self.axs[0].clear()
        self.axs[1].clear()
        self.plot_Energia()
        self.canvas.draw()

    def p_grid(self):
        self.ax.grid()
        self.canvas.draw()
    def set_params(self):
        if self.ready == True:
            self.ready = False
        self.ready = True
        self.start_but["state"] = "normal"
        self.clear_plot()
        self.canvas.draw()

    def generuj_sinusa(self, i=0):
        x = [s/100 for s in range(i, i+500)]
        y = [random.random() for a in range(i, i+500)]
        return x, y
    
   # def pobierz_dane(self):


    def dodaj_pkt(self):
        self.start_but["state"] = "disabled"

        k = 0
        h = 0
 
        while True:
            z = 0
            for x in range(k, k+2):
                self.axs[0].set_xlim(k, k+1)
                self.canvas.draw()
                self.slupekBox.coords(self.kinetyczna, 75, 269 - (self.wartosci[x] * 50), 230, 270)
                self.slupekBox.coords(self.potencjalna, 270, 269 - ((2-self.wartosci[x]) * 50), 415, 270)
                self.EnergiaPotencjalna.config(text=f'  Energia potencjalna = {round((2-self.wartosci[x]), 3)} N')
                self.EnergiaKinetyczna.config(text=f'   Energia kinetyczna = {round(self.wartosci[x], 3)} N')
            k +=1
            h += 500
            self.czas3, self.wartosci = self.generuj_sinusa(h)
            self.axs[0].plot(self.czas3, self.wartosci)
            self.axs[1].plot(self.czas3, self.wartosci)

    def plot_Energia(self):
        self.fig = Figure(figsize=(2, 1))
        self.axs = self.fig.subplots(2, 1)
        self.czas3, self.wartosci=self.generuj_sinusa()
        self.scatter0 = self.axs[0].plot(self.czas3, self.wartosci)  # potencjalna liniowa
        self.axs[0].set_title("Energia Potencjalna")
        self.axs[0].set_ylim(-1, 3)
        self.axs[0].set_xlim(-1, 0)

        self.scatter1 = self.axs[1].plot(self.czas3, self.wartosci)  # kinetyczna liniowa
        self.axs[1].set_title("Energia Kinetyczna")
        self.axs[1].sharey(self.axs[0])
        self.axs[1].sharex(self.axs[0])

        self.axs[0].grid(True)
        self.axs[1].grid(True)
        self.fig.subplots_adjust(bottom=0.05)
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
        if self.ready==False:
            time=0
        self.after(35, self.animacja, self.new_angle, time)




    def window(self):
        """look and feel"""
        self.name_label = tk.Label(self, text=f"App")
        fontSize = 16
        # self.Xpos = tk.Label(self, text=f"X = }", font=("Arial", fontSize), anchor="w", padx=20)
        # self.Ypos = tk.Label(self, text=f"Y = ", font=("Arial", fontSize))
        self.EnergiaPotencjalna = tk.Label(self, text=f"Energia potencjalna = ", font=("Arial", fontSize))
        self.EnergiaKinetyczna = tk.Label(self, text=f"Energia Kinetyczna = ", font=("Arial", fontSize))
        # self.Predkosc = tk.Label(self, text=f"Predkosc = ", font=("Arial", fontSize))
        # self.Przyspieszenie = tk.Label(self, text=f"Przyspieszenie = ", font=("Arial", fontSize))
        self.autorzy = tk.Label(self, text=f"Autorzy: \n mgr in??. Karol Liszka \n Marcin Partyka \n B??a??ej Pietryja", font=("Arial", fontSize))
        self.animacjaBox = tk.Canvas(self, width=500, height=400, bg="white")
        self.set_but = tk.Button(self, text=f"unlock start button", command=lambda: self.set_params(),
                                 font=("Arial", fontSize))
        self.start_but = tk.Button(self, text=f"Start experiment", command=lambda: self.start(), font=("Arial", fontSize))
        self.start_but["state"] = "disabled"
        self.stop_but = tk.Button(self, text=f"STOP", command=lambda: self.stop(), fg="red", font=("Arial", fontSize))
        self.clear_plot_but = tk.Button(self, text=f"Clear plot", command=lambda: self.clear_plot(), font=("Arial", fontSize))
        self.slupekBox = tk.Canvas(self, width=500, height=400, bg="white")
        self.ball = self.animacjaBox.create_oval(250 - self.RADIUS, 210 - self.RADIUS, 250 + self.RADIUS,
                                                 210 + self.RADIUS, fill='blue')
        self.ceil = self.animacjaBox.create_rectangle(230, 10, 270, 11, fill='black')
        self.rod = self.animacjaBox.create_line(250, 10, 250, 210)
        self.kinetyczna_label= tk.Label(self.slupekBox, text='Energia Kinetyczna', bg='white')
        self.potencjalna_label = tk.Label(self.slupekBox, text='Energia Potencjalna', bg='white')
        self.slupekBox.create_window(150, 10, window=self.kinetyczna_label)
        self.slupekBox.create_window(340, 10, window=self.potencjalna_label)
        self.kinetyczna = self.slupekBox.create_rectangle(75, 269, 230, 270, fill='blue')
        self.potencjalna = self.slupekBox.create_rectangle(270, 269, 415, 270, fill='orange')
        self.plot_Energia()
        self.__place_all()

    def __place_all(self):
        self.name_label.place(anchor=tk.NW, x=10, y=10, width=1900, height=30)
        Upheight = 80
        Upwidth = 300
        UpXpos = 60
        UpYpos = 50
        # self.Xpos.place(anchor=tk.NW, x=UpXpos, y=UpYpos, width=Upwidth, height=Upheight)
        # self.Ypos.place(anchor=tk.NW, x=UpXpos + 300, y=UpYpos, width=Upwidth, height=Upheight)
        self.EnergiaPotencjalna.place(anchor=tk.NW, x=UpXpos + 600, y=UpYpos, width=Upwidth, height=Upheight)
        self.EnergiaKinetyczna.place(anchor=tk.NW, x=UpXpos + 900, y=UpYpos, width=Upwidth, height=Upheight)
        # self.Predkosc.place(anchor=tk.NW, x=UpXpos + 1200, y=UpYpos, width=Upwidth, height=Upheight)
        # self.Przyspieszenie.place(anchor=tk.NW, x=UpXpos + 1500, y=UpYpos, width=Upwidth, height=Upheight)
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