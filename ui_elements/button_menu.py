import tkinter as tk
import os
from PIL import ImageTk, Image
from gameplay.enums import ActionCost
from tkinter import messagebox
suggest_canvas = None

class ButtonMenu(object):
    def __init__(self, root, items):
        self.canvas = tk.Canvas(root, width=500, height=80, highlightthickness=0)
        self.canvas.place(x=75, y=200)
        suggest_canvas = tk.Canvas(root, width=50, height=30, highlightthickness=0)
        suggest_canvas.place(x=540, y=720)
        self.buttons = create_buttons(self.canvas, items)
        create_menu(self.buttons)

        # background color
        from gameplay.ui import bg_color
        self.canvas.configure(background=bg_color)
        suggest_canvas.configure(bg=bg_color)

    def disable_buttons(self, remaining_time, remaining_humanoids, at_capacity, is_disable=False):
        if not at_capacity:
            for i in range(0, len(self.buttons)):
                self.buttons[i].config(state="normal")
        if remaining_humanoids == 0 or remaining_time <= 0:
            for i in range(0, len(self.buttons)):
                self.buttons[i].config(state="disabled")
        #  Not enough time left? Disable action
        if (remaining_time - ActionCost.SCRAM.value) < ActionCost.SKIP.value:
            self.buttons[0].config(state="disabled")
        if (remaining_time - ActionCost.SCRAM.value) < ActionCost.SQUISH.value:
            self.buttons[1].config(state="disabled")
        if (remaining_time - ActionCost.SCRAM.value) < ActionCost.SAVE.value:
            self.buttons[2].config(state="disabled")
        if at_capacity:
            self.buttons[0].config(state="disabled")
            self.buttons[1].config(state="disabled")
            self.buttons[2].config(state="disabled")

    def error_skip(remaining_time, at_capacity):
        if (remaining_time - ActionCost.SCRAM.value) < ActionCost.SKIP.value:
            messagebox.showwarning('Warning', "Not enough time to skip, skip button is disabled")
    def error_squish(remaining_time, at_capacity):
        if (remaining_time - ActionCost.SCRAM.value) < ActionCost.SQUISH.value:
            messagebox.showwarning('Warning', "Not enough time to squish, squish button is disabled")
    def error_save(remaining_time, at_capacity):
        if at_capacity:
            messagebox.showwarning('','Capacity Full, cannot carry any more people')
    def delete_buttons(self):
        for i in range(0, len(self.buttons)):
            self.buttons[i].pack_forget()

def create_buttons(canvas, items):
    buttons = []
    for item in items:
        (text, action) = item
        current_canvas = None
        # suggest button goes on a different canvas
        if text.lower() == "suggest":
            current_canvas = suggest_canvas
        else:
            current_canvas = canvas
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'buttons', f'{text.lower()}.png')
        image_file = Image.open(path)
        image = ImageTk.PhotoImage(image_file)
        # access the background color variable
        from gameplay.ui import bg_color
        button = tk.Button(current_canvas, image=image, command=action,  borderwidth=0, highlightthickness=0, background=bg_color)
        button.image = image
        buttons.append(button)
    return buttons


def create_menu(buttons):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'logo.png')
    logo = ImageTk.PhotoImage(Image.open(path).resize((300, 50), Image.LANCZOS))
    label = tk.Label(image=logo, highlightthickness=0)
    label.image = logo
    # Position image
    label.place(x=10, y=10)

    i = 1
    for button in buttons:
        # check if it's the suggest button
        if i <= 4:
            button.pack(side=tk.TOP, pady=10)
            i += 1
        else:
            button.pack(side=tk.BOTTOM, padx=10)
            button.place(x=530, y=710)