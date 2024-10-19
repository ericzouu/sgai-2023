import tkinter as tk
import os
from PIL import ImageTk, Image
class StartMenu(object):
    def __init__(self, start_menu, start_button):
        # access the background color variable
        from gameplay.ui import bg_color
        #self.canvas = tk.Canvas(start_menu, width=math.floor(1280), height=math.floor(800), background=bg_color)
        #self.canvas.place(relx=0.5, rely=0.5, anchor="center")
        self.canvas = tk.Canvas(start_menu, width=1280, height=800, background=bg_color)
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")
        self.start_status=True
        # Create start button
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'buttons', 'start.png')
        image = ImageTk.PhotoImage(Image.open(path).resize((170, 65), Image.LANCZOS))
        action = start_button[1]
        start = tk.Button(self.canvas, image=image, command=action, borderwidth=0, highlightthickness=0, background=bg_color)
        start.image = image
        start.place(relx=0.5, rely=0.9, anchor="center")
        # Title
        game = "SGAI - Team Prime"
        # UI elements
        # Instructions
        tk.Label(self.canvas, text=game, font=("Helvetica", 25), background=bg_color).place(relx=0.5, y=50, anchor='center')
        tk.Label(self.canvas, text="How to Play", font=("Helvetica", 40, "bold"), background=bg_color).place(relx=0.5, y=100, anchor='center')
        text1 = "In the midst of the zombie apocalypse, your mission is to race through\nthe city in an ambulance, rescuing as many humans as you can!"
        tk.Label(self.canvas, text=text1, font=("Helvetica", 20), background=bg_color).place(relx=0.5, y=170, anchor='center')
        text2 = "Along the way, you will encounter the healthy, injured, corpses, and zombies.\nIt's your responsibility to identify each figure and make the right choice."
        tk.Label(self.canvas, text=text2, font=("Helvetica", 20), background=bg_color).place(relx=0.5, y=245, anchor='center')
        tk.Label(self.canvas, text="Your ambulance is equipped with an AI sensor that can help you with classification.",
                 font=("Helvetica", 15), foreground="dark red", background=bg_color).place(relx=0.5, y=295, anchor='center')
        text3 = "With only 24 hours on the clock, you must balance accuracy and speed.\nEvery decision you make will consume time!"
        tk.Label(self.canvas, text=text3, font=("Helvetica", 20), background=bg_color).place(relx=0.5, y=350, anchor='center')
        # AI accuracy info
        tk.Label(self.canvas, text="There are a few AI models being used in this game.",
                 font=("Helvetica", 20), background=bg_color).place(relx=0.5, y=620, anchor='center')
        tk.Label(self.canvas, text="You will be receiving the following model:",
                 font=("Helvetica", 20), background=bg_color).place(relx=0.45, y=660, anchor='center')
        tk.Label(self.canvas, text="Accurate", font=("Helvetica", 20, "bold"),
                 foreground="dark green", background=bg_color).place(relx=0.695, y=662, anchor='center')
        # Button images (non-clickable)
        buttons = ["skip", "squish", "save", "scram", "suggest"]
        info = [["-15 minutes", "Ignore and proceed", "*points lost when used\nagainst injured people"],
                ["-5 minutes", "Plow through", "*points lost when used\nagainst humans"],
                ["-30 minutes", "Bring into ambulance", "*zombies will kill\nhumans onboard"],
                ["-2 hours", "Drive to hospital", "*empties capacity\n"],
                ["Free", "Show hint from AI", "*may not be\nfully accurate"]]
        x_value = 0.15
        for button in buttons:
            # Display possible actions
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'buttons', f'{button}.png')
            image = ImageTk.PhotoImage(Image.open(path).resize((170, 65), Image.LANCZOS))
            action = tk.Label(self.canvas, image=image, background=bg_color)
            action.image = image
            action.place(relx=x_value, y=440, anchor='center')
            # Info under each action
            # Time cost
            if button == buttons[4]:
                tk.Label(self.canvas, text=info[buttons.index(button)][0], font=("Helvetica", 23),
                         foreground="dark green", background=bg_color).place(relx=x_value, y=490, anchor='center')
            else:
                tk.Label(self.canvas, text=info[buttons.index(button)][0], font=("Helvetica", 23),
                         foreground="dark red", background=bg_color).place(relx=x_value, y=490, anchor='center')
            # Description
            tk.Label(self.canvas, text=info[buttons.index(button)][1], font=("Helvetica", 18),
                     background=bg_color).place(relx=x_value, y=525, anchor='center')
            # Warning
            if info[buttons.index(button)][2] == "*empties capacity\n":
                tk.Label(self.canvas, text=info[buttons.index(button)][2], font=("Helvetica", 14),
                         foreground="dark green", background=bg_color).place(relx=x_value, y=565, anchor='center')
            else:
                tk.Label(self.canvas, text=info[buttons.index(button)][2], font=("Helvetica", 14),
                         foreground="dark red", background=bg_color).place(relx=x_value, y=565, anchor='center')               
            x_value += 0.175