import os
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from .general_config import *

class JsonManager:
    def __init__(self, parent, graphgui):
        self.__JSON_SAVE_DIR = os.path.join(os.path.dirname(__file__), 'store/')

        self.graphgui = graphgui
        self.__parent = parent
        self.current_data_id = None
        self.current_data = None

        try:
            with open(self.__JSON_SAVE_DIR + '../permanent.json', "r", encoding="utf-8", newline="") as file:
                self.__permanent = json.load(file)
        except FileNotFoundError:
            self.__permanent = {}

    def update_permanent(self):
        with open(self.__JSON_SAVE_DIR + '../permanent.json', "w", encoding="utf-8", newline="") as file:
            json.dump(self.__permanent, file, indent=4)

    def add_permanent(self, name: str):
        self.__permanent[name] = str(datetime.now())
        self.update_permanent()

    def get_data(self, file_name: str) -> dict:
        try:
            with open(self.__JSON_SAVE_DIR + file_name + '.json', "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = None
        self.current_data_id = file_name
        self.current_data = data
        return data

    def save_data(self, file_name: str, data: dict):
        with open(self.__JSON_SAVE_DIR + file_name + '.json', "w", encoding="utf-8", newline="") as file:
            json.dump(data, file, indent=4)

    def generate_save_window(self, current_position: dict):
        SaveWindow(self.__parent, self, current_position)

    def generate_load_window(self):
        LoadWindow(self.__parent, self)


class LoadWindow(tk.Toplevel):
    def __init__(self, root, json_manager: JsonManager):
        super().__init__(root)
        self.title("Load")
        self.geometry("200x100")
        self.resizable(False, False)
        self.configure(background=BACKGROUND_CANVAS_COLOR)
        self.__manager = json_manager

        self.__label = tk.Label(self, text="Select save:", bg=BACKGROUND_CANVAS_COLOR)
        self.__label.pack(side=tk.TOP)

        options = list(self.__manager._JsonManager__permanent.keys())
        if len(options) > 0:
            self.__selecion = tk.StringVar(self)
            self.__selecion.set(options[0])
            self.__option_menu = tk.OptionMenu(self, self.__selecion, *options)
            self.__option_menu.config(bg=BUTTON_COLOR)
            self.__option_menu.pack(side=tk.TOP)

            self.__button = tk.Button(self, text="Load", command=self.__on_load, bg=BUTTON_COLOR)
            self.__button.place(x=0+7, y=100-7-30, width=60, height=30)

            self.__button2 = tk.Button(self, text="Cancel", command=self.__on_cancel, bg=BUTTON_COLOR)
            self.__button2.place(x=200-7-60, y=100-7-30, width=60, height=30)

    def __on_load(self):
        selection = self.__selecion.get()
        if selection not in self.__manager._JsonManager__permanent:
            messagebox.showerror("Error", "The selected save does not exist")
            self.destroy()
        self.new_position = self.__manager.get_data(selection)
        self.__manager.graphgui.display_reset(self.new_position)

    def __on_cancel(self):
        self.destroy()

class SaveWindow(tk.Toplevel):
    def __init__(self, root, json_manager: JsonManager, graph_position: dict):
        super().__init__(root)
        self.title("Save")
        self.geometry("200x100")
        self.resizable(False, False)
        self.configure(bg=BACKGROUND_CANVAS_COLOR)
        self.__current_position = graph_position
        self.__manager = json_manager
        self.__root = root

        self.__label = tk.Label(self, text="Save as:", bg=BACKGROUND_CANVAS_COLOR)
        self.__label.pack(side=tk.TOP)

        self.__entry = tk.Entry(self)
        self.__entry.pack(side=tk.TOP)

        self.__button = tk.Button(self, text="Save", command=self.__on_save, bg=BUTTON_COLOR)
        self.__button.place(x=0+7, y=100-7-30, width=60, height=30)

        self.__button2 = tk.Button(self, text="Cancel", command=self.__on_cancel, bg=BUTTON_COLOR)
        self.__button2.place(x=200-7-60, y=100-7-30, width=60, height=30)

    def __on_save(self):
        word = self.__entry.get()
        word = word.strip()
        word = word.replace(" ", "_")
        if word:
            self.__manager.save_data(word, self.__current_position)
            self.__manager.add_permanent(word)
            messagebox.showinfo("Confirmación", f"Guardado : {word}")
        else:
            messagebox.showerror("Error", "You must enter a name")
        self.destroy()

    def __on_cancel(self):
        self.destroy()