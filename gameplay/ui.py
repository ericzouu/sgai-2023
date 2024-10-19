import math
import tkinter as tk
from ui_elements.button_menu import ButtonMenu
from ui_elements.capacity_meter import CapacityMeter
from ui_elements.digital_clock import DigitalClock
from endpoints.machine_interface import MachineInterface
from ui_elements.restart_menu import RestartMenu
from ui_elements.game_viewer import GameViewer
#from ui_elements.machine_menu import MachineMenu
from os.path import join
from tkinter import messagebox
from ui_elements.button_menu import ButtonMenu
from random import choice
import random
from threading import Thread
from time import sleep
from ui_elements.start import StartMenu
from ui_elements.survey_menu import SurveyMenu
import os
class UI(object):
    def __init__(self, data_parser, scorekeeper, data_fp, is_disable, is_poor=False):
        # Set background color
        global bg_color # variable accessed by other files
        #r,g,b = (150, 150, 155)
        #bg_color = f'#{r:02x}{g:02x}{b:02x}'
        bg_color = 'dark gray'
        # Create a new window so that it doesn't interfere with the game
        # base window setup
        w, h = 1280, 800
        # main root window
        self.root=tk.Tk()
        self.root.withdraw() # hide it initially
        # start menu setup
        start_menu = tk.Toplevel(background="white")
        start_menu.title("Start Menu")
        # Delete the window after the click of a button
        global status
        status = True
        # Position the start window in the center
        def centerWindow(width, height, root):  
            screen_width = root.winfo_screenwidth()  # width of  screen
            screen_height = root.winfo_screenheight() # height of  screen     
            x = (screen_width/2) - (width/2)
            y = (screen_height/2) - (height/2)
            return int(x), int(y)
        x, y = centerWindow(1280, 800, self.root)
        start_menu.geometry(f"{w}x{h}+{x}+{y}")
        start_menu.resizable(False, False)
        # title
        start_menu.title("Beaverworks SGAI 2023 - Start Menu")
        # main loop for the start window
        def start():
            global status
            status = False
        # start button
        start_button = ("Start", lambda: start())
        self.start= StartMenu(start_menu, start_button)
        counter = 0
        # On closing of the start window so that it doesnt run over
        def on_closing():
            os._exit(0)
        # Delete window protocol
        start_menu.protocol("WM_DELETE_WINDOW", lambda: on_closing())
        while status:
            start_menu.update()
            counter += 1
            # Time out to save system resources
            if counter>1000000000:
                self.root.destroy()
        # Destroy start window
        start_menu.destroy()
        # Configure root
        self.root.deiconify()
        self.root.title("Beaverworks SGAI 2023 - Dead or Alive")
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(background=bg_color)

        # machine learning models
        mdl = random.choice(["poor_net.pth", "full_net.pth"])
        model_path = join("models", mdl)
        # gets first image
        self.humanoid = data_parser.get_random(scorekeeper)

        img_file = random.choice(["person", "robot"])
        if not is_disable:
            self.machine_interface = MachineInterface(self.root, w, h, model_file=model_path, img_file=img_file)
        scorekeeper.img_name = img_file
        scorekeeper.model = mdl

        #  Add buttons and logo
        user_buttons = [("Skip", lambda: self.skip_button(scorekeeper, data_fp, data_parser)),
                        ("Squish", lambda: self.squish_button(scorekeeper, data_fp, data_parser)),
                        ("Save", lambda: self.save_button(scorekeeper, data_fp, data_parser)),
                        ("Scram", lambda: self.scram_button(scorekeeper, data_fp, data_parser)),
                        ("Suggest", lambda: self.suggest_button(scorekeeper))]
        self.button_menu = ButtonMenu(self.root, user_buttons)
        # restart button
        restart_button = ("Restart", lambda: RestartMenu.restart())
        self.restart = RestartMenu(self.root, restart_button)
        #survey =[("Accurate", lambda: [(scorekeeper.record_accuracy(), self.disable_button(scorekeeper) )]), ("Inaccurate", lambda: [scorekeeper.inaccurate() , self.disable_button(scorekeeper)])]
        survey = [("1", lambda: [(scorekeeper.record_accuracy(1), self.disable_button(scorekeeper))]),
                  ("2", lambda: [(scorekeeper.record_accuracy(2), self.disable_button(scorekeeper))]),
                  ("3", lambda: [(scorekeeper.record_accuracy(3), self.disable_button(scorekeeper))]),
                  ("4", lambda: [(scorekeeper.record_accuracy(4), self.disable_button(scorekeeper))]),
                  ("5", lambda: [(scorekeeper.record_accuracy(5), self.disable_button(scorekeeper))])]
        self.survey= SurveyMenu(self.root, survey)
        
        # Display central photo
        self.game_viewer = GameViewer(self.root, w, h, data_fp, self.humanoid)
        self.root.bind("<Delete>", self.game_viewer.delete_photo)    

        # digital clock setup
        init_h = (24- (math.floor(scorekeeper.remaining_time / 60.0)))
        init_m = 60 - (scorekeeper.remaining_time % 60)
        self.clock = DigitalClock(self.root, w, h, init_h, init_m)
        # Create thread to make the time decrement
        time = Thread(target=scorekeeper.clock_tick, args=(self,))
        time.setDaemon(True) # prevent error after exiting the game
        time.start()
        # Display ambulance capacity
        self.capacity_meter = CapacityMeter(self.root, w, h, data_parser.capacity)

        # keybinds
        self.root.bind("q", lambda event: self.skip_button(scorekeeper, data_fp, data_parser))
        self.root.bind("w", lambda event: self.squish_button(scorekeeper, data_fp, data_parser))
        self.root.bind("e", lambda event: self.save_button(scorekeeper, data_fp, data_parser))
        self.root.bind("r", lambda event: self.scram_button(scorekeeper, data_fp, data_parser))
        self.root.bind("<space>", lambda event: self.suggest_button(scorekeeper))
        #places notif
        self.notif = tk.Label(self.root, text="", font=("Helvetica", 15), bg=bg_color)
        self.notif.place(x=(0.25 * 1280), y=50)

        # obstructions
        num_blood = random.randint(0, 3)
        self.game_viewer.display_blood(num_blood,  scorekeeper.remaining_time)
        self.game_viewer.display_wipers(0)

        # main loop
        self.root.mainloop()
    
    def disable_button(self, scorekeeper):
        self.survey.disable(scorekeeper.is_disabled)
    def update_ui(self, scorekeeper):
        """"
        update the text for the digital clock
        """
        h = (24 - (math.floor(scorekeeper.remaining_time / 60.0)))
        m = 60 - (scorekeeper.remaining_time % 60)
        self.clock.update_time(h, m)
        self.capacity_meter.update_fill(scorekeeper.get_current_capacity())
    def on_resize(self, event):
        w, h = 0.6 * self.root.winfo_width(), 0.7 * self.root.winfo_height()
        self.game_viewer.canvas.config(width=w, height=h)

    def get_next(self, data_fp, data_parser, scorekeeper):
        remaining = len(data_parser.unvisited)

        # Ran out of humanoids? Disable skip/save/squish
        if remaining == 0 or scorekeeper.remaining_time <= 0:
            self.capacity_meter.update_fill(0)
            self.game_viewer.delete_photo(None)
            self.game_viewer.display_score(scorekeeper.get_score())
            tk.Label(self.root, text="Don't reveal any aspect about this game to another player!", font=("Helvetica", 15),
                    bg=bg_color, highlightthickness=0).place(x=600, y=440, anchor='center')
            tk.Label(self.root, text="How would you rate the AI out of 5?", font=("Helvetica", 20),
                    bg=bg_color, highlightthickness=0).place(x=600, y=480, anchor='center')
            tk.Label(self.root, text="THIS IS MANDATORY! Please click on an option below:", font=("Helvetica", 15, 'bold'),
                    bg=bg_color, highlightthickness=0, foreground="red").place(x=600, y=520, anchor='center')
            self.button_menu.delete_buttons()
        else:
            humanoid = data_parser.get_random(scorekeeper)
            # Update visual display
            self.humanoid = humanoid
            fp = join(data_fp, self.humanoid.fp)
            self.game_viewer.create_photo(fp)

        # Disable button(s) if options are no longer possible
        self.button_menu.disable_buttons(scorekeeper.remaining_time, remaining, scorekeeper.at_capacity())

    def zombie_notif(self, killed):
        if killed == 1:
            notif_text = 'A zombie in your ambulance killed 1 person upon returning to the hospital.'
        else:
            notif_text = f'A zombie in your ambulance killed {killed} people upon returning to the hospital.'
        self.notif.config(text=notif_text)

    def clear_zombie_notif(self):
        self.notif.config(text="")

    def skip_button(self, scorekeeper, data_fp, data_parser, event=None):
        if str(self.button_menu.buttons[0]['state']) == 'disabled':
            return 0
        scorekeeper.skip(self.humanoid)
        self.update_ui(scorekeeper)
        ButtonMenu.error_skip(scorekeeper.remaining_time, scorekeeper.at_capacity())
        self.get_next(data_fp, data_parser, scorekeeper)
        self.game_viewer.display_blood(random.randint(0, 3), scorekeeper.remaining_time)
       # self.game_viewer.display_wipers(),
        self.machine_interface.reset_suggestion()


    def squish_button(self, scorekeeper, data_fp, data_parser):
        if str(self.button_menu.buttons[1]['state']) == 'disabled':
            return 0
        scorekeeper.squish(self.humanoid)
        self.update_ui(scorekeeper)
        ButtonMenu.error_squish(scorekeeper.remaining_time, scorekeeper.at_capacity())
        self.get_next(data_fp, data_parser, scorekeeper)
        self.game_viewer.display_blood(random.randint(0, 3), scorekeeper.remaining_time)
        #self.game_viewer.display_wipers()
        self.machine_interface.reset_suggestion()
        return 0

    def save_button(self, scorekeeper, data_fp, data_parser):
        if str(self.button_menu.buttons[2]['state']) == 'disabled':
            return 0
        scorekeeper.save(self.humanoid)
        self.update_ui(scorekeeper)
        ButtonMenu.error_save(scorekeeper.remaining_time, scorekeeper.at_capacity())
        #self.game_viewer.display_wipers()
        self.get_next(data_fp, data_parser, scorekeeper)
        self.game_viewer.display_blood(random.randint(0, 3), scorekeeper.remaining_time)
        #self.game_viewer.display_wipers()
        self.machine_interface.reset_suggestion()
        return 0

    def scram_button(self, scorekeeper, data_fp, data_parser):
        if str(self.button_menu.buttons[3]['state']) == 'disabled':
            return 0
        self.clear_zombie_notif()
        scorekeeper.scram(self)
        self.update_ui(scorekeeper)
        self.get_next(data_fp, data_parser, scorekeeper)
        self.game_viewer.display_blood(random.randint(0, 3), scorekeeper.remaining_time)
        #self.game_viewer.display_wipers()
        self.machine_interface.reset_suggestion()
        return 0

    def suggest_button(self, scorekeeper):
        self.machine_interface.suggest(self.humanoid)
        scorekeeper.suggested(self.machine_interface.suggest(self.humanoid))