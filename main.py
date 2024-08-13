import ttkbootstrap as tb
from ttkbootstrap import Style
from ttkbootstrap.widgets import Meter
import tkinter as tk
import sv_ttk
import math
from PIL import Image, ImageTk, ImageDraw
import os
from threading import Thread
import random
from tkinter import ttk
from Arc_API.Arc_API import arc_API
import customtkinter as ctk

def resource_path(relative_path):
    """ Fixes issues with PyInstaller """
    try:
        # PyInstaller creates a temp folder, path found in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class color_picker:
    def __init__(self,canvas_frame, size,arc_api, max_colors=10, tab=0):
        self.tab = tab
        self.width, self.height = size
        self.canvas = tk.Canvas(canvas_frame, width=self.width, height=self.height, )
        self.arc_api = arc_api
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        self.circles = []
        self.img = self.generate_color_picker_canvas()
        
        display_img = Image.open(resource_path("resources/img/dot_pad.png")) # add an arg later
        self.display_img = display_img.resize((self.width, self.height))
        self.display_img_tk = ImageTk.PhotoImage(self.display_img)
        self.canvas.create_image(2, 2, image=self.display_img_tk, anchor='nw')
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        self.selected_size = 13
        self.unselected_size = 10

        self.current_circle = None
        self.max_colors = max_colors
        gradient_heigth = 400
        gradient_width = 400
        self.gradient_size = (gradient_width,gradient_heigth)
        self.gradient_points = [(0,0),(0,gradient_heigth),(gradient_width,gradient_heigth//2),(0,gradient_heigth//2),(gradient_width//2,gradient_heigth//2)]
        self.mode = "light"
        self.alpha = 0.7
        self.intensity =1
    def on_canvas_click(self,event):
        x = min(max(event.x, 0), self.width)
        y = min(max(event.y, 0), self.height)
        
        rgb = self.get_rgb_at_coordinate(x, y)
        for circle in self.circles:
                if self.is_within_circle(event.x, event.y, circle):
                    self.current_circle = circle
                    break
                else:
                    self.current_circle = None
        if self.current_circle == None:
            self.add_color(x=x,y=y)
        if self.current_circle and self.current_circle['id'] is not None:
            self.canvas.delete(self.current_circle['id'])

        if self.current_circle:
            self.current_circle['id'] = self.canvas.create_oval(
                x - self.selected_size, y - self.selected_size,
                x + self.selected_size, y + self.selected_size,
                fill=self.rgb_to_hex(rgb), outline='white', width=3
            )
            self.current_circle['x'] = x
            self.current_circle['y'] = y
            self.current_circle['rgb'] = rgb
        
    def on_canvas_drag(self, event):
        if self.current_circle is None:
            return
        x = max(0, min(event.x, self.width))
        y = max(0, min(event.y, self.height))
        rgb = self.get_rgb_at_coordinate(x, y)
        self.canvas.coords(
            self.current_circle['id'], x - self.selected_size, y - self.selected_size,
            x + self.selected_size, y + self.selected_size
        )
        self.canvas.itemconfig(self.current_circle['id'], fill=self.rgb_to_hex(rgb))
        self.current_circle['x'] = x
        self.current_circle['y'] = y
        self.current_circle['rgb'] = rgb
        #self.canvas.delete(self.circles[0]['id'])
    def on_canvas_release(self, event):
        if self.current_circle is not None:
            self.canvas.delete(self.current_circle['id'])
            self.current_circle['id'] = self.canvas.create_oval(
                self.current_circle['x'] - self.unselected_size, self.current_circle['y'] - self.unselected_size,
                self.current_circle['x'] + self.unselected_size, self.current_circle['y'] + self.unselected_size,
                fill=self.rgb_to_hex(self.current_circle['rgb']), outline='white', width=2
            )
            self.current_circle = None  # Reset current circle after releasing
    def is_within_circle(self, x, y, circle):
        return (circle['x'] - self.unselected_size <= x <= circle['x'] + self.unselected_size and
                circle['y'] - self.unselected_size <= y <= circle['y'] + self.unselected_size)

    def generate_color_picker_canvas(self):
        img = Image.new("RGBA", (self.width,self.height))
        draw = ImageDraw.Draw(img)
        for y in range(self.height):
            for x in range(self.width):
                r = int((x / self.width) * 255)
                g = int((y / self.height) * 255)
                b = 255 - int(((x / self.width) + (y / self.height)) / 2 * 255)
                draw.point((x, y), (r, g, b, 255))
        return img
    def get_compliment_pos(self,x,y):
        if len(self.circles) == 1:
            mirrored_x = 2 * self.center_x - x
            mirrored_y = 2 * self.center_y - y
            return mirrored_x, mirrored_y
    def get_rgb_at_coordinate(self, x, y):
        x = min(max(x, 0), self.width - 1)
        y = min(max(y, 0), self.height - 1)
        image = self.img
        image = image.convert('RGB')
        rgb = image.getpixel((x, y))
        return rgb
    
    def add_color(self,x=None, y=None):
        if len(self.circles) < self.max_colors:
            x = x if x is not None else self.center_x
            y = y if y is not None else self.center_y
            rgb = self.get_rgb_at_coordinate(x,y)
            new_circle = self.canvas.create_oval(
                    x - self.unselected_size, y - self.unselected_size,
                    x + self.unselected_size, y + self.unselected_size,
                    fill=self.rgb_to_hex(rgb), outline='white', width=3
                )
            self.circles.append({'id': new_circle, 'x': x, 'y': y, 'rgb': rgb})
    def remove_color(self,):
        if self.circles:
            last_circle = self.circles.pop()  # Remove and get the last added circle
            self.canvas.delete(last_circle['id'])  # Delete the circle from the canvas
    def rgb_to_hex(self, rgb):
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
    def create_smooth_radial_gradient_thread(self,):
        thread = Thread(target=self.create_smooth_radial_gradient)
        thread.start()
    def set_theme(self,):
        print(self.tab)
        colors = []
        if var.get() == 1:
            arc_api.close_arc()
            arc_api.kill_arc()
        for id, cirlce in enumerate(self.circles):
            if id < len(self.gradient_points):
                colors.append((cirlce['rgb'][0],cirlce['rgb'][1],cirlce['rgb'][2],self.alpha))
        print(len(colors))
        if len(colors) < 2:
            print("single color")
            print(colors)
            self.arc_api.set_space_theme_color(self.tab,"blendedSingleColor",colors,self.mode,intensityFactor=self.intensity)
        else:
            self.arc_api.set_space_theme_color(self.tab,"blendedGradient",colors,self.mode,intensityFactor=self.intensity)
        if var.get() == 1:
            arc_api.open_arc()
    def set_mode(self,mode):
        self.mode = mode
    def set_alpha(self,alpha):
        self.alpha = float(alpha/100)
        print(float(alpha/100))
    def set_intensity(self,intensity):
        self.intensity = float(intensity/100)
        print(float(intensity/100))


class ImageButton:
    def __init__(self, button_frame, img_path, command_function, size=(20,20)):
        self.button_frame = button_frame
        self.button_display_img = Image.open(img_path)
        self.button_display_img = self.button_display_img.resize(size, Image.LANCZOS)
        self.button_imgtk = ImageTk.PhotoImage(self.button_display_img)
        self.button = tk.Button(button_frame, image=self.button_imgtk,borderwidth=0, command=command_function)
        self.button.image = self.button_imgtk  # Keep a reference to the image
        self.button.config(image=self.button_imgtk, highlightthickness=0, pady=0, padx=0)
    def pack(self, **kwargs):
        self.button.pack(**kwargs)

def add_tab(arc_api):
    def slider_set_alpha(value):
        color_pick.set_alpha(value)
    def slider_set_intensity(value):
        color_pick.set_intensity(value)
    global tab_count
    canvas_h = 320
    canvas_w = 320
    
    tab = ttk.Frame(notebook)
    notebook.add(tab, text=f"Space {tab_count + 1}")


    # Add some content to the new tab
    color_pick_frame = tk.Frame(tab,)
    color_pick_frame.pack(side="top")
    color_pick = color_picker(color_pick_frame, (canvas_w, canvas_h), arc_api, tab=tab_count)
    button_frame = ttk.Frame(tab,)
    button_frame.pack(side="top")
    button_frame2 = ttk.Frame(button_frame,)
    button_frame2.pack(side="left")
    minus_button = ImageButton(button_frame2, resource_path("resources/img/minus_button.png"), color_pick.remove_color)
    minus_button.pack(pady=5,padx=5,side="left")
    slider_frame = ttk.Frame(button_frame,)
    slider_frame.pack(side="right")
    theme_button = ImageButton(button_frame2, resource_path("resources/img/set_theme_button.png"), color_pick.set_theme)
    theme_button.pack(pady=5,padx=5,side="left",)
    plus_button = ImageButton(button_frame2, resource_path("resources/img/plus_button.png"), color_pick.add_color)
    plus_button.pack(pady=5,padx=5,side="left")


    slider_alpha_frame = ttk.Frame(button_frame,)
    slider_alpha_frame.pack(side="top")
    alpha_label = ttk.Label(slider_alpha_frame,text="Opacity")
    alpha_label.pack(pady=5,padx=5,side="left")
    slider = ctk.CTkSlider(master=slider_alpha_frame, from_=0, to=100, command=slider_set_alpha)
    slider.pack(pady=5,padx=5,side="right")

    slider_transparency_frame = ttk.Frame(button_frame,)
    slider_transparency_frame.pack(side="bottom")
    transparency_label = ttk.Label(slider_transparency_frame,text="Intensity")
    transparency_label.pack(pady=5,padx=5,side="left")
    slider2 = ctk.CTkSlider(master=slider_transparency_frame, from_=0, to=100, command=slider_set_intensity)
    slider2.pack(pady=5,padx=5,side="right")


    
    tab_count += 1

"""def update_spaces_count():
    global tab_count, spaces_num, notebook
    arc_api = arc_API()
    new_spaces_num = arc_api.get_number_of_spaces()
    print(spaces_num,new_spaces_num)
    if new_spaces_num > spaces_num:
        for i in range(new_spaces_num - spaces_num):
            add_tab(arc_api)
    if new_spaces_num < spaces_num:
        print("NEED TO DELEAST")


    spaces_num = new_spaces_num
    
    root.after(100, update_spaces_count)"""

if __name__ == "__main__":
    global tab_count, spaces_num, notebook
    tab_count = 0
    root = tk.Tk()
    arc_api = arc_API()
    spaces_num = arc_api.get_number_of_spaces()
    var = tk.IntVar()
    root.iconbitmap(resource_path("resources/img/icon.ico"))
    root.title('Arc Palette')
    root.geometry("340x450")
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)
    for i in range(spaces_num):
        add_tab(arc_api)
    check_box = ttk.Checkbutton(root, text="Auto Restart Arc",var=var)
    check_box.pack()
    #update_spaces_count()
    sv_ttk.set_theme("light")
    root.mainloop()
