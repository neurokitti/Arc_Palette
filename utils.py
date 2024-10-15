# Built-in libraries
import os, sys, platform
# General image related libraries
from PIL import Image, ImageTk, ImageDraw

# for cross-platform compatibility
def is_windows():
    return platform.system() == "Windows"

# Fixes issues with compiling into binaries
def resource_path(relative_path):
    # using different compilers for Windows/Mac
    if is_windows():
        # fix for nuitka (try the temp path first, before assuming absolute path)
        base_path = os.path.join(os.path.dirname(__file__), relative_path)
        if os.path.isfile(base_path):
            return base_path
        else:
            return os.path.join(os.path.abspath("."), relative_path)
    else:
        # fix for pyinstaller (creates a temp folder, path found in _MEIPASS)
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

def path_to_img(image_path,):
    
    image = Image.open(resource_path(image_path))
    
    return image

def path_to_tk(image_path, size):
    
    image = Image.open(resource_path(image_path))
    
    return img_to_tk(image,size)

def img_to_tk(image,size):
    width, height = size
    display_img = image.resize((width, height))
    tk_image = ImageTk.PhotoImage(display_img)
    return tk_image