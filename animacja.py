import tkinter as tk

def rectangle_animation(master):
    canvas = tk.Canvas(master, width=500, height=500)
    canvas.pack()
    rect1 = None
    rect2 = None
    value1 = 0
    value2 = 0

    def animate():
        nonlocal rect1, rect2, value1, value2
        value1 += 1
        value2 += 2
        if rect1:
            canvas.delete(rect1)
        if rect2:
            canvas.delete(rect2)
        rect1 = canvas.create_rectangle(160, 450-value1, 210 , 470, fill="red")
        rect2 = canvas.create_rectangle(100, 450-value2, 150, 470, fill="blue")
        master.after(50, animate)

    animate()

root = tk.Tk()
rectangle_animation(root)
root.mainloop()