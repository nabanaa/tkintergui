import tkinter as tk
import math


import tkinter.ttk as ttk
from tkinter import font as tkfont



import os,sys
import threading
import multiprocessing
from multiprocessing import Pipe,Process,Value,Array
import numpy as np
import time
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


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
        #self.attributes("-fullscreen", 1)
        self.geometry("1920x1080+0+0")
        self.bind('<Escape>',lambda event: self.koncz())
        self.style = ttk.Style()
        self.style.configure("BW.TLabel", foreground="black", background="green")
        self.container = tk.Frame(self,width=1920,height=1080)
        self.container.place(x=0,y=0)
        self.containers = {}
        self.cokolwiek = {}

        self.containers[1] = tk.Frame(self,width=1920,height=1080,bg="green")
        self.containers[1].place(x=1*0,y=0)
        tk.Label(self.containers[1],text=f"{1}").place(x=200,y=20)
        self.cokolwiek[1] = klasa_cokolwiek(parent=self.containers[1], controller=self,address=1+1)
        self.cokolwiek[1].place(x=0,y=0)

    def koncz(self):
        self.quit()


class klasa_cokolwiek(tk.Frame):
    def __init__(self, parent, controller, address=1):

        tk.Frame.__init__(self,parent,height=1080,width=1920)
        self.parent = parent
        self.controller = controller
        self.address = address

        self.c = tk.Canvas(self,width=1910,height=1070,highlightthickness=5,bg="#8F8F8F")
        self.c.place(x=0,y=0)
        self.ready=False

        self.LENGTH = 300 # Długość nici wahadła
        self.RADIUS = 5   # Promień kuli wahadła
        self.GRAVITY = 0.981 # Przyspieszenie ziemskie
        self.czas=[x for x in range(0, 100000)]
        self.kat_poczatkowy=math.pi/4
        self.theta=self.kat_poczatkowy*math.cos(math.sqrt(self.GRAVITY/self.LENGTH)*self.czas[0])
        self.x0=250
        self.y0=10

        self.start_time = tk.StringVar(self,"0","my_Var")
        self.stop_time = tk.StringVar(self,"0","my_Var2")
        self.window()



    def randomuj(self,num=10000):
        if self.ready:
            self.start_but["state"]= "disabled"

            time.sleep(1)
            i = 0
            self.__xtimer = time.time()
            while (i < num):
                time.sleep(0.01)
                self.dodaj_ptk()
                i+=1
            self.ready=False

        else:
            print("you should set parameters")

    def start(self):
        self.t = Thread2(target=self.randomuj,args=())
        self.t.daemon=True
        self.t.start()
        self.set_but["state"]= "disabled"

    def clear_plot(self):
        self.scatter.set_offsets(np.c_[[],[]])
        self.canvas.draw()

    def p_grid(self):
        self.ax.grid()
        self.canvas.draw()

    def stop(self):
        if self.ready == True:
            self.set_but["state"]= "normal"
            self.t.stop()
            self.ready = False

    def set_params(self):
        if self.ready==True:
            self.ready=False
        self.ready = True
        self.start_but["state"]= "normal"
        self.clear_plot()
        self.canvas.draw()

    def dodaj_ptk(self):
        t = np.random.randint(100)
        x=self.axs[0,0].get_offsets()[:,0].tolist()
        y=self.axs[0,0].get_offsets()[:,1].tolist()
        if len(x) ==0:
            x.append(0)
        else:
            x.append(time.time()-self.__xtimer)
        y.append(t)
        xx = np.c_[x,y]
        self.axs[0,0].set_offsets(xx)
        self.axs[0,0].set_xlim(0,x[-1]+1)
        self.canvas.draw()
        return t

    def plot_Energia(self):
        self.fig = Figure(figsize=(1,1))
        self.axs = self.fig.subplots(2, 2)
        self.axs[0, 0].scatter([], [])
        self.axs[0, 0].set_title("main")
        self.axs[1, 0].scatter([], [])
        self.axs[1, 0].set_title("shares x with main")
        self.axs[1, 0].sharex(self.axs[0, 0])
        self.axs[0, 1].scatter([], [])
        self.axs[0, 1].set_title("unrelated")
        self.axs[1, 1].scatter([], [])
        self.axs[1, 1].set_title("also unrelated")
        self.axs[0, 0].grid(True)
        self.axs[0, 1].grid(True)
        self.axs[1, 0].grid(True)
        self.axs[1, 1].grid(True)
        # self.fig.tight_layout()
        self.fig.subplots_adjust(bottom=0.20)
        self.canvas = FigureCanvasTkAgg(self.fig,master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=120,y=150,width=1500,height=600)

    # def plot_EnergiaKinSlup(self):
    #     self.fig = Figure(figsize=(1,1))
    #     self.ax = self.fig.add_subplot(111)
    #     self.ax.set_xlim(0,2)                   # Skala wykresu
    #     self.ax.set_ylim(-10,100)
    #     self.ax.set_xlabel("2[sec]",fontsize=10)
    #     self.ax.set_ylabel("random[random]",fontsize=10)
    #     self.ax.grid(True)
    #     self.scatter = self.ax.scatter([],[])
    #     self.fig.subplots_adjust(bottom=0.20)
    #     self.canvas = FigureCanvasTkAgg(self.fig,master=self)
    #     self.canvas.draw()
    #     self.canvas.get_tk_widget().place(x=1000,y=150,width=550,height=280)

    # def plot_EnergiaLin(self, tag, place):
    #     self.fig = Figure(figsize=(1,1))
    #     self.ax = self.fig.add_subplot(111)
    #     self.ax.set_xlim(0,2)                   # Skala wykresu
    #     self.ax.set_ylim(-10,100)
    #     self.ax.set_xlabel(f"{tag}[sec]",fontsize=10)
    #     self.ax.set_ylabel("random[random]",fontsize=10)
    #     self.ax.grid(True)
    #     self.scatter = self.ax.scatter([],[])
    #     self.fig.subplots_adjust(bottom=0.20)
    #     self.canvas = FigureCanvasTkAgg(self.fig,master=self)
    #     self.canvas.draw()
    #     self.canvas.get_tk_widget().place(x=120+880*place,y=450,width=550,height=280)

    # def plot_EnergiaKinLin(self):
    #     self.fig = Figure(figsize=(1,1))
    #     self.ax = self.fig.add_subplot(111)
    #     self.ax.set_xlim(0,2)                   # Skala wykresu
    #     self.ax.set_ylim(-10,100)
    #     self.ax.set_xlabel("4[sec]",fontsize=10)
    #     self.ax.set_ylabel("random[random]",fontsize=10)
    #     self.ax.grid(True)
    #     self.scatter = self.ax.scatter([],[])
    #     self.fig.subplots_adjust(bottom=0.20)
    #     self.canvas = FigureCanvasTkAgg(self.fig,master=self)
    #     self.canvas.draw()
    #     self.canvas.get_tk_widget().place(x=1000,y=450,width=550,height=280)

    #def anim_setup(self):
        


    def animacja(self, angle, time):

        self.x=self.x0+self.LENGTH*math.sin(angle)
        self.y=self.y0+self.LENGTH*math.cos(angle)
        self.animacjaBox.coords(self.ball, self.x - self.RADIUS, self.y - self.RADIUS, self.x + self.RADIUS, self.y + self.RADIUS)
        self.animacjaBox.coords(self.rod, 250, 10, self.x, self.y)
        self.new_angle = self.theta * math.cos(math.sqrt(self.GRAVITY / self.LENGTH) * time[0])
        time=time[1:]
        self.after(35, self.animacja, self.new_angle, time)


                        # Definicje przyciskow
    def window(self):
        """look and feel"""
        self.name_label = tk.Label(self,text=f"App")
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
        self.set_but = tk.Button(self,text=f"unlock start button",command = lambda: self.set_params(), font=("Arial", fontSize))
        self.start_but = tk.Button(self,text=f"Start experiment",command = lambda: self.start(), font=("Arial", fontSize))
        self.start_but["state"]= "disabled"
        self.stop_but = tk.Button(self,text=f"STOP",command = lambda: self.stop(),fg="red", font=("Arial", fontSize))
        

        self.ball = self.animacjaBox.create_oval(250-self.RADIUS, 100-self.RADIUS, 250+self.RADIUS, 100+self.RADIUS, fill='blue')
        self.ceil = self.animacjaBox.create_rectangle(230, 10, 270, 11, fill='black')
        self.rod = self.animacjaBox.create_line(250, 10, 250, 310)

        self.animacja(self.theta, self.czas)
        self.plot_Energia()
        # self.plot_Energia('2', 0, 1)
        # self.plot_Energia('3', 1, 0)
        # self.plot_Energia('4', 1, 1)
        self.__place_all()

                    # Rozmieszczenie przyciskow
    def __place_all(self):
        self.name_label.place(anchor=tk.NW,x=10,y=10,width=1900,height=30)
        Upheight = 80
        Upwidth = 260
        UpXpos = 60
        UpYpos = 50
        self.Xpos.place(anchor=tk.NW, x=UpXpos, y=UpYpos, width=Upwidth, height=Upheight)
        self.Ypos.place(anchor=tk.NW, x=UpXpos+300, y=UpYpos, width=Upwidth, height=Upheight)
        self.EnergiaPotencjalna.place(anchor=tk.NW, x=UpXpos+600, y=UpYpos, width=Upwidth, height=Upheight)
        self.EnergiaKinetyczna.place(anchor=tk.NW, x=UpXpos+900, y=UpYpos, width=Upwidth, height=Upheight)
        self.Predkosc.place(anchor=tk.NW, x=UpXpos+1200, y=UpYpos, width=Upwidth, height=Upheight)
        self.Przyspieszenie.place(anchor=tk.NW, x=UpXpos+1500, y=UpYpos, width=Upwidth, height=Upheight)
        self.dlugosc.place(anchor=tk.NW, x=40, y=800, width=200, height=50)
        self.waga.place(anchor=tk.NW, x=40, y=900, width=200, height=50)
        self.animacjaBox.place(anchor=tk.NW, x=700, y=750, width=500, height=320)
        self.autorzy.place(anchor=tk.NW, x=1600, y=820, width=200, height=100)
        self.set_but.place(anchor=tk.NW,x=1650,y=310,width=200,height=60)
        self.start_but.place(x=1650,y=390,anchor=tk.NW,width=200,height=60)
        self.stop_but.place(x=1650,y=470,anchor=tk.NW,width=200,height=60)


if __name__ == "__main__":
    app = App()
    #Thread(app.drive).start()
    #app.bind('<Escape>',lambda event: app.destroy())
    app.mainloop()