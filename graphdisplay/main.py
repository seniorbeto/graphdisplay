"""
graphdisplay module created by Alberto Penas Díaz (https://github.com/seniorbeto).

WARNING: modifying this file may cause the program to stop working or work incorrectly.
"""
# Libraries
import tkinter as tk
import tkinter.ttk as ttk
import math
import copy
import time
import queue
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
    """
    Creates a GraphGUI object, which will display the graph in an external window. Nodes can be moved with the mouse.
    :param graph: The graph/tree to be displayed.
    :param node_radius: The radius of the nodes.
    :param scr_width: The width of the window.
    :param scr_height: The height of the window.
    :param theme: color scheme of the node display.
    """

    # Using an instance-counter will determine how many GraphGUI objects are wanted
    instance = 0

    def __new__(cls, graph, node_radius: int = 30, theme: str = 'BROWN'):
        GraphGUI.instance += 1
        if GraphGUI.instance > 5:
            raise Exception("For safety reasons, only five instances of GraphGUI can be created")

        # Generate multiprocessing

        if platform.system() == "Linux":
            mp.Process(target=cls._generate, args=(graph,
                                                    GraphGUI.instance,
                                                    node_radius,
                                                    theme)).start()
        else:
            try:
                pid = mp.Process(target=cls._generate, args=(graph,
                                                             GraphGUI.instance,
                                                             node_radius,
                                                             theme))
                pid.start()
            except RecursionError:
                print('\n' + '\033[91m' + "ERROR: " + '\033[0m' + "For how GraphGUI works, high-demanding recursion trees are"
                                                                 " not supported. Sorry for the inconvenience. ")
            except RuntimeError:

                # For how multiprocessing works in python, it doesn't allow generating multiple processes
                # without using a "if __name__ == "__main__":" statement. By implementing a try/expect, we
                # can temporarily deal with this issue. Nevertheless, by doing this, there is a high chance
                # to run into code-duplication and zombie processes generations.

                print('\n'+'\033[93m'+"WARNING:"+'\033[0m'+" it is highly recommended to run the program inside a\n\n"
                      "     if __name__ == \"__main__\":\n\n"
                      "statement in order to avoid issues and duplicated processes.\n"
                      "For more information please consider visiting the proyect \n"
                      "documentation at: https://github.com/seniorbeto/graphdisplay\n")

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)

    @staticmethod
    def _generate(graph, instance, node_radius, theme):
        GraphGUI.__GraphGUI(graph, instance, node_radius, theme)

    class __GraphGUI:
        def __init__(self, graph, instance, node_radius: int = 40, theme: str = 'BROWN'):
            """
            Creates a GraphGUI object, which will display the graph in a external window. Nodes can be moved with the mouse.
            The creation of the window will stop the execution of the program until the window is closed. Thus, it is recommended
            to create the GraphGUI object at the end of the program.
            :param graph: The graph to be displayed
            :param node_radius: The radius of the nodes (default 40)
            :param scr_width: The width of the window (default 600)
            :param scr_height: The height of the window (default 600)
            """

            # Begin time measurement
            start = time.time()

            # Parameter validation
            if type(node_radius) != int:
                raise TypeError("The parameter node_radius must be an integer")
            if node_radius < 10 or node_radius > 100:
                raise ValueError("The parameter node_radius must be a value between 10 and 100")

            self.__ACTUAL_INSTANCE = instance
            self._graph = graph
            self.__node_radius = node_radius
            self.__scr_width = DEFAULT_SCR_WIDTH
            self.__scr_height = DEFAULT_SCR_WIDTH
            self.__XMARGIN = XMARGEN
            self.__YMARGIN = YMARGEN
            self._theme = theme.upper()
            self.nodes = {}
            self.edges = []
            self.__canvas_node_relation = {}
            try:
                self._BACKGROUND_CANVAS_COLOR = THEMES[theme.upper()]['BACKGROUND_CANVAS_COLOR']
                self._BUTTON_COLOR = THEMES[theme.upper()]['BUTTON_COLOR']
                self._SELECTED_VERTEX_COLOR = THEMES[theme.upper()]['SELECTED_VERTEX_COLOR']
                self._FRAME_COLOR = THEMES[theme.upper()]['FRAME_COLOR']
                self._VERTEX_COLOR = THEMES[theme.upper()]['VERTEX_COLOR']
                self._AUTHOR_NAME_COLOR = THEMES[theme.upper()]['AUTHOR_NAME_COLOR']
            except KeyError:
                raise ValueError("The theme must be one of the following: " + str(list(THEMES.keys())))

            # We will transform the graph type into our own prototype, so that future changes are easier
            # to implement. Beyond this point, code will be implemented based on these prototypes.
            try:
                self.__tree_root = graph._root
                self._is_tree = True

                vertices = list(self.__levelorder(self.__tree_root).keys())
                if type(graph) == AVLTree:
                    self._graph = AVLTree()
                else:
                    self._graph = BinarySearchTree()

                for i in vertices:
                    self._graph.insert(i)

            except AttributeError:
                self._is_tree = False

                vertices = list(graph._vertices.keys())
                self._graph = Graph(vertices)

                for vertex in graph._vertices:
                    for adj in graph._vertices[vertex]:
                        self._graph.addEdge(vertex, adj._vertex, adj._weight)

            # Create the main window
            self.root = tk.Tk()
            self.root.title('GraphGUI')
            self.root.geometry(f"{self.__scr_width}x{self.__scr_height}")
            self.root.configure(bg=self._FRAME_COLOR, border=0)

            # Canvas Frame
            self.__canvas_frame = tk.Frame(self.root, bg=self._BACKGROUND_CANVAS_COLOR)
            self.__canvas_frame.pack(expand=1, fill='both', pady=self.__YMARGIN, padx=self.__XMARGIN)

            # Closing protocol
            self.root.protocol("WM_DELETE_WINDOW", self.__on_closing)

            # Canvas creation and placement
            self.canvas = tk.Canvas(self.__canvas_frame, bg=self._BACKGROUND_CANVAS_COLOR, bd=0,
                                    width=self.__scr_width - self.__XMARGIN * 2,
                                    height=self.__scr_height - self.__YMARGIN * 2 - BUTTON_HEIGHT)
            self.canvas.pack(fill='both', expand=1)

            # Menu display ( Experimental )
            self.__menu_display()

            # Main display
            self.json_manager = JsonManager(self.root, self)
            data = self.json_manager.get_data('__last_store_'+str(self.__ACTUAL_INSTANCE))
            self.__display(data)
            if data:
                actual_scr_width = data['Screen_dimensions'][0]
                actual_scr_height = data['Screen_dimensions'][1]
                self.root.geometry(f'{actual_scr_width}x{actual_scr_height}')

            # Tag_bind for movable canvas objects
            self.canvas.tag_bind("movil", "<ButtonPress-1>", self.on_press)
            if self._is_tree and platform.system() != "Linux":
                self.canvas.tag_bind("movil", "<Button-3>", self.on_press_left)
            self.canvas.tag_bind("movil", "<Button1-Motion>", self.move)
            self.selected_node = None

            # End time measurement
            end = time.time()
            print("Displayed in:", round(end-start, 4))

            # Main display protocol
            self.root.mainloop()

        def __menu_display(self):
            self.__main_menu = tk.Menu(self.root)
            self.root.config(menu=self.__main_menu)

            self.__file_menu = tk.Menu(self.__main_menu, tearoff=False)
            self.__main_menu.add_cascade(label='File', menu=self.__file_menu)

            self.__file_menu.add_command(label='Save', command=self.__call_manager_save)
            self.__file_menu.add_command(label='Reset', command=self.display_reset)
            self.__file_menu.add_command(label='Load', command=self.__call_manager_load)
            self.__file_menu.add_command(label='Delete', command=self.__call_manager_delete)

            self.__tools_menu = tk.Menubutton(self.__main_menu)
            self.__main_menu.add_cascade(label='Tools', menu=self.__tools_menu, command=self.__call_tools_window)

            self.__about_menu = tk.Menubutton(self.__main_menu)
            self.__main_menu.add_cascade(label='About', menu=self.__about_menu, command=self.__call_about_window)


        def __call_tools_window(self):
            """Generator of ToolWindow"""
            ToolWindow(self.root, self)

        def __call_about_window(self):
            """Generator of AboutWindow"""
            AboutWindow(self.root, self)

        def __call_manager_delete(self):
            """Generator of Delete Window"""
            if not self._is_tree:
                self.json_manager.generate_delete_window()
            else:
                tk.messagebox.showerror("Error", "This function is not yet available for trees")

        def __call_manager_load(self):
            """Generator of Load Window"""
            if not self._is_tree:
                new_position = self.json_manager.generate_load_window()
                if new_position:
                    self.display_reset(new_position)
            else:
                tk.messagebox.showerror("Error", "This function is not yet available for trees")

        def __call_manager_save(self):
            """Generator of Save Window"""
            if not self._is_tree:
                curr_pos = {}
                actual_scr_width = self.root.winfo_width()
                actual_scr_height = self.root.winfo_height()
                curr_pos['Screen_dimensions'] = (actual_scr_width, actual_scr_height)
                for node in self.nodes:
                    curr_pos[node] = (self.nodes[node].pos_x, self.nodes[node].pos_y)
                self.json_manager.generate_save_window(curr_pos)
            else:
                tk.messagebox.showerror("Error", "This function is not yet available for trees")

        def display_reset(self, new_data: dict = None):
            """
            Sets the main display to default by deleting all objects in canvas and displaying them
            in the position stored in new_data.
            """
            self.canvas.delete("all")
            self.__display(new_data)

        def __display(self, data: dict = None):
            """
            Main display for all nodes in the canvas, whose position is determined in "data".
            If data is None, the default display will be showed. This is, in case of a simple graph,
            the first vertex in the middle of the screen and the rest surrounding it in a polygon shape.
            In case of a tree, it is always display in a tree-like structure.

            This function also checks if some node position has been stored outside the frames of the window,
            in which case will correct.
            """
            # First, we store the actual dimensions of the screen
            if data:
                actual_scr_width = data['Screen_dimensions'][0]
                actual_scr_height = data['Screen_dimensions'][1]
            else:
                actual_scr_width = self.root.winfo_width()
                actual_scr_height = self.root.winfo_height()
                if actual_scr_height == 1 and actual_scr_width == 1:
                    actual_scr_width = DEFAULT_SCR_WIDTH
                    actual_scr_height = DEFAULT_SCR_HEIGHT


            if not self._is_tree:
                # Preparation for the nodes display
                scr_center = ((actual_scr_width - (self.__XMARGIN*2)) // 2, (actual_scr_height - (self.__YMARGIN*2)) // 2)
                display_radius = min(actual_scr_width - 30 - self.__node_radius, actual_scr_height - 14 - self.__node_radius) // 2 - self.__node_radius - 10
                arch_angle = 360 / len(self._graph._vertices)
                first_node_pos = (scr_center[0] - self.__node_radius, scr_center[1] - self.__node_radius)

                # Display the nodes
                self.nodes = {}
                i = 0
                angle = 0
                for vertex in self._graph._vertices:
                    # The first vertex will be displayed in the screen center
                    if i == 0:
                        if data and str(vertex) in data and \
                                data[str(vertex)][0] < actual_scr_width and \
                                data[str(vertex)][1] < actual_scr_height - 30 and \
                                data[str(vertex)][0] + self.__node_radius*2 > 0 and \
                                data[str(vertex)][1] + self.__node_radius*2 > 0:
                            node = Node(self.canvas,
                                     self.__node_radius,
                                     data[str(vertex)][0],
                                     data[str(vertex)][1],
                                     text=vertex,
                                     bg=self._VERTEX_COLOR)
                            self.nodes[vertex] = node
                        else:
                            node = Node(self.canvas,
                                     self.__node_radius,
                                     first_node_pos[0],
                                     first_node_pos[1],
                                     text=vertex,
                                     bg=self._VERTEX_COLOR)
                            self.nodes[vertex] = node
                    else:
                        # Those vertices that are not the first, will surround the screen center, scrolling
                        # around an imaginary circumference.
                        if data and str(vertex) in data and \
                                data[str(vertex)][0] < actual_scr_width and \
                                data[str(vertex)][1] < actual_scr_height - 30 and \
                                data[str(vertex)][0] + self.__node_radius*2 > 0 and \
                                data[str(vertex)][1] + self.__node_radius*2 > 0:
                            node = Node(self.canvas,
                                     self.__node_radius,
                                     data[str(vertex)][0],
                                     data[str(vertex)][1],
                                     text=vertex,
                                     bg=self._VERTEX_COLOR)
                            self.nodes[vertex] = node
                        else:
                            node = Node(self.canvas,
                                                   self.__node_radius,
                                                   int(scr_center[0] - self.__node_radius - display_radius * math.sin(
                                                       math.radians(angle))),
                                                   int(scr_center[1] - self.__node_radius - display_radius * math.cos(
                                                       math.radians(angle))),
                                                   text=vertex, bg=self._VERTEX_COLOR)
                            self.nodes[vertex] = node
                    i += 1
                    angle += arch_angle

                # Create the edges
                i = 0
                self.edges = []
                for vertex in self._graph._vertices:
                    for adj in self._graph._vertices[vertex]:
                        node = self.nodes[adj._vertex]
                        self.edges.append(Edge(self.canvas,
                                               self.nodes[vertex],
                                               node,
                                               adj._weight,
                                               window_color=self._BACKGROUND_CANVAS_COLOR))
                    i += 1

                # While displaying the edges, we first have to check if it is needed to display the weight
                # in an edge side (instead of the center) in case that two vertices are pointing to each other,
                # since this would result in an overlap between those two weights.
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
                # The tree display is slightly more complicated (it was a complete nightmare for a one man job
                # to be honest). For information on how it works, please consider visiting: #TODO
                self.nodes = {}
                self.edges = []
                root_position = ((actual_scr_width - self.__node_radius*2) // 2, self.__YMARGIN + 3)
                root_node = Node(self.canvas,
                                       self.__node_radius,
                                       root_position[0],
                                       root_position[1],
                                       text=self._graph._root.elem,
                                       bg=self._VERTEX_COLOR)
                self.nodes[self._graph._root.elem] = root_node

                # We display the rest of the nodes in a tree-like structure by
                # dividing the screen in levels and displaying the nodes in each level
                level_order = self.__levelorder(self._graph._root)
                levels = max(level_order.values()) + 1
                level_height = (actual_scr_height - self.__YMARGIN*2 - self.__node_radius) // levels
                level_list = []
                for _ in range(levels):
                    level_list.append([])
                for node in level_order:
                    level_list[level_order[node]].append(node)

                # We determine how many nodes are in each level
                last_nodes = [self._graph._root.elem]
                for i in range(levels - 1):
                    if i != 0:
                        last_nodes = nodes_in_level
                    nodes_in_level = level_list[i+1]

                    level_grid = 2**(i + 1)

                    # We determine the x_axis of each node in the level
                    x_axis = (actual_scr_width - (self.__XMARGIN * 2) - (self.__node_radius * 2)) // level_grid
                    x_axis_counter = 0

                    final_nodes = nodes_in_level + last_nodes
                    final_nodes.sort()
                    for node in last_nodes:
                        # We look for the position x of the father
                        position_x = self.nodes[node].pos_x
                        father_node = self.nodes[node]

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
                            self.nodes[children_left] = new_node
                            new_edge = Edge(self.canvas,
                                            father_node,
                                            new_node,
                                            None,
                                            window_color=self._BACKGROUND_CANVAS_COLOR)
                            new_edge.show()
                            self.edges.append(new_edge)

                        if children_right or children_right == 0:
                            final_position_x = position_x + x_axis // 2
                            if final_position_x >= actual_scr_width - (self.__XMARGIN * 2) - (self.__node_radius * 2) - 5:
                                final_position_x = actual_scr_width - (self.__XMARGIN * 2) - (self.__node_radius * 2) - 5

                            new_node = Node(self.canvas,
                                            self.__node_radius,
                                            final_position_x,
                                            root_position[1] + level_height*(level_order[children_right]),
                                            text=children_right,
                                            bg=self._VERTEX_COLOR)
                            self.nodes[children_right] = new_node
                            new_edge = Edge(self.canvas,
                                            father_node,
                                            new_node,
                                            None,
                                            window_color=self._BACKGROUND_CANVAS_COLOR)
                            new_edge.show()
                            self.edges.append(new_edge)

            # We will store each canvas TAGorID with each associated node object in order
            # to reduce movement complexity to O(1)
            self.__canvas_node_relation = {}
            for node in self.nodes:
                self.__canvas_node_relation[self.nodes[node].circle] = self.nodes[node]
                self.__canvas_node_relation[self.nodes[node].text] = self.nodes[node]

        def __get_children(self, elem) -> tuple:
            """returns a tuple with the children of node with element = elem"""
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
            """Store the current data at closing protocol"""
            data = {}
            actual_scr_width = self.root.winfo_width()
            actual_scr_height = self.root.winfo_height()
            data['Screen_dimensions'] = (actual_scr_width, actual_scr_height)
            for node in self.nodes:
                data[node] = (self.nodes[node].pos_x, self.nodes[node].pos_y)
            self.json_manager.save_data('__last_store_'+str(self.__ACTUAL_INSTANCE), data)
            self.root.destroy()

        def on_press_left(self, event):
            """
            If, in a tree, a node is left-clicked, it will generate a display of the subtree
            """
            if self._is_tree:
                node = self.canvas.find_withtag(tk.CURRENT)
                node_obj = self.__canvas_node_relation[node[0]]
                root = self.__search_node(node_obj.id)
                vertices = self.__levelorder(root)
                new_tree = copy.copy(self._graph)
                new_tree.remove_all()
                for i in list(vertices.keys()):
                    new_tree.insert(i)
                GraphGUI(new_tree,
                         self.__node_radius,
                         self._theme)

        def on_press(self, event):
            """Right mouse click protocol"""
            # Store the node if it has been right-clicked
            node = self.canvas.find_withtag(tk.CURRENT)
            self.selected_node = (node, event.x, event.y)

        def move(self, event):
            """
            It moves a node if it has been selected on the right mouse click protocol. After moving it, it updates
            automatically all edges attached to the node.
            """
            x, y = event.x, event.y
            node, x0, y0 = self.selected_node
            node_obj = self.__canvas_node_relation[node[0]]
            self.canvas.move(node_obj.circle, x - x0, y - y0)
            self.canvas.move(node_obj.text, x - x0, y - y0)
            node_obj.pos_x += x - x0
            node_obj.pos_y += y - y0
            for edge in node_obj.asociated_edges_IN:
                edge.update_position()
            for edge in node_obj.asociated_edges_OUT:
                edge.update_position()
            self.selected_node = (node, x, y)

class Node:
    def __init__(self, canvas: tk.Canvas, radius: int, posx: int, posy: int, text: str, bg: str = "white"):
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

        if self not in self.end_node.asociated_edges_IN:
            self.end_node.asociated_edges_IN.append(self)
        if self not in self.start_node.asociated_edges_OUT:
            self.start_node.asociated_edges_OUT.append(self)

    def update_position(self):
        self.__recalculate()
        self.canvas.coords(self.line, self.start[0], self.start[1], self.end[0], self.end[1])
        if self.weight:
            if not self.overlaped:
                self.canvas.coords(self.window, (self.start[0] + self.end[0]) // 2, (self.start[1] + self.end[1]) // 2)
            else:
                self.canvas.coords(self.window, self.start[0] * 0.2 + self.end[0] * 0.8, self.start[1] * 0.2 + self.end[1] * 0.8)

    def terminate(self):
        self.canvas.delete(self.line)
        if self.weight:
            self.canvas.delete(self.window)

    def show(self):
        self.line = self.canvas.create_line(self.start[0],
                                            self.start[1],
                                            self.end[0],
                                            self.end[1],
                                            arrow=tk.LAST,
                                            width=1.5)
        if self.weight:
            if not self.overlaped:
                self.window = self.canvas.create_window((self.start[0] + self.end[0]) // 2,
                                                        (self.start[1] + self.end[1]) // 2,
                                                        window=tk.Label(self.canvas,
                                                                        bg=self.window_color,
                                                                        text=str(self.weight)))
            else:
                self.window = self.canvas.create_window((self.start[0] * 0.2 + self.end[0] * 0.8),
                                                        (self.start[1] * 0.2 + self.end[1] * 0.8),
                                                        window=tk.Label(self.canvas,
                                                                        bg=self.window_color,
                                                                        text=str(self.weight)))

    def __recalculate(self):
        self.start = self.__calculate_start(self.start_node, self.end_node)
        self.end = self.__calculate_end(self.start_node, self.end_node)

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
