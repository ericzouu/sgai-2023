import math
import tkinter as tk
from PIL import ImageTk, Image
import os


class CapacityMeter(object):
    def __init__(self, root, w, h, max_cap):
        self.canvas = tk.Canvas(root, width=310, height=325, highlightthickness=0)
        self.canvas.place(x=math.floor(0.75 * w), y=math.floor(0.4 * h)-100)
        # units setup
        self.__units = []
        self.unit_size = 35
        self.canvas.update()
        self.render(max_cap, self.unit_size, root)
        # background color
        from gameplay.ui import bg_color
        self.canvas.configure(background=bg_color)

    def render(self, max_cap, size, root):
        self.canvas.create_text(135, 40, text="Capacity", font="Helvetica 30 bold")
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'ambulance.png')
        logo = ImageTk.PhotoImage(Image.open(path).resize((310, 240), Image.LANCZOS)) # default size (299, 185)
        root.logo = logo
        self.canvas.create_image(155, 200, image=logo)
        # Create the squares in the ambulance
        x = 3
        y = 95
        for i in range(0, max_cap):
            unit = create_unit(self.canvas, x+20, y, size)
            self.__units.append(unit)
            x += size * 1.5
            if (x + size * 1.5*3) > self.canvas.winfo_width():
                x = 3
                y += size * 1.5

    def update_fill(self, index):
        if index != 0:
            self.canvas.itemconfig(self.__units[index-1], stipple="gray50")
        else:
            for unit in self.__units:
                self.canvas.itemconfig(unit, stipple="")


def create_unit(canvas, x, y, size):
    from gameplay.ui import bg_color
    return canvas.create_rectangle(x, y, x+size, y+size, fill=bg_color, stipple="")