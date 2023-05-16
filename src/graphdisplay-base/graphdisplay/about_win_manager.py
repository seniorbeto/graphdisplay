import tkinter as tk
import turtle
from .general_config import *

class AboutWindow(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("About")
        self.geometry("400x400")
        self.resizable(False, False)

