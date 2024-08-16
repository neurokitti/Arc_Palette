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
import pywinstyles

def resource_path(relative_path):
    """ Fixes issues with PyInstaller """
    base_path = os.path.abspath(".")
    if '_MEIPASS2' in os.environ:
        # PyInstaller creates a temp folder, path found in _MEIPASS
        base_path = os.environ['_MEIPASS2']
    return os.path.join(base_path, relative_path)

def path_to_img(image_path, size):
    width, height = size
    image = Image.open(resource_path(image_path))
    display_img = image.resize((width, height))
    tk_image = ImageTk.PhotoImage(display_img)
    return tk_image
