import os
import json
import tkinter as tk
from tkinter import messagebox
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

        try:
            with open(self.__JSON_SAVE_DIR + '../win_config.json', "r", encoding="utf-8", newline="") as file:
                self._config = json.load(file)
        except FileNotFoundError:
            self._config = {
                'node_radius': DEFAULT_NODE_RADIUS,
                'theme': DEFAULT_THEME
            }
            self.update_main_config()

    def update_main_config(self):
        with open(self.__JSON_SAVE_DIR + '../win_config.json', "w", encoding="utf-8", newline="") as file:
            json.dump(self._config, file, indent=4)

    def update_permanent(self):
        with open(self.__JSON_SAVE_DIR + '../permanent.json', "w", encoding="utf-8", newline="") as file:
            json.dump(self.__permanent, file, indent=4)

    def delete_permanent(self, name: str):
        del self.__permanent[name]
        os.remove(self.__JSON_SAVE_DIR + name + '.json')
        self.update_permanent()

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

    def generate_delete_window(self):
        DeleteWindow(self.__parent, self)

    def generate_config_window(self):
        ConfigWindow(self.__parent, self)

class ConfigWindow(tk.Toplevel):
    def __init__(self, root, json_manager: JsonManager):
        super().__init__(root)
        self.title("Config")
        self.resizable(False, False)
        self.__manager = json_manager
        self.configure(background=self.__manager.graphgui._FRAME_COLOR)

        # Node configuration frame
        self.__node_frame = tk.Frame(self, bg=self.__manager.graphgui._BACKGROUND_CANVAS_COLOR, width=320, height=40)
        self.__node_frame.pack(padx=7, pady=7, expand=True)

        # Theme configuration frame
        self.__theme_frame = tk.Frame(self, bg=self.__manager.graphgui._BACKGROUND_CANVAS_COLOR, width=320, height=40)
        self.__theme_frame.pack(padx=7, pady=7, expand=True)

        # Node radius label
        text_label = tk.Label(self.__node_frame,
                              text="Node radius:",
                              bg=self.__manager.graphgui._BACKGROUND_CANVAS_COLOR,
                              font=("Courier", 13))
        text_label.place(x=5, y=7)

        # Node radius Scale widget
        self.__node_scale = tk.Scale(self.__node_frame,
                                     from_=10,
                                     to=100,
                                     orient=tk.HORIZONTAL,
                                     bg=self.__manager.graphgui._BACKGROUND_CANVAS_COLOR,
                                     troughcolor=self.__manager.graphgui._FRAME_COLOR,
                                     highlightthickness=0,
                                     length=150,
                                     sliderlength=20)
        self.__node_scale.set(self.__manager._config['node_radius'])
        self.__node_scale.place(x=150, y=0)

        # Theme label
        text_label = tk.Label(self.__theme_frame,
                                text="Theme:",
                                bg=self.__manager.graphgui._BACKGROUND_CANVAS_COLOR,
                                font=("Courier", 13))
        text_label.place(x=5, y=7)

         # Theme Selection widget
        self.__theme_selection = tk.StringVar(self)
        self.__theme_selection.set(self.__manager._config['theme'])
        self.__theme_option_menu = tk.OptionMenu(self.__theme_frame, self.__theme_selection, *THEMES)
        self.__theme_option_menu.config(bg=self.__manager.graphgui._BUTTON_COLOR, bd=0, highlightthickness=0)
        self.__theme_option_menu.place(x=150, y=9)

        # Button frame
        self.__button_frame = tk.Frame(self, bg=self.__manager.graphgui._BACKGROUND_CANVAS_COLOR, width=320, height=40)
        self.__button_frame.pack(padx=7, pady=7, expand=True)

        # Apply button
        self.__apply_button = tk.Button(self.__button_frame,
                                        text="Apply",
                                        bg=self.__manager.graphgui._BUTTON_COLOR,
                                        bd=0,
                                        command=self.__apply__settings)
        self.__apply_button.place(width=BUTTON_WIDTH,
                                  height=BUTTON_HEIGHT,
                                  x=160 - BUTTON_WIDTH / 2,
                                  y=7)


    def __apply__settings(self):
        new_node_radius = self.__node_scale.get()
        new_theme = self.__theme_selection.get()
        self.__manager._config['node_radius'] = new_node_radius
        self.__manager._config['theme'] = new_theme
        self.__manager.update_main_config()

        # Change the GUI theme
        self.__manager.graphgui._theme = new_theme
        self.__manager.graphgui.set_colors(new_theme)

        # Change the node radius
        self.__manager.graphgui.set_node_radius(new_node_radius)

        # Update the GUI
        current_position = self.__manager.graphgui.get_current_position()
        self.__manager.graphgui.display_reset(current_position)


