"""
graphdisplay module created by Alberto Penas Díaz (https://github.com/seniorbeto).

WARNING: modifying this file may cause the program to stop working or work incorrectly.
"""
# Libraries
import tkinter as tk
import math
import time
import queue
import ctypes
import pprint
import platform
import multiprocessing as mp

# Modules
from .json_manager import JsonManager
from .about_win_manager import AboutWindow
from .tools_win_manager import ToolWindow
from .graphs import Graph
from .trees import AVLTree, BinarySearchTree
from .general_config import *


class GraphGUI:

    instance = 0

    def __new__(cls, graph, node_radius: int = 30, scr_width: int = 600, scr_height: int = 600, theme: str = 'BROWN'):
        GraphGUI.instance += 1
        if GraphGUI.instance > 5:
            raise Exception("For safety reasons, only five instances of GraphGUI can be created")
        if platform.system() == "Linux":
            mp.Process(target=cls._generate, args=(graph,
                                                    GraphGUI.instance,
                                                    node_radius,
                                                    scr_width,
                                                    scr_height,
                                                    theme)).start()
        else:
            try:
                pid = mp.Process(target=cls._generate, args=(graph,
                                                             GraphGUI.instance,
                                                             node_radius,
                                                             scr_width,
                                                             scr_height,
                                                             theme))
                pid.start()
            except RuntimeError:

                # For how multiprocessing works in python, it doesn't allow generating multiple processes
                # without using a "if __name__ == "__main__":" statement. By implementing a try/expect, we
                # can temporarily deal with this issue. Nevertheless, by doing this, there is a high chance
                # to run into code-duplication and zombie processes generations.

                print('\033[93m'+"WARNING:"+'\033[0m'+" it is highly recommended to run the program inside a\n\n"
                      "     if __name__ == \"__name__\":\n\n"
                      "statement in order to avoid issues and duplicated processes.\n"
                      "For more information please consider visiting the proyect \n"
                      "documentation at: https://github.com/seniorbeto/graphdisplay\n")

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)

    @staticmethod
    def _generate(graph, instance, node_radius, scr_width, scr_height, theme):
        GraphGUI.__GraphGUI(graph, instance, node_radius, scr_width, scr_height, theme)

    class __GraphGUI:
        def __init__(self, graph, instance, node_radius: int = 40, scr_width: int = 600, scr_height: int = 600, theme: str = 'BROWN'):
            """
            Creates a GraphGUI object, which will display the graph in a external window. Nodes can be moved with the mouse.
            The creation of the window will stop the execution of the program until the window is closed. Thus, it is recommended
            to create the GraphGUI object at the end of the program.
            :param graph: The graph to be displayed
            :param node_radius: The radius of the nodes (default 40)
            :param scr_width: The width of the window (default 600)
            :param scr_height: The height of the window (default 600)
            """
            start = time.time()
            if type(node_radius) != int:
                raise TypeError("The parameter node_radius must be an integer")
            if type(scr_width) != int or type(scr_height) != int:
                raise TypeError("The parameters scr_width and scr_height must be integers")
            if node_radius < 10 or node_radius > 100:
                raise ValueError("The parameter node_radius must be a value between 10 and 100")
            if scr_width < 200 or scr_height < 200:
                raise ValueError("The parameters scr_width and scr_height must be values greater than 200")
            if scr_width > 2000 or scr_height > 2000:
                raise ValueError("The parameters scr_width and scr_height must be values less than 2000")

            self.__ACTUAL_INSTANCE = instance
            self._graph = graph
            self.__node_radius = node_radius
            self.__scr_width = scr_width
            self.__scr_height = scr_height
            self.__XMARGIN = XMARGEN
            self.__YMARGIN = YMARGEN
            self._theme = theme.upper()
            self.nodes = []
            self.edges = []
            try:
                self._BACKGROUND_CANVAS_COLOR = THEMES[theme.upper()]['BACKGROUND_CANVAS_COLOR']
                self._BUTTON_COLOR = THEMES[theme.upper()]['BUTTON_COLOR']
                self._FRAME_COLOR = THEMES[theme.upper()]['FRAME_COLOR']
                self._VERTEX_COLOR = THEMES[theme.upper()]['VERTEX_COLOR']
                self._AUTHOR_NAME_COLOR = THEMES[theme.upper()]['AUTHOR_NAME_COLOR']
            except KeyError:
                raise ValueError("The theme must be one of the following: " + str(list(THEMES.keys())))

            try:
                self.__tree_root = graph._root
                self._is_tree = True

                # We will transform the tree into our own prototype, so that future changes are easier
                # to implement

                vertices = list(self.__levelorder(self.__tree_root).keys())
                if type(graph) == AVLTree:
                    self._graph = AVLTree()
                else:
                    self._graph = BinarySearchTree()

                for i in vertices:
                    self._graph.insert(i)

            except AttributeError:
                self._is_tree = False

                # We will transform the graph into our own prototype, so that future changes are easier
                # to implement

                vertices = list(graph._vertices.keys())
                self._graph = Graph(vertices)

                for vertex in graph._vertices:
                    for adj in graph._vertices[vertex]:
                        self._graph.addEdge(vertex, adj._vertex, adj._weight)

            # create the main window and start the GUI
            self.root = tk.Tk()
            self.root.title('GraphGUI')
            self.root.resizable(False, False)
            self.root.configure(bg=self._FRAME_COLOR, border=0, width=self.__scr_width, height=self.__scr_height)

            # Closing protocol
            self.root.protocol("WM_DELETE_WINDOW", self.__on_closing)

            self.canvas = tk.Canvas(self.root, bg=self._BACKGROUND_CANVAS_COLOR, bd=0)
            self.canvas.place(x=self.__XMARGIN,
                              y=self.__YMARGIN,
                              width=self.__scr_width - self.__XMARGIN * 2,
                              height=self.__scr_height - self.__YMARGIN * 2 - BUTTON_HEIGHT)

            # Buttons display
            self.__display_buttons()

            # Main display
            self.json_manager = JsonManager(self.root, self)
            data = self.json_manager.get_data('__last_store_'+str(self.__ACTUAL_INSTANCE))
            self.__display(data)

            self.canvas.tag_bind("movil", "<ButtonPress-1>", self.on_press)
            self.canvas.tag_bind("movil", "<Button1-Motion>", self.move)
            self.selected_node = None

            end = time.time()
            print("Displayed in:", round(end-start, 4))

            self.root.mainloop()

        def __display_buttons(self):
            # Reset button
            self.reset_button = tk.Button(self.root, text="Reset", bg=self._BUTTON_COLOR, command=self.display_reset,
                                          bd=0)
            self.reset_button.place(x=self.__XMARGIN,
                                    y=self.__scr_height - self.__YMARGIN // 2 - BUTTON_HEIGHT,
                                    width=BUTTON_WIDTH,
                                    height=BUTTON_HEIGHT)

            # Load button
            self.load_button = tk.Button(self.root, text="Load", bg=self._BUTTON_COLOR,
                                         command=self.__call_manager_load,
                                         bd=0)
            self.load_button.place(x=self.__XMARGIN + BUTTON_WIDTH + self.__XMARGIN,
                                   y=self.__scr_height - self.__YMARGIN // 2 - BUTTON_HEIGHT,
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT)

            # Save button
            self.save_button = tk.Button(self.root, text="Save", bg=self._BUTTON_COLOR,
                                         command=self.__call_manager_save,
                                         bd=0)
            self.save_button.place(x=self.__XMARGIN + (BUTTON_WIDTH + self.__XMARGIN) * 2,
                                   y=self.__scr_height - self.__YMARGIN // 2 - BUTTON_HEIGHT,
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT)

            # Delete button
            self.save_button = tk.Button(self.root, text="Delete", bg=self._BUTTON_COLOR,
                                         command=self.__call_manager_delete, bd=0)
            self.save_button.place(x=self.__XMARGIN + (BUTTON_WIDTH + self.__XMARGIN) * 3,
                                   y=self.__scr_height - self.__YMARGIN // 2 - BUTTON_HEIGHT,
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT)

            # About button
            self.save_button = tk.Button(self.root, text="About", bg=self._BUTTON_COLOR,
                                         command=self.__call_about_window, bd=0)
            self.save_button.place(x=self.__scr_width - self.__XMARGIN - BUTTON_WIDTH,
                                   y=self.__scr_height - self.__YMARGIN // 2 - BUTTON_HEIGHT,
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT)

            # Tools button
            self.save_button = tk.Button(self.root, text="Tools", bg=self._BUTTON_COLOR,
                                         command=self.__call_tools_window, bd=0)
            self.save_button.place(x=self.__XMARGIN + (BUTTON_WIDTH + self.__XMARGIN) * 4,
                                   y=self.__scr_height - self.__YMARGIN // 2 - BUTTON_HEIGHT,
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT)

        def __call_tools_window(self):
            if not self._is_tree:
                ToolWindow(self.root, self)

        def __call_about_window(self):
            AboutWindow(self.root, self)

        def __call_manager_delete(self):
            if not self._is_tree:
                self.json_manager.generate_delete_window()
            else:
                tk.messagebox.showerror("Error", "This function is not yet available for trees")

        def __call_manager_load(self):
            if not self._is_tree:
                new_position = self.json_manager.generate_load_window()
                if new_position:
                    self.display_reset(new_position)
            else:
                tk.messagebox.showerror("Error", "This function is not yet available for trees")

        def __call_manager_save(self):
            if not self._is_tree:
                curr_pos = {}
                for node in self.nodes:
                    curr_pos[node.id] = (node.pos_x, node.pos_y)
                self.json_manager.generate_save_window(curr_pos)
            else:
                tk.messagebox.showerror("Error", "This function is not yet available for trees")

        def display_reset(self, new_data: dict = None):
            self.canvas.delete("all")
            self.__display(new_data)

        def __display(self, data: dict = None):
            if not self._is_tree:
                # Preparation for the nodes display
                scr_center = ((self.__scr_width - 14) // 2, (self.__scr_height - 30) // 2)
                display_radius = min(self.__scr_width - 30 - self.__node_radius, self.__scr_height - 14 - self.__node_radius) // 2 - self.__node_radius - 10
                arch_angle = 360 / len(self._graph._vertices)
                first_node_pos = (scr_center[0] - self.__node_radius, scr_center[1] - self.__node_radius)

                # Display the nodes
                self.nodes = []
                i = 0
                angle = 0
                for vertex in self._graph._vertices:
                    if i == 0:
                        if data and str(vertex) in data and \
                                data[str(vertex)][0] < self.__scr_width and \
                                data[str(vertex)][1] < self.__scr_height - 30 and \
                                data[str(vertex)][0] + self.__node_radius*2 > 0 and \
                                data[str(vertex)][1] + self.__node_radius*2 > 0:
                            self.nodes.append(
                                Node(self.canvas,
                                     self.__node_radius,
                                     data[str(vertex)][0],
                                     data[str(vertex)][1],
                                     text=vertex,
                                     bg=self._VERTEX_COLOR))
                        else:
                            self.nodes.append(
                                Node(self.canvas,
                                     self.__node_radius,
                                     first_node_pos[0],
                                     first_node_pos[1],
                                     text=vertex,
                                     bg=self._VERTEX_COLOR))
                    else:
                        if data and str(vertex) in data and \
                                data[str(vertex)][0] < self.__scr_width and \
                                data[str(vertex)][1] < self.__scr_height - 30 and \
                                data[str(vertex)][0] + self.__node_radius*2 > 0 and \
                                data[str(vertex)][1] + self.__node_radius*2 > 0:
                            self.nodes.append(
                                Node(self.canvas,
                                     self.__node_radius,
                                     data[str(vertex)][0],
                                     data[str(vertex)][1],
                                     text=vertex,
                                     bg=self._VERTEX_COLOR))
                        else:
                            self.nodes.append(Node(self.canvas,
                                                   self.__node_radius,
                                                   int(scr_center[0] - self.__node_radius - display_radius * math.sin(
                                                       math.radians(angle))),
                                                   int(scr_center[1] - self.__node_radius - display_radius * math.cos(
                                                       math.radians(angle))),
                                                   text=vertex, bg=self._VERTEX_COLOR))
                    i += 1
                    angle += arch_angle

                # Create the edges
                i = 0
                self.edges = []
                for vertex in self._graph._vertices:
                    for adj in self._graph._vertices[vertex]:
                        for node in self.nodes:
                            if node.id == adj._vertex:
                                self.edges.append(Edge(self.canvas,
                                                       self.nodes[i],
                                                       node,
                                                       adj._weight if adj._weight else 1,
                                                       window_color=self._BACKGROUND_CANVAS_COLOR))
                                node.asociated_edges_IN.append(self.edges[-1])
                                self.nodes[i].asociated_edges_OUT.append(self.edges[-1])
                    i += 1

                # Display the edges
                if self._graph._directed:
                    for edge in self.edges:
                        edge_start_node = edge.start_node
                        edge_end_node = edge.end_node
                        found = False
                        for i in edge_start_node.asociated_edges_IN:
                            if i.start_node == edge_end_node:
                                found = True
                                edge.overlaped = True
                                edge.show()
                                break
                        if not found:
                            edge.show()
                else:
                    for edge in self.edges:
                        edge.show()

            elif self._is_tree:
                self.nodes = []
                self.edges = []
                root_position = ((self.__scr_width - self.__node_radius*2) // 2, self.__YMARGIN + 33)
                self.nodes.append(Node(self.canvas,
                                       self.__node_radius,
                                       root_position[0],
                                       root_position[1],
                                       text=self._graph._root.elem,
                                       bg=self._VERTEX_COLOR))

                # We display the rest of the nodes in a tree-like structure by
                # dividing the screen in levels and displaying the nodes in each level
                level_order = self.__levelorder(self._graph._root)
                levels = max(level_order.values()) + 1
                level_height = (self.__scr_height - self.__YMARGIN - 60) // levels

                # We determine how many nodes are in each level
                last_nodes = [self._graph._root.elem]
                for i in range(levels - 1):
                    if i != 0:
                        last_nodes = nodes_in_level
                    nodes_in_level = []
                    for node in level_order:
                        if level_order[node] == i + 1:
                            nodes_in_level.append(node)

                    level_grid = 2**(i + 1)

                    # We determine the x_axis of each node in the level
                    x_axis = (self.__scr_width - (self.__XMARGIN * 2) - (self.__node_radius * 2)) // level_grid
                    x_axis_counter = 0

                    final_nodes = nodes_in_level + last_nodes
                    final_nodes.sort()
                    for node in last_nodes:
                        # We look for the position x of the father
                        for aux in self.nodes:
                            if node == aux.id:
                                position_x = aux.pos_x
                                father_node = aux
                                break
                        relative = last_nodes.index(node) + 1
                        children_left, children_right = self.__get_children(node)
                        if children_left or children_left == 0:
                            final_position_x = position_x - x_axis // 2
                            if final_position_x <= self.__XMARGIN + 5:
                                final_position_x = self.__XMARGIN + 5
                            new_node = Node(self.canvas,
                                            self.__node_radius,
                                            final_position_x,
                                            root_position[1] + level_height*(level_order[children_left]),
                                            text=children_left,
                                            bg=self._VERTEX_COLOR)
                            self.nodes.append(new_node)
                            new_edge = Edge(self.canvas,
                                            father_node,
                                            new_node,
                                            None,
                                            window_color=self._BACKGROUND_CANVAS_COLOR)
                            new_edge.show()
                            self.edges.append(new_edge)
                            new_node.asociated_edges_IN.append(new_edge)
                            father_node.asociated_edges_OUT.append(new_edge)

                        if children_right or children_right == 0:
                            final_position_x = position_x + x_axis // 2
                            if final_position_x >= self.__scr_width - (self.__XMARGIN * 2) - (self.__node_radius * 2) - 5:
                                final_position_x = self.__scr_width - (self.__XMARGIN * 2) - (self.__node_radius * 2) - 5

                            new_node = Node(self.canvas,
                                            self.__node_radius,
                                            final_position_x,
                                            root_position[1] + level_height*(level_order[children_right]),
                                            text=children_right,
                                            bg=self._VERTEX_COLOR)
                            self.nodes.append(new_node)
                            new_edge = Edge(self.canvas,
                                            father_node,
                                            new_node,
                                            None,
                                            window_color=self._BACKGROUND_CANVAS_COLOR)
                            new_edge.show()
                            self.edges.append(new_edge)
                            new_node.asociated_edges_IN.append(new_edge)
                            father_node.asociated_edges_OUT.append(new_edge)


            # Display author
            self.__autor = self.canvas.create_text(self.__scr_width // 2, self.__YMARGIN + 3, text="by @seniorbeto",
                                                   fill=self._AUTHOR_NAME_COLOR, font=("Courier", 10))

        def __get_children(self, elem) -> tuple:
            """returns a tuple with the children of node"""
            node = self.__search_node(elem)
            return node.left.elem if node.left else None, node.right.elem if node.right else None

        def __search_node(self, elem):
            """returns the node with the given element"""
            return self.__search_node_aux(self._graph._root, elem)

        def __search_node_aux(self, node, elem):
            """returns the node with the given element"""
            if node == None:
                return None
            if node.elem == elem:
                return node
            else:
                return self.__search_node_aux(node.left, elem) or self.__search_node_aux(node.right, elem)

        def __levelorder(self, node) -> dict:
            """
            returns a dictionary with the level order of the tree and the height of each node
            """
            register = {}
            q = queue.Queue()
            q.put(node)  # enqueue: we save the root
            register[node.elem] = 0

            while q.empty() == False:
                current = q.get()  # dequeue
                value = register[current.elem]
                if current.left != None:
                    q.put(current.left)
                    register[current.left.elem] = value + 1
                if current.right != None:
                    q.put(current.right)
                    register[current.right.elem] = value + 1

            return register

        def __on_closing(self):
            data = {}
            for node in self.nodes:
                data[node.id] = (node.pos_x, node.pos_y)
            self.json_manager.save_data('__last_store_'+str(self.__ACTUAL_INSTANCE), data)
            self.root.destroy()

        def on_press(self, event):
            node = self.canvas.find_withtag(tk.CURRENT)
            self.selected_node = (node, event.x, event.y)

        def move(self, event):
            x, y = event.x, event.y
            node, x0, y0 = self.selected_node
            for i in self.nodes:
                if i.circle == node[0] or i.text == node[0]:
                    self.canvas.move(i.circle, x - x0, y - y0)
                    self.canvas.move(i.text, x - x0, y - y0)
                    i.pos_x += x - x0
                    i.pos_y += y - y0
                    for edge in i.asociated_edges_IN:
                        edge_start = edge.start_node
                        weight = edge.weight
                        color = edge.window_color
                        overlaped = edge.overlaped
                        i.asociated_edges_IN.remove(edge)
                        edge.terminate()
                        new_edge = Edge(self.canvas, edge_start, i, weight, overlaped=overlaped, window_color=color)
                        new_edge.show()
                        i.asociated_edges_IN.append(new_edge)
                        for nd in self.nodes:
                            if edge in nd.asociated_edges_OUT:
                                nd.asociated_edges_OUT.remove(edge)
                                nd.asociated_edges_OUT.append(new_edge)
                                break
                    for edge in i.asociated_edges_OUT:
                        edge_end = edge.end_node
                        weight = edge.weight
                        color = edge.window_color
                        overlaped = edge.overlaped
                        i.asociated_edges_OUT.remove(edge)
                        edge.terminate()
                        new_edge = Edge(self.canvas, i, edge_end, weight, overlaped=overlaped, window_color=color)
                        new_edge.show()
                        i.asociated_edges_OUT.append(new_edge)
                        for nd in self.nodes:
                            if edge in nd.asociated_edges_IN:
                                nd.asociated_edges_IN.remove(edge)
                                nd.asociated_edges_IN.append(new_edge)
                                break


            self.selected_node = (node, x, y)

class Node:
    def __init__(self, canvas: tk.Canvas, radius:int, posx: int, posy: int, text: str, bg: str = "white"):
        self.asociated_edges_IN = []
        self.asociated_edges_OUT = []
        self.canvas = canvas
        self.id = text
        self.radius = radius
        self.pos_x = posx
        self.pos_y = posy
        self.circle = canvas.create_oval(self.pos_x, self.pos_y, self.pos_x + self.radius*2, self.pos_y + self.radius*2, fill=bg, width=2,)
        self.text = canvas.create_text(self.pos_x + self.radius, self.pos_y + self.radius, text=text)
        canvas.addtag_enclosed("movil", self.pos_x - 3, self.pos_y - 3, self.pos_x + self.radius * 2 + 3, self.pos_y + self.radius * 2 + 3)

    def terminate(self):
        for edge in self.asociated_edges_IN:
            edge.terminate()
        for edge in self.asociated_edges_OUT:
            edge.terminate()
        self.canvas.delete(self.circle)
        self.canvas.delete(self.text)

class Edge:
    def __init__(self, canvas: tk.Canvas, start: Node, end: Node, weight: int = 1, overlaped: bool = False, window_color: str = "white"):
        self.canvas = canvas
        self.overlaped = overlaped
        self.start_node = start
        self.end_node = end
        self.weight = weight
        self.window_color = window_color
        self.start = self.__calculate_start(start, end)
        self.end = self.__calculate_end(start, end)

    def terminate(self):
        self.canvas.delete(self.line)
        if self.weight:
            self.canvas.delete(self.window)

    def show(self):
        self.line = self.canvas.create_line(self.start[0], self.start[1], self.end[0], self.end[1], arrow=tk.LAST, width=1.5)
        if self.weight:
            if not self.overlaped:
                self.window = self.canvas.create_window((self.start[0] + self.end[0]) // 2, (self.start[1] + self.end[1]) // 2,
                                                   window=tk.Label(self.canvas,bg=self.window_color ,text=str(self.weight)))
            else:
                self.window = self.canvas.create_window((self.start[0] * 0.2 + self.end[0] * 0.8),
                                                   (self.start[1] * 0.2 + self.end[1] * 0.8),
                                                   window=tk.Label(self.canvas, bg=self.window_color, text=str(self.weight)))

    def __calculate_start(self, start: Node, end: Node) -> tuple:
        """
        It calculates the initial position of the arrow that connects the nodes "start" and "end"
        :param start: Node
        :param end: Node
        :return: tuple with the initial position of the arrow
        """
        center_start = (start.pos_x + start.radius, start.pos_y + start.radius)
        center_end = (end.pos_x + end.radius, end.pos_y + end.radius)

        x1 = center_start[0]
        y1 = center_start[1]
        x2 = center_end[0]
        y2 = center_end[1]

        x = x2 - x1
        y = y2 - y1
        edge_angle = math.atan2(y, x) * (180.0 / math.pi)
        x = math.cos(math.radians(edge_angle)) * start.radius
        y = math.sin(math.radians(edge_angle)) * start.radius
        return (center_start[0] + int(x), center_start[1] + int(y))

    def __calculate_end(self, start: Node, end: Node) -> tuple:
        """
        It calculates the final position of the arrow that connects the nodes "start" and "end"
        :param start: Node
        :param end: Node
        :return: tuple with the final position of the arrow
        """
        center_start = (start.pos_x + start.radius, start.pos_y + start.radius)
        center_end = (end.pos_x + end.radius, end.pos_y + end.radius)

        x1 = center_start[0]
        y1 = center_start[1]
        x2 = center_end[0]
        y2 = center_end[1]

        x = x2 - x1
        y = y2 - y1
        edge_angle = math.atan2(y, x) * (180.0 / math.pi)
        x = math.cos(math.radians(edge_angle)) * end.radius
        y = math.sin(math.radians(edge_angle)) * end.radius
        return  (center_end[0] - int(x), center_end[1] - int(y))

if __name__ == "__main__":
    pass