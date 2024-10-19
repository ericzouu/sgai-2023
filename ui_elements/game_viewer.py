import math
import tkinter as tk
import random
from os.path import join
from PIL import ImageTk, Image
import os


class GameViewer(object):
    def __init__(self, root, w, h, data_fp, humanoid):
        self.canvas = tk.Canvas(root, width=math.floor(0.5 * w), height=math.floor(0.75 * h), highlightthickness=5)
        self.canvas.place(x=280, y=90)
        self.canvas.update()
        self.blood_tk_img=[]
        self.photo = None
        self.create_photo(join(data_fp, humanoid.fp))
        # background color
        from gameplay.ui import bg_color
        self.canvas.configure(background=bg_color)

    def delete_photo(self, event=None):
        self.canvas.delete('photo')
        self.canvas.delete('blood')
        for i in self.blood_tk_img:
            self.canvas.delete(i)

    def create_photo(self, fp):
        self.canvas.delete('photo')
        self.photo = display_photo(fp, self.canvas.winfo_width(), self.canvas.winfo_height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo, tags='photo')
    
    def display_blood(self, num_blood, remaining_time):
        # Delay the display of blood if the canvas is not yet created
        count=0
        if not self.canvas.winfo_exists():
            self.canvas.after(100, lambda: self.display_blood(num_blood))
            count+=100
            return
        #self.display_wipers(count)

        # Remove previous zombie images
        for i in self.blood_tk_img:
            self.canvas.delete(i)
        self.blood_tk_img=[]
        # Load the blood image
        blood_img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'blood.png') 
        blood_img = Image.open(blood_img_path)
        if remaining_time>0:
            for _ in range(num_blood):
                # Calculate random positions for the blood
                x = random.randint(0, self.canvas.winfo_width() - blood_img.width)
                y = random.randint(0, self.canvas.winfo_height() - blood_img.height)
                # Calculate a random rotation angle for the blood (in degrees)
                rotation_angle = random.randint(0, 360)
                # Rotate the blood image by the calculated angle
                rotated_blood_img = blood_img.rotate(rotation_angle)

                # Display the rotated blood on the canvas
                self.blood_tk_img.append(ImageTk.PhotoImage(rotated_blood_img))
                self.canvas.create_image(x, y, image=self.blood_tk_img[-1], anchor=tk.NW, tags='blood')
                self.canvas.image = self.blood_tk_img[-1]  # Keep a reference to prevent garbage collection
                self.canvas.tag_raise('blood')  # Bring the blood to the front
                self.canvas.tag_raise('wiper')

    def display_wipers(self, time):
        #self.canvas.delete('wiper')
        # Load the wiper images
        wiper_image_path1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'wiper.png')
        wiper_image_path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'wiper2.png')
        wiper_img1 = Image.open(wiper_image_path1)
        wiper_img2 = Image.open(wiper_image_path2)
        
        # Resize the wiper images to fit within the canvas
        wiper_img1 = wiper_img1.resize((self.canvas.winfo_width()-50, self.canvas.winfo_height()-200), Image.LANCZOS)
        wiper_img2 = wiper_img2.resize((self.canvas.winfo_width()-50, self.canvas.winfo_height()-200), Image.LANCZOS)
        
        # Create PhotoImage objects from the resized wiper images
        self.wiper_tk_img1 = ImageTk.PhotoImage(wiper_img1)
        self.wiper_tk_img2 = ImageTk.PhotoImage(wiper_img2)
        
        # Create a canvas image for the first wiper
        self.wiper_canvas_item = self.canvas.create_image(20, 231, image=self.wiper_tk_img1, anchor=tk.NW, tags='wiper')
        
        # Keep references to the wiper images to prevent garbage collection
        self.canvas.image = self.wiper_tk_img1
        self.canvas.image = self.wiper_tk_img2
        
        # Schedule the swapping of wiper images
        self.current_wiper_image = 1  # Start with the first wiper image
        self.canvas.after(time, self.swap_wiper_images)


    def swap_wiper_images(self):
        # Check which wiper image is currently displayed
        if self.current_wiper_image == 1:
            # If the first wiper image is displayed, swap to the second one
            self.canvas.itemconfig(self.wiper_canvas_item, image=self.wiper_tk_img2)
            self.current_wiper_image = 2
        else:
            # If the second wiper image is displayed, swap to the first one
            self.canvas.itemconfig(self.wiper_canvas_item, image=self.wiper_tk_img1)
            self.current_wiper_image = 1
        
        # Schedule the next swap after 0.5 seconds (500 milliseconds)
        self.canvas.after(500, self.swap_wiper_images)

    def display_score(self, score):
        from gameplay.ui import bg_color
        self.canvas.configure(highlightthickness=0)
        tk.Label(self.canvas, text="FINAL SCORE", font=("Helvetica", 30, "bold"), background=bg_color).pack(anchor=tk.NW)
        #tk.Label(self.canvas, text="Killed {}".format(score["killed"]), font=("Arial", 15)).pack(anchor=tk.NW)
        #tk.Label(self.canvas, text="Saved {}".format(score["saved"]), font=("Arial", 15)).pack(anchor=tk.NW)
        # feel free to adjust the weights
        tk.Label(self.canvas, text="Score {}".format(score["saved"]*15-score["killed"]*5),
                font=("Helvetica", 20), background=bg_color).pack(anchor=tk.NW)
        tk.Label(self.canvas, text="Total Suggestions {}".format(score["suggested"]),
                font=("Helvetica", 20), background=bg_color).pack(anchor=tk.NW)
        tk.Label(self.canvas,
                text="Suggestions Taken {}".format(score["suggestions taken"]),
                font=("Helvetica", 20), background=bg_color).pack(anchor=tk.NW)

def display_photo(img_path, w, h):
    img = Image.open(img_path).convert("RGBA")
    left = (img.width-img.height)/2
    right = img.width-left
    upper = 0
    lower = img.height
    img2 = img.crop([ left, upper, right, lower])
    resized = img2.resize((w, h), Image.LANCZOS)
    tk_img= ImageTk.PhotoImage(resized)
    return tk_img