class DeleteWindow(tk.Toplevel):
    def __init__(self, root, json_manager: JsonManager):
        super().__init__(root)
        self.title("Delete save")
        self.geometry("200x100")
        self.resizable(False, False)
        self.__manager = json_manager
        self.configure(background=self.__manager.graphgui._BACKGROUND_CANVAS_COLOR)

        self.__label = tk.Label(self, text="Select save:", bg=self.__manager.graphgui._BACKGROUND_CANVAS_COLOR)
        self.__label.pack(side=tk.TOP)

        options = list(self.__manager._JsonManager__permanent.keys())
        if len(options) > 0:
            self.__selecion = tk.StringVar(self)
            self.__selecion.set(options[0])
            self.__option_menu = tk.OptionMenu(self, self.__selecion, *options)
            self.__option_menu.config(bg=self.__manager.graphgui._BUTTON_COLOR)
            self.__option_menu.pack(side=tk.TOP)

            self.__button = tk.Button(self, text="Delete", command=self.__on_delete, bg=self.__manager.graphgui._BUTTON_COLOR)
            self.__button.place(x=0+7, y=100-7-30, width=60, height=30)

            self.__button2 = tk.Button(self, text="Cancel", command=self.__on_cancel, bg=self.__manager.graphgui._BUTTON_COLOR)
            self.__button2.place(x=200-7-60, y=100-7-30, width=60, height=30)

    def __on_delete(self):
        selection = self.__selecion.get()
        if selection not in self.__manager._JsonManager__permanent:
            messagebox.showerror("Error", "The selected save does not exist")
            self.destroy()
        self.__manager.delete_permanent(selection)
        messagebox.showinfo("Confirm", f"Removed : {selection}")

    def __on_cancel(self):
        self.destroy()

class LoadWindow(tk.Toplevel):
    def __init__(self, root, json_manager: JsonManager):
        super().__init__(root)
        self.title("Load")
        self.geometry("200x100")
        self.resizable(False, False)
        self.__manager = json_manager
        self.configure(background=self.__manager.graphgui._BACKGROUND_CANVAS_COLOR)

        self.__label = tk.Label(self, text="Select save:", bg=self.__manager.graphgui._BACKGROUND_CANVAS_COLOR)
        self.__label.pack(side=tk.TOP)

        options = list(self.__manager._JsonManager__permanent.keys())
        if len(options) > 0:
            self.__selecion = tk.StringVar(self)
            self.__selecion.set(options[0])
            self.__option_menu = tk.OptionMenu(self, self.__selecion, *options)
            self.__option_menu.config(bg=self.__manager.graphgui._BUTTON_COLOR)
            self.__option_menu.pack(side=tk.TOP)

            self.__button = tk.Button(self, text="Load", command=self.__on_load, bg=self.__manager.graphgui._BUTTON_COLOR)
            self.__button.place(x=0+7, y=100-7-30, width=60, height=30)

            self.__button2 = tk.Button(self, text="Cancel", command=self.__on_cancel, bg=self.__manager.graphgui._BUTTON_COLOR)
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
        self.__current_position = graph_position
        self.__manager = json_manager
        self.configure(bg=self.__manager.graphgui._BACKGROUND_CANVAS_COLOR)
        self.__root = root
        self.bind("<Return>", self.__on_save)

        self.__label = tk.Label(self, text="Save as:", bg=self.__manager.graphgui._BACKGROUND_CANVAS_COLOR)
        self.__label.pack(side=tk.TOP)

        self.__entry = tk.Entry(self)
        self.__entry.pack(side=tk.TOP)

        self.__button = tk.Button(self, text="Save", command=self.__on_save, bg=self.__manager.graphgui._BUTTON_COLOR)
        self.__button.place(x=0+7, y=100-7-30, width=60, height=30)

        self.__button2 = tk.Button(self, text="Cancel", command=self.__on_cancel, bg=self.__manager.graphgui._BUTTON_COLOR)
        self.__button2.place(x=200-7-60, y=100-7-30, width=60, height=30)

    def __on_save(self, event = None):
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

if __name__ == "__main__":
    confirmation = input("WARNING: eliminating store. Do you want to proceed? [Y/N]: ")
    if confirmation == "Y":
        path = os.getcwd()

        if os.path.exists(os.path.join(path, "permanent.json")):
            os.remove(os.path.join(path, "permanent.json"))

        if os.path.exists(os.path.join(path, "win_config.json")):
            os.remove(os.path.join(path, "win_config.json"))

        store_path = os.path.join(path, "store/")

        for file in os.listdir(store_path):
            if file.endswith(".json"):
                removing = os.path.join(store_path, file)
                os.remove(removing)