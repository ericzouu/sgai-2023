import tkinter as tk
import os
import math
from datetime import timedelta
import pyglet
pyglet.options['win32_gdi_font'] = True
from sys import platform

class DigitalClock(object):
    def __init__(self, root, w, h, init_h, init_m):
        self.x = 150
        self.y = 150
        self.canvas = tk.Canvas(root, width=math.floor(0.2*w)+20, height=math.floor(0.3 * h), highlightthickness=0)
        self.canvas.place(x=math.floor(0.75 * w), y=50)

        # background color
        from gameplay.ui import bg_color
        self.canvas.configure(background=bg_color)

        self.text = ""
        self.time_desc = tk.Label(self.canvas, text="Remaining Time", font=("Helvetica", 25, "bold"), background=bg_color)
        self.time_desc.place(x=20, y=30)

        # digital font
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'digital-7.ttf')
        pyglet.font.add_file(path)

        # font only works on Windows
        if platform=="win32":
            self.timer = tk.Label(self.canvas, text=self.text, font=("digital-7", 75), background=bg_color, fg='dark red')
            self.timer.place(x=40, y=70)
        else:
            self.timer = tk.Label(self.canvas, text=self.text, font=("Helvetica", 50), background=bg_color, fg='dark red')
            self.timer.place(x=40, y=70)
        
        self.minutes = 25 * 60
        self.update_time(init_h, init_m)

    def update_time(self, h, m):
        self.minutes = 25*60 - h*60 - m
        self.text = str(timedelta(minutes=self.minutes))[:-3]
        if self.minutes >= 24*60:
            self.text = "24:00"
        if self.minutes < 0:
            self.text = "0:00"
        self.timer.config(text=self.text)
        return