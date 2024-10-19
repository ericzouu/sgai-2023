import tkinter as tk
import os
import sys
from PIL import ImageTk, Image

class RestartMenu(object):
    def __init__(self, root, restart_button):
        self.canvas = tk.Canvas(root, width=500, height=80, highlightthickness=0)
        self.canvas.place(x=530, y=350)
        # Create restart button
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'buttons', 'restart.png')
        image_file = Image.open(path)
        image = ImageTk.PhotoImage(image_file)
        from gameplay.ui import bg_color
        action = restart_button[1]
        button = tk.Button(self.canvas, image=image, command=action, borderwidth=0, highlightthickness=0, background=bg_color)
        button.image = image
        create_menu(button)
        # background color
        from gameplay.ui import bg_color
        self.canvas.configure(background=bg_color)
    def restart():
        #code to destroy window and restart the game
        python = sys.executable
        os.execl(python, python, * sys.argv)

def create_menu(button):
    button.pack(side=tk.BOTTOM)