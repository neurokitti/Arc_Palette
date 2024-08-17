# Built-in libraries
import os, sys
# General image related libraries
from PIL import Image, ImageTk, ImageDraw


# Fixes issues with compiling into binaries
def resource_path(relative_path):
    isWindows = os.name == "nt"
    # using different compilers for Windows/Mac
    if isWindows:
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

def path_to_img(image_path, size):
    width, height = size
    image = Image.open(resource_path(image_path))
    display_img = image.resize((width, height))
    tk_image = ImageTk.PhotoImage(display_img)
    return tk_image
