import tkinter as tk
from .general_config import *
from .graphs import Graph

class ToolWindow(tk.Toplevel):
    def __init__(self, root, graph):
        super().__init__(root)
        self.geometry("500x500")
        self.resizable(False, False)
        self.__gui = graph
        self.configure(background=self.__gui._FRAME_COLOR)
        self.protocol("WM_DELETE_WINDOW", self.__on_closing)

        if not self.__gui._is_tree:
            self.__create_djistra_frame()
            self.__create_minimum_path_frame()

    def __reset_colors(self):
        for node in self.__gui.nodes:
            self.__gui.canvas.itemconfigure(node.circle, fill=self.__gui._VERTEX_COLOR)

    def __on_closing(self):
        self.__reset_colors()
        self.destroy()

    def __create_djistra_frame(self):
        self.__djistra_frame = tk.Frame(self, bg=self.__gui._BACKGROUND_CANVAS_COLOR,
                                        height=80,
                                        width=500)
        self.__djistra_frame.pack(padx=7, pady=7)

        # Djistra text
        text_label = tk.Label(self.__djistra_frame,
                              text="Djistra",
                              bg=self.__gui._BACKGROUND_CANVAS_COLOR,
                              font=("Courier", 13))
        text_label.place(x=5, y=35)

        # First node entry
        self.first_node_entry_djis = tk.Entry(self.__djistra_frame)
        self.first_node_entry_djis.place(height=BUTTON_HEIGHT,
                               width=BUTTON_WIDTH,
                               y=35,
                               x=170)
        first_entry_text = tk.Label(self.__djistra_frame,
                                    text="First Node",
                                    bg=self.__gui._BACKGROUND_CANVAS_COLOR,
                                    font=("Courier", 13))
        first_entry_text.place(x=150, y=10)

        # Second node entry
        self.second_node_entry_djis = tk.Entry(self.__djistra_frame)
        self.second_node_entry_djis.place(height=BUTTON_HEIGHT,
                               width=BUTTON_WIDTH,
                               y=35,
                               x=240 + BUTTON_WIDTH)
        first_entry_text = tk.Label(self.__djistra_frame,
                                    text="Second Node",
                                    bg=self.__gui._BACKGROUND_CANVAS_COLOR,
                                    font=("Courier", 13))
        first_entry_text.place(x=275, y=10)

        # Go button
        go_button = tk.Button(self.__djistra_frame,
                              text="Show Path",
                              command=self.__djistra_press,
                              bg=self.__gui._BUTTON_COLOR,
                              bd=0)
        go_button.place(x=390, y=35, height=BUTTON_HEIGHT, width=BUTTON_WIDTH + 30)

    def __djistra_press(self):
        self.__reset_colors()
        first_node = self.first_node_entry_djis.get()
        second_node = self.second_node_entry_djis.get()

        gui_graph: Graph = self.__gui._graph

        if first_node not in list(gui_graph._vertices.keys()):
            print("ERROR: first node not in graph's vertices")
            return
        elif  second_node not in list(gui_graph._vertices.keys()):
            print("ERROR: second node not in graph's vertices")
            return

        min_path = gui_graph.minimum_path(first_node, second_node)
        if len(min_path[0]) >= 2:
            for node in self.__gui.nodes:
                if node.id in min_path[0]:
                    if node.id == first_node or node.id == second_node:
                        self.__gui.canvas.itemconfigure(node.circle,
                                                        fill=self.__gui._AUTHOR_NAME_COLOR)
                    else:
                        self.__gui.canvas.itemconfigure(node.circle, fill=self.__gui._AUTHOR_NAME_COLOR)
        else:
            print("ERROR: there is no path from", first_node, "to", second_node)

    def __create_minimum_path_frame(self):
        self.__minimum_path_frame = tk.Frame(self, bg=self.__gui._BACKGROUND_CANVAS_COLOR,
                                        height=80,
                                        width=500)
        self.__minimum_path_frame.pack(padx=7, pady=7)

        # Djistra text
        text_label = tk.Label(self.__minimum_path_frame,
                              text="Minimum Path",
                              bg=self.__gui._BACKGROUND_CANVAS_COLOR,
                              font=("Courier", 13))
        text_label.place(x=5, y=35)

        # First node entry
        self.first_node_entry_min = tk.Entry(self.__minimum_path_frame)
        self.first_node_entry_min.place(height=BUTTON_HEIGHT,
                               width=BUTTON_WIDTH,
                               y=35,
                               x=170)
        first_entry_text = tk.Label(self.__minimum_path_frame,
                                    text="First Node",
                                    bg=self.__gui._BACKGROUND_CANVAS_COLOR,
                                    font=("Courier", 13))
        first_entry_text.place(x=150, y=10)

        # Second node entry
        self.second_node_entry_min = tk.Entry(self.__minimum_path_frame)
        self.second_node_entry_min.place(height=BUTTON_HEIGHT,
                               width=BUTTON_WIDTH,
                               y=35,
                               x=240 + BUTTON_WIDTH)
        first_entry_text = tk.Label(self.__minimum_path_frame,
                                    text="Second Node",
                                    bg=self.__gui._BACKGROUND_CANVAS_COLOR,
                                    font=("Courier", 13))
        first_entry_text.place(x=275, y=10)

        # Go button
        go_button = tk.Button(self.__minimum_path_frame,
                              text="Show Path",
                              command=self.__minpath_press,
                              bg=self.__gui._BUTTON_COLOR,
                              bd=0)
        go_button.place(x=390, y=35, height=BUTTON_HEIGHT, width=BUTTON_WIDTH + 30)

    def __minpath_press(self):
        self.__reset_colors()
        first_node = self.first_node_entry_min.get()
        second_node = self.second_node_entry_min.get()

        gui_graph: Graph = self.__gui._graph

        if first_node not in list(gui_graph._vertices.keys()):
            print("ERROR: first node not in graph's vertices")
            return
        elif second_node not in list(gui_graph._vertices.keys()):
            print("ERROR: second node not in graph's vertices")
            return

        min_path = gui_graph.min_number_edges(first_node, second_node)
        if len(min_path[0]) >= 2:
            for node in self.__gui.nodes:
                if node.id in min_path[0]:
                    if node.id == first_node or node.id == second_node:
                        self.__gui.canvas.itemconfigure(node.circle,
                                                        fill=self.__gui._AUTHOR_NAME_COLOR)
                    else:
                        self.__gui.canvas.itemconfigure(node.circle, fill=self.__gui._AUTHOR_NAME_COLOR)
        else:
            print("ERROR: there is no path from", first_node, "to", second_node)