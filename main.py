import ttkbootstrap as tb
from ttkbootstrap import Style
from ttkbootstrap.widgets import Meter
import tkinter as tk
import math
from PIL import Image, ImageTk, ImageDraw
import ctypes # ignor this one im gonna remove it 
import os
from threading import Thread
import random
from tkinter import ttk
from Arc_API.Arc_API import arc_API
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
        
        display_img = Image.open("resources\dot_pad.png") # add an arg later
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
    def create_smooth_radial_gradient(self,):
        width, height = self.gradient_size
        color_positions = []
        for id, cirlce in enumerate(self.circles):
            if id < len(self.gradient_points):
                color_positions.append((self.gradient_points[id], cirlce['rgb']))
            else:
                color_positions.append(((random.randint(0, width),random.randint(0, height)), cirlce['rgb']))
        image = Image.new('RGB', self.gradient_size, (255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        for x in range(width):
            for y in range(height):
                weights = []
                weight_sum = 0
                
                for pos, color in color_positions:
                    dist = math.sqrt((x - pos[0])**2 + (y - pos[1])**2)
                    weight = 1 / (dist + 1)**2  # Adding 1 to avoid division by zero
                    weights.append((weight, color))
                    weight_sum += weight
                
                r, g, b = 0, 0, 0
                for weight, color in weights:
                    normalized_weight = weight / weight_sum
                    r += color[0] * normalized_weight
                    g += color[1] * normalized_weight
                    b += color[2] * normalized_weight
                
                draw.point((x, y), (int(r), int(g), int(b)))
        image.save('resources\gradient_wallpaper.png')
        self.set_wallpaper('resources\gradient_wallpaper.png')
        return image
    def set_wallpaper(self,image_path):
        # Convert the path to an absolute path
        image_path = os.path.abspath(image_path)
        
        # Check if the file exists
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"No such file: '{image_path}'")
        
        # Use the Windows API to set the wallpaper
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
    def set_theme(self,):
        print(self.tab)
        colors = []
        print(auto_launch_var.get())
        if auto_launch_var.get() == 1:
            arc_api.close_arc()
            print('WHAAAAAT')
            arc_api.kill_arc()
        for id, cirlce in enumerate(self.circles):
            if id < len(self.gradient_points):
                colors.append((cirlce['rgb'][0],cirlce['rgb'][1],cirlce['rgb'][2],1))
        self.arc_api.set_space_theme_color(self.tab,"blendedGradient",colors,"light",intensityFactor=0.7)
        if auto_launch_var.get() == 1:
            arc_api.open_arc()
        print('ACUALRJALSDK ASLDASDADASDASD')



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

    global tab_count
    canvas_h = 320
    canvas_w = 320
    tab = ttk.Frame(notebook)
    notebook.add(tab, text=f"space {tab_count + 1}")
    
    # Add some content to the new tab
    color_pick_frame = tk.Frame(tab)
    color_pick_frame.pack(side="top")
    color_pick = color_picker(color_pick_frame, (canvas_w, canvas_h), arc_api, tab=tab_count)
    button_frame = tk.Frame(tab)
    button_frame.pack(side="top")
    minus_button = ImageButton(button_frame, r"resources\minus_button.png", color_pick.remove_color)
    minus_button.pack(pady=10,padx=5,side="left")
    
    theme_button = ImageButton(button_frame, r"resources/wallpaper_set.png", color_pick.set_theme)
    theme_button.pack(pady=10,padx=5,side="left",)
    plus_button = ImageButton(button_frame, r"resources\plus_button.png", color_pick.add_color)
    plus_button.pack(pady=10,padx=5,side="right")
    tab_count += 1

if __name__ == "__main__":

    tab_count = 0
    root = tk.Tk()
    arc_api = arc_API()
    spaces_num = arc_api.get_number_of_spaces()
    checkbox_var = tk.IntVar()
    
    root.iconbitmap('resources\icon.ico')
    root.title('Arc Palette')
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)
    for i in range(spaces_num):
        add_tab(arc_api)
    auto_launch_var = tk.IntVar()
    auto_restart_button = tk.Checkbutton(text="Auto restart",variable=auto_launch_var,)
    auto_restart_button.pack()
    #update_spaces_count()
    root.mainloop()
