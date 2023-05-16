import tkinter as tk
import turtle
from time import sleep
from .general_config import *

class AboutWindow(tk.Toplevel):
    def __init__(self, root, graphgui):
        super().__init__(root)
        self.__graphgui = graphgui
        self.title("About")
        self.geometry("400x400")
        self.resizable(False, False)

        self.canvas = tk.Canvas(self, width=400, height=400, bg=self.__graphgui._BACKGROUND_CANVAS_COLOR)
        self.canvas.pack()
        self.turtle = turtle.RawTurtle(self.canvas, visible=False)
        self.canvas.configure(bg=self.__graphgui._BACKGROUND_CANVAS_COLOR)
        self.turtle.speed(0)
        text = self.canvas.create_text(0, -150, text="GraphDisplay", font=("Courier", 20),
                                fill=self.__graphgui._AUTHOR_NAME_COLOR)
        for i in range(92):
            if i % 2 == 0:
                self.turtle.penup()
            else:
                self.turtle.pendown()
                self.turtle.color(self.__graphgui._VERTEX_COLOR)
            self.turtle.forward(i+1+5)
            self.turtle.right(91)


#        self.canvas.configure(bg=self.__graphgui._BACKGROUND_CANVAS_COLOR)