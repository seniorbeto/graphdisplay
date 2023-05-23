import tkinter as tk

class ToolWindow(tk.Toplevel):
    def __init__(self, root, graph):
        super().__init__(root)
        self.geometry("500x500")
        self.resizable(False, False)
        self.__graph = graph
        self.configure(background=self.__graph._BACKGROUND_CANVAS_COLOR)

        if not self.__graph._is_tree:
            ...