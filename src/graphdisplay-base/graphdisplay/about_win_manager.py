import tkinter as tk
import turtle
import webbrowser
from .general_config import *

class AboutWindow(tk.Toplevel):
    def __init__(self, root, graphgui):
        super().__init__(root)
        self.__graphgui = graphgui
        self.title("About")
        self.geometry("400x430")
        self.resizable(False, False)
        self.configure(bg=self.__graphgui._FRAME_COLOR, width=400, height=430)

        buton = tk.Button(self, text="Contribute", bg=self.__graphgui._BUTTON_COLOR, command=self.__open_github, bd=0)
        buton.pack(side=tk.BOTTOM)

        self.canvas = tk.Canvas(self, width=400, height=400, bg=self.__graphgui._BACKGROUND_CANVAS_COLOR)
        self.canvas.pack()
        self.turtle = turtle.RawTurtle(self.canvas, visible=False)
        self.canvas.configure(bg=self.__graphgui._BACKGROUND_CANVAS_COLOR)
        self.turtle.speed(0)
        text = "GraphDisplay v"+VERSION
        self.canvas.create_text(0, -150, text=text, font=("Courier", 20),
                                fill=self.__graphgui._AUTHOR_NAME_COLOR)
        self.canvas.create_text(0, 147, text="An open source proyect made", font=("Courier", 13),
                                fill=self.__graphgui._AUTHOR_NAME_COLOR)
        self.canvas.create_text(0, 165, text="by and for students!", font=("Courier", 13),
                                fill=self.__graphgui._AUTHOR_NAME_COLOR)
        for i in range(92):
            if i % 2 == 0:
                self.turtle.penup()
            else:
                self.turtle.pendown()
                self.turtle.color(self.__graphgui._VERTEX_COLOR)
            self.turtle.forward(i+1+5)
            self.turtle.right(91)

    def __open_github(self):
        webbrowser.open("https://github.com/seniorbeto/graphdisplay")

    def __open_twitter(self):
        webbrowser.open("https://twitter.com/seniorbeto__")