# Built-in libraries
import os, sys, math, random
from threading import Thread
from typing import Union
# General system related libraries
import darkdetect
# General image related libraries
from PIL import Image, ImageTk, ImageDraw
# General GUI related libraries
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap import Style
from ttkbootstrap.widgets import Meter
import sv_ttk
# Conditional GUI related libraries (based on OS)
try:
    # Windows only
    import pywinstyles
except ImportError: # MacOS can only have non-blurry transparency at this time
    pass
# Additional libraries from local PY files
from Arc_API.Arc_API import arc_API
import utils




class color_picker(tk.Canvas):
    def __init__(self, parent, dot_pad_path, colour_image_path, display_image_path, size, arc_api, max_colors=10, tab=0, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Arguments
        self.tab = tab
        self.arc_api = arc_api
        self.max_colors = max_colors

        # Sizing
        self.width, self.height = size
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        min_dimension = min(self.width, self.height)

        # Set circle sizes proportional to the canvas size
        self.selected_size = int(min_dimension * 0.038)  # 5% of the smaller dimension
        self.unselected_size = int(min_dimension * 0.031)
        self.border_width_selected_size = int((min_dimension*0.039) / 3.4)
        self.border_width_unselected_size = int((min_dimension*0.039) / 3.5)

        # Circle Info
        self.circles = []
        self.current_circle = None
        self.circle_outline_color = "grey11" if theme == "dark" else "grey98"
                                   # The colors above match transparency of background, (due to the colors used by the `sv_ttk` light/dark themes not meshing
                                   # with `pywinstyles` acrylic). Those specific colors used are the background colors for `sv_ttk`'s light/dark themes.
                                   #
                                   # Another thing to mention, due to how acrylic works in Windows, black becomes the color to be full translucent blur, while
                                   # white (or full value of a color in terms of HSV) becomes the color to be fully opaque (no transluceny). This is also why
                                   # I had to do some funky things to the `dot_pad.png` pictures for both to work with acrylic.
                                   #
                                   # By setting `color_pick_tab_frame` and `notebook` to have different alpha values, by default it will still use black
                                   # as the color to turn translucent blur.
                                   # What we should be doing instead is just setting the alpha level on just the `notebook`, and remove the alpha level from
                                   # `color_pick_tab_frame`.
                                   # Then, see my further comments below around `color_pick` in the program for other steps that would need to be taken.
                                   #
                                   # NOTE: Arylic doesn't technically have a dark/light theme, it's just translucency. Dark/light only affects the blending onto
                                   #       the translucent area.
                                   #
                                   #       We need to correctly make 2 color schemes for acrylic to work right, e.g. for "dark mode" from a range of black (full
                                   #       translucent blur) to white (no transluceny) colors in the UI. This also means we'll need another `dot_pad.png` for
                                   #       both acrylic theme options so they both play well with the restrictions mentioned with how Windows treats colors when
                                   #       using acrylic for UI. Additionally, we would then want to make sure to adjust the colors above to change appropriately
                                   #       for light/dark/acrylic (but the colors for light and dark have already been figured out above, so it's just a matter
                                   #       of fiddling with a color for acrylic, which requires creating a custom color scheme to use with `pywinstyles`).
                                   #
                                   #       When it comes to selecting a theme for the app, it should show System, Light, and Dark. Then, there should be a toggle
                                   #       for turning on/off Arylic.
                                   #
                                   #       What we might want to do for the Acrylic theme, is implement a translucency slider (like how Windows Terminal does it),
                                   #       but that might take more work to do, depending on how I need to alter the current `sv_ttk` theme to be compatible
                                   #       with acrylic in both light/dark mode.
                                   #
                                   #       - Drew

        # Default Settings
        self.mode = "light"
        self.alpha = 0.7
        self.intensity = 1
        self.display_image_var = tk.BooleanVar(value=False)
        self.dotpad_img = utils.path_to_tk(dot_pad_path, (self.width, self.height))
        self.colour_img = utils.path_to_img(colour_image_path)
        self.display_img= utils.path_to_tk(display_image_path, (self.width, self.height))
        
        self.set_display_image()
        
        
        self.config(width=self.width, height=self.height, bg=None, highlightthickness=0)

        # Color Picker Detection
        self.bind("<Button-1>", self.on_canvas_click)
        self.bind("<B1-Motion>", self.on_canvas_drag)
        self.bind("<ButtonRelease-1>", self.on_canvas_release)
    

    def set_display_image(self,):
        if self.display_image_var.get() == True:
            
            self.display_image = self.display_img
        else:
            self.display_image = self.dotpad_img
            
        
        self.create_image(0, 0, anchor=tk.NW, image=self.display_image)
        self.redraw_circles()

    def redraw_circles(self):
        
        for circle in self.circles:
            self.current_circle = circle
            self.delete(self.current_circle["id"])
            self.current_circle["id"] = self.spawn_circle((self.current_circle["x"], self.current_circle["y"]),
                                                          self.current_circle["rgb"], self.unselected_size, self.border_width_unselected_size)
            self.current_circle = None
            
    def get_point_data(self, limit, pos, get_rgb=True): # ensures that an 'x' and 'y' point are within the range of the canvas
        pos_x, pos_y = pos
        rgb = None
        x = min(max(limit.x, 0), pos_x)
        y = min(max(limit.y, 0), pos_y)

        if get_rgb == True:
            rgb = self.get_rgb_at_coordinate(x, y)

        return (x, y, rgb)

    def spawn_circle(self, pos, rgb, size, border_size):
        x, y = pos
        circle_id = self.create_oval(
            x - size, y - size,
            x + size, y + size,
            fill=self.rgb_to_hex(rgb), outline=self.circle_outline_color, width=border_size)
        return circle_id

    def update_circle_data(self, x, y, rgb):
        self.current_circle["x"] = x
        self.current_circle["y"] = y
        self.current_circle["rgb"] = rgb

    def on_canvas_click(self, event):
        self.current_circle = None
        x, y, rgb = self.get_point_data(event, (self.width, self.height))

        for circle in self.circles:
            if self.is_within_circle(event.x, event.y, circle):
                self.current_circle = circle
                break

        if self.current_circle != None:
            self.delete(self.current_circle["id"])
            self.current_circle["id"] = self.spawn_circle((x, y), rgb, self.selected_size, self.border_width_selected_size)
            self.update_circle_data(x, y, rgb)

        else:
            self.add_color(x=x, y=y)

    def on_canvas_drag(self, event):
        if self.current_circle is not None:
            x, y, rgb = self.get_point_data(event, (self.width, self.height))

            self.coords(
                self.current_circle["id"], x - self.selected_size, y - self.selected_size,
                x + self.selected_size, y + self.selected_size)

            self.itemconfig(self.current_circle["id"], fill=self.rgb_to_hex(rgb))
            self.update_circle_data(x, y, rgb)

    def on_canvas_release(self, event):
        if self.current_circle is not None:
            self.delete(self.current_circle["id"])
            self.current_circle["id"] = self.spawn_circle((self.current_circle["x"], self.current_circle["y"]),
                                                          self.current_circle["rgb"], self.unselected_size, self.border_width_unselected_size)
            self.current_circle = None

    def is_within_circle(self, x, y, circle, mod=2):
        leftProduct = circle["x"] - (self.unselected_size + mod) <= x <= circle["x"] + (self.unselected_size + mod)
        rightProduct = circle["y"] - (self.unselected_size + mod) <= y <= circle["y"] + (self.unselected_size + mod)
        return (leftProduct and rightProduct)

    def get_rgb_at_coordinate(self, x, y):
        x = min(max(x, 0), self.width - 1)
        y = min(max(y, 0), self.height - 1)
        image = self.colour_img
        resized_img = image.resize((self.width,self.height))

        resized_img = resized_img.convert("RGB")
        rgb = resized_img.getpixel((x, y))
        return rgb

    def add_color(self, x=None, y=None):
        if len(self.circles) < self.max_colors:
            x = x if x is not None else self.center_x
            y = y if y is not None else self.center_y
            rgb = self.get_rgb_at_coordinate(x, y)
            new_circle = self.spawn_circle((x, y), rgb, self.unselected_size, self.border_width_unselected_size)
            self.circles.append({"id": new_circle, "x": x, "y": y, "rgb": rgb})

    def remove_color(self):
        if self.circles:
            last_circle = self.circles.pop()
            self.delete(last_circle["id"])

    def rgb_to_hex(self, rgb):
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    def create_smooth_radial_gradient_thread(self):
        thread = Thread(target=self.create_smooth_radial_gradient)
        thread.start()

    def set_theme(self):
        colors = []
        if self.arc_api.auto_restart_arc == True:
            self.arc_api.close_arc()
            self.arc_api.kill_arc()
        for id, circle in enumerate(self.circles):
            colors.append((circle["rgb"][0], circle["rgb"][1], circle["rgb"][2], self.alpha))
        print(len(colors))
        if len(colors) < 1:
            print("windows theme color")
            print(colors)
            self.arc_api.set_space_theme_color(self.tab, "none", colors, self.mode, intensityFactor=self.intensity)
        elif len(colors) < 2:
            print("single color")
            print(colors)
            self.arc_api.set_space_theme_color(self.tab, "blendedSingleColor", colors, self.mode, intensityFactor=self.intensity)
        else:
            self.arc_api.set_space_theme_color(self.tab, "blendedGradient", colors, self.mode, intensityFactor=self.intensity)
        if self.arc_api.auto_restart_arc == True:
            self.arc_api.open_arc()

    def set_alpha(self, alpha):
        self.alpha = float(alpha / 100)
        print(float(alpha / 100))

    def set_intensity(self, intensity):
        self.intensity = float(intensity / 100)
        print(float(intensity / 100))




class TransparentCanvas(tk.Canvas):
    # NOTE: Images inside of the canvas should already respect transparency (relative to the background color/image set in the canvas).
    #       to make a certain color inside the canvas be transparent, need to use pywinstyles: `pywinstyles.set_opacity(widget_id, color="white")`
    #       - Drew
    # TODO: ... I have some ideas - Drew
    def __init__(self, parent, image_path, *args, **kwargs):
        # Initialize the Canvas with parent and other options
        super().__init__(parent, *args, **kwargs)

        # Load the image with transparency
        self.image = Image.open(utils.resource_path(image_path))
        self.image_with_transparency = ImageTk.PhotoImage(self.image)

        # Set the canvas size to the image size
        self.config(width=self.image.width, height=self.image.height, bg=None, highlightthickness=0)

        # Add the image to the canvas
        self.create_image(0, 0, anchor=tk.NW, image=self.image_with_transparency)




class ImageButton:
    def __init__(self, button_frame, img_path, command_function, size=(20, 20)):
        self.button_frame = button_frame
        self.button_display_img = Image.open(utils.resource_path(img_path))
        self.button_display_img = self.button_display_img.resize(size, Image.LANCZOS)
        self.button_imgtk = ImageTk.PhotoImage(self.button_display_img)
        self.button = ttk.Button(button_frame, image=self.button_imgtk, command=command_function)
        self.button.image = self.button_imgtk  # Keep a reference to the image
        self.button.config(image=self.button_imgtk)

    def pack(self, **kwargs):
        self.button.pack(**kwargs)




class tab_bar(ttk.Notebook):
    def __init__(self, parent, tabs, tab_class, arc_api, window_color_mode,show_space_name=True,show_space_number=False, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.show_space_name = show_space_name
        self.show_space_number = show_space_number
        self.window_color_mode = window_color_mode
        self.tabs_count = 0
        self.canvas_h, self.canvas_w = (335, 335)
        self.arc_api = arc_api
        self.parent = parent
        # BooleanVar to track the checkbox state
        self.auto_restart_var = tk.BooleanVar(value=self.arc_api.auto_restart_arc)

        for i in range(tabs):
            tab_instance = tab_class(self, self.arc_api)
            space_icon = ""
            if self.arc_api.get_space_icon(i) != None:
                space_icon = self.arc_api.get_space_icon(i)[0]
            else:
                space_icon = "·"
            self.add(tab_instance, text=space_icon)

            if self.arc_api.get_space_name(i) != None:
                space_name = self.arc_api.get_space_name(i)
            else:
                space_name = f"Space {i+1}"
            
            
            if show_space_name == False:
                self.add(tab_instance, text=f"{space_icon}")
            else:
                if show_space_number == True:
                    self.add(tab_instance, text=f"{space_icon} {f'Space {i+1}'}")
                    # Used to be self.add(tab_instance, text=f"{space_icon} {f"Space {i+1}"}")
                    # Looked into the main.py file in VSCode and looked up the error when the 
                    # program wasn't working on my machine, using double quotes two times in
                    # a single F-String can be confusing to python apparently.
                    # - Raviable
                else:
                    self.add(tab_instance, text=f"{space_icon} {space_name}")
            
        self.bind('<<NotebookTabChanged>>', self.on_tab_change)

    def on_tab_change(self, event):
        tab = event.widget.tab('current')

    def set_auto_restart_arc(self):
        # Update the auto_restart_arc attribute in arc_api
        self.arc_api.set_auto_restart_arc(self.auto_restart_var.get())
    def get_window_width(self, ):
        width = self.parent.winfo_width()
        print(f"Window width: {width}")
        return width



class space_tab(ttk.Frame):
    def __init__(self, notebook, arc_api, *args, **kwargs):
        super().__init__(notebook, *args, **kwargs)

        def slider_set_alpha(value):
            color_pick.set_alpha(float(value))

        def slider_set_intensity(value):
            print(value)
            color_pick.set_intensity(float(value))

        # Accessing canvas_h and canvas_w from the parent (tab_bar)
        self.canvas_h = notebook.canvas_h
        self.canvas_w = notebook.canvas_w
        self.window_color_mode = notebook.window_color_mode
        self.arc_api = arc_api
        color_pick_tab_frame = ttk.Frame(self, background=None)
        color_pick_tab_frame.pack(side="top", padx=10, pady=10, expand=True)

        color_pick_frame = ttk.Frame(color_pick_tab_frame, background=None)
        color_pick_frame.pack(side="top")
        # Pass canvas_h and canvas_w to color_picker
        color_pick = color_picker(color_pick_frame,
                                  f"res/img/{self.window_color_mode}/dot_pad.png",f"res/img/colorpicker_real.png",f"res/img/colorpicker_display.png", (self.canvas_w, self.canvas_h), self.arc_api, tab=notebook.tabs_count)
        color_pick.pack()

        colorPickTabFrameAlphaValue = 1 # All this setting does is set how transparent this widget is compared to its parent widget.
                                        #
                                        # Since one of the parent widgets is already set to have translucency (`notebook`) it affects all elements inside it,
                                        # including this one.
                                        #
                                        # That is why the color picker itself is still translucent.
                                        #
                                        # To rectify that, we would have to somehow separate the canvas from the `notebook` such that they are in the same
                                        # parent frame (in this case that would be in `Arc_Palette` as `self`), which means there's going to be complicated
                                        # work that needs to be done there with positioning correctly in the window, and getting buttons and such working
                                        # properly with the notebook.
                                        #
                                        # To keep the background of the canvas being translucent (the `dot_pad.png`), while keeping the foreground of it (the
                                        # circle color selections) opaque, we'd need to have the `dot_pad.png` displayed behind the canvas. Then, would need to
                                        # use a certain color for the background of the canvas for which `pywinstyles` can used to set that color to be
                                        # transparent (this color will have to change based on a future proposed dark/light, referring to the blackground
                                        # blending toggle in Arc, for the theme generating).
                                        #
                                        # For Arc's background blending mode, "light" has white as a pickable color while "dark" has black as a pickable color.
                                        # If we refer to "white" and "black" as the "no go color" for each blending mode, then we just have to make sure to set
                                        # the background of the canvas to the opposite "no go color" (e.g. background of the canvas while on "light" blending
                                        # mode would need to be black), and then make sure `pywinstyles` is set to use that background color as the one to make
                                        # transparent. Only problem with that though is now for sure the ring around the color circle will always have some form
                                        # of transparency, which is why I suggest that the ring around the circles (only when in the acrylic theme) to be just
                                        # HTML color "gray" (this is #808080, half way between white and black, so the transluceny effect on the canvas would be
                                        # the same on "dark" or "light" blending mode).
                                        #
                                        # - Drew
        if utils.is_windows():
            pywinstyles.set_opacity(color_pick_tab_frame, value=colorPickTabFrameAlphaValue)
        #else: # WIP for MacOS version - Drew
            #color_pick_tab_frame.attributes('-alpha', colorPickTabFrameAlphaValue)

        # frames
        controls_frame = ttk.Frame(color_pick_tab_frame)
        controls_frame.pack(side="top")
        options_frame = ttk.Frame(color_pick_tab_frame)
        options_frame.pack(side="bottom")
        button_frame = ttk.Frame(controls_frame)
        button_frame.pack(side="left")
        slider_frame = ttk.Frame(controls_frame)
        slider_frame.pack(side="right")

        # buttons
        minus_button = ImageButton(button_frame, f"res/img/{self.window_color_mode}/minus_button.png", color_pick.remove_color)
        minus_button.pack(pady=5, padx=5, side="left")

        theme_button = ImageButton(button_frame, f"res/img/{self.window_color_mode}/set_theme.png", color_pick.set_theme)
        theme_button.pack(pady=5, padx=5, side="left")

        plus_button = ImageButton(button_frame, f"res/img/{self.window_color_mode}/plus_button.png", color_pick.add_color)
        plus_button.pack(pady=5, padx=5, side="left")

        # sliders
        slider_alpha_frame = ttk.Frame(controls_frame)
        slider_alpha_frame.pack(side="top")
        alpha_label = ttk.Label(slider_alpha_frame, text="Opacity")
        alpha_label.pack(pady=5, padx=5, side="left")
        slider = ttk.Scale(slider_alpha_frame, from_=0, to=100, command=slider_set_alpha)
        slider.pack(pady=5, padx=5, side="right")

        slider_transparency_frame = ttk.Frame(controls_frame)
        slider_transparency_frame.pack(side="bottom")
        transparency_label = ttk.Label(slider_transparency_frame, text="Intensity")
        transparency_label.pack(pady=5, padx=5, side="left")
        slider2 = ttk.Scale(slider_transparency_frame, from_=0, to=100, command=slider_set_intensity)
        slider2.pack(pady=5, padx=5, side="right")

        # checkboxes (uses the notebox to store and update auto restart value)
        check_box = ttk.Checkbutton(options_frame, text="Auto Restart Arc",
                                    variable=notebook.auto_restart_var,
                                    command=notebook.set_auto_restart_arc)
        check_box_hide_dot_grid = ttk.Checkbutton(options_frame, text="Hide Dot Grid",
                                    variable=color_pick.display_image_var,
                                    command=color_pick.set_display_image)
        #check_box.pack(pady=(0, 10), side="bottom")
        check_box.pack(side="bottom")
        check_box_hide_dot_grid.pack(side="bottom")

        notebook.tabs_count += 1




class Arc_Palette(tk.Tk):
    def __init__(self, window_color_mode="light"):
        super().__init__()
        self.window_color_mode = window_color_mode
        self.iconbitmap(utils.resource_path("res/img/icon.ico" if utils.is_windows() else "res/img/icon.icns"))
        self.title("Arc Palette")

        # setting x dimensions any lower will result in canvas being cut off
        # changing the following also can affect things: size, padding, and borderwidth
        # with no border, this odd number aligns perfectly with the rest of the frames in view
        

        self.arc_api = arc_API()
        self.spaces_num = self.arc_api.get_number_of_spaces()
        self.tab_count = 0

        # Setup main GUI
        acrylicAlphaValue = 0.7

        notebook = tab_bar(self, self.spaces_num, space_tab, self.arc_api, self.window_color_mode, show_space_name=True, show_space_number=False)
        notebook.pack(side="top", fill="both", expand=True)

        # apply transparency
        if utils.is_windows():
            pywinstyles.set_opacity(notebook, value=acrylicAlphaValue)
        #else: # WIP for MacOS version - Drew
            #notebook.attributes('-alpha', notebookAlphaValue)

        self.apply_window_theme()

    def apply_window_theme(self):
        # set light/dark theme and give window transparency blur effects
        sv_ttk.set_theme(self.window_color_mode)

        if utils.is_windows():
            pywinstyles.apply_style(self, "acrylic")
        #else: # WIP for MacOS version - Drew
            #self.attributes('-alpha', 0.9)

    def monitor_system_theme(self):
        # automatically fix theme when system theme changes
        theme = (darkdetect.theme()).lower()
        if self.window_color_mode != theme:
            self.window_color_mode = theme
            self.apply_window_theme()
        self.after(100, self.monitor_system_theme)





if __name__ == "__main__":
    theme = (darkdetect.theme()).lower()
    
    arc_palette = Arc_Palette(theme)
    # TODO: many aspects of the UI needs ways to update configuration when system theme changes while
    #       app is in use, and some basic boilerplate code is in place, which changes the majority of
    #       the theme, except:
    #       - images loaded in for the buttons
    #       - the background image of the canvas
    #       - outlines of pre-existing circles on the canvas
    #arc_palette.monitor_system_theme()
    arc_palette.mainloop()
