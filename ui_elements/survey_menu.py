import tkinter as tk
import os
import sys
from PIL import ImageTk, Image
import math
class SurveyMenu(object):
    def __init__(self, root, item):
        from gameplay.ui import bg_color
        self.canvas = tk.Canvas(root,width=0,height=0)
        self.canvas.place(x=300, y=90)
        self.canvas = tk.Canvas(root, width=500, height=80)
        self.canvas.configure(borderwidth=0, bd=0, highlightthickness=0, relief='ridge', background=bg_color)
        self.canvas.place(x=405, y=542.5)
        self.start_status=True
        self.buttons = create_buttons(self.canvas, item)
        #create buttons
        create_menu(self.buttons)
    def disable(self, isdisable):
        if isdisable:
            for button in self.buttons:
                button.config(state="disabled")
        #end menu messages
def create_buttons(canvas, items):
    buttons=[]
    for item in items:
        from gameplay.ui import bg_color
        (text, action) = item
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'buttons', f'{text.lower()}.png')
        image_file = Image.open(path)
        image = ImageTk.PhotoImage(image_file)
        button = tk.Button(canvas, image=image, command=action, borderwidth=0, highlightthickness=0, background=bg_color)
        button.image = image
        buttons.append(button)
    return buttons

def create_menu(buttons):
    for button in buttons:
        button.pack(side=tk.LEFT, padx=10)
