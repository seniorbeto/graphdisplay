import tkinter as tk
import json
import math
import os

class GraphGUI:

    instance = 0

    def __new__(cls, graph, node_radius: int = 40, scr_width: int = 600, scr_height: int = 600):
        GraphGUI.instance += 1
        return GraphGUI.__GraphGUI(graph, GraphGUI.instance, node_radius, scr_width, scr_height)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)

    class __GraphGUI:
        def __init__(self, graph, instance, node_radius: int = 40, scr_width: int = 600, scr_height: int = 600):
            """
            Creates a GraphGUI object, which will display the graph in a external window. Nodes can be moved with the mouse.
            The creation of the window will stop the execution of the program until the window is closed. Thus, it is recommended
            to create the GraphGUI object at the end of the program.
            :param graph: The graph to be displayed
            :param node_radius: The radius of the nodes (default 40)
            :param scr_width: The width of the window (default 600)
            :param scr_height: The height of the window (default 600)
            """
            if type(node_radius) != int:
                raise TypeError("The parameter node_radius must be an integer")
            if type(scr_width) != int or type(scr_height) != int:
                raise TypeError("The parameters scr_width and scr_height must be integers")
            if node_radius < 10 or node_radius > 100:
                raise ValueError("The parameter node_radius must be a value between 10 and 100")
            if scr_width < 200 or scr_height < 200:
                raise ValueError("The parameters scr_width and scr_height must be values greater than 200")
            if scr_width > 1000 or scr_height > 1000:
                raise ValueError("The parameters scr_width and scr_height must be values less than 1000")

            self.__ACTUAL_INSTANCE = instance
            self.__JSON_SAVE_DIR = os.path.join(os.path.dirname(__file__), 'save'+str(self.__ACTUAL_INSTANCE)+'.json')
            self.__graph = graph
            self.__node_radius = node_radius
            self.__scr_width = scr_width
            self.__scr_height = scr_height
            self.__XMARGIN = 7
            self.__YMARGIN = 7
            self.nodes = []
            self.edges = []

            # create the main window and start the GUI
            self.root = tk.Tk()
            self.root.title('GraphGUI')
            self.root.resizable(False, False)
            self.root.configure(bg="#87715f", border=0, width=self.__scr_width, height=self.__scr_height)

            # Closing protocol
            self.root.protocol("WM_DELETE_WINDOW", self.__on_closing)

            # Data recovery
            data = self.__get_data()

            # Create the canvas
            #self.canvas = tk.Canvas(self.root, width=scr_width, height=scr_height, bg="#c7b9a5")
            #self.canvas.pack(fill=tk.BOTH, expand=True, padx=7, pady=7)

            self.canvas = tk.Canvas(self.root, bg="#c7b9a5")
            self.canvas.place(x=self.__XMARGIN,
                              y=self.__YMARGIN,
                              width=self.__scr_width - self.__XMARGIN * 2,
                              height=self.__scr_height - self.__YMARGIN * 2 - 30)

            # Reset button
            self.reset_button = tk.Button(self.root, text="Reset", bg="#ede4cc", command=self.__display_reset)
            self.reset_button.place(x=self.__XMARGIN, y=self.__scr_height-self.__YMARGIN//2-30, width=60, height=30)

            # Config button
            self.reset_button = tk.Button(self.root, text="Load", bg="#ede4cc")
            self.reset_button.place(x=self.__XMARGIN + 60 + 7, y=self.__scr_height - self.__YMARGIN // 2 - 30, width=60,
                                    height=30)

            # Save button
            self.reset_button = tk.Button(self.root, text="Save", bg="#ede4cc")
            self.reset_button.place(x=self.__XMARGIN + 60 + 60 + 7 + 7, y=self.__scr_height - self.__YMARGIN // 2 - 30, width=60,
                                    height=30)

            # Main display
            self.__display(data)

            self.canvas.tag_bind("movil", "<ButtonPress-1>", self.on_press)
            self.canvas.tag_bind("movil", "<Button1-Motion>", self.move)
            self.selected_node = None

            self.root.mainloop()

        def __display_reset(self):
            for node in self.nodes:
                node.terminate()
            for edge in self.edges:
                edge.terminate()
            self.__display()

        def __display(self, data: dict = None):
            # Preparation for the nodes display
            scr_center = (self.__scr_width // 2, self.__scr_height // 2)
            display_radius = min(self.__scr_width, self.__scr_height) // 2 - self.__node_radius - 10
            arch_angle = 360 / len(self.__graph._vertices)
            first_node_pos = (scr_center[0] - self.__node_radius, scr_center[1] - self.__node_radius)

            # Display the nodes
            self.nodes = []
            i = 0
            angle = 0
            for vertex in self.__graph._vertices:
                if i == 0:
                    if data and vertex in data and data[vertex][0] < self.__scr_width and data[vertex][
                        1] < self.__scr_height - 30:
                        self.nodes.append(
                            Node(self.canvas, self.__node_radius, data[vertex][0], data[vertex][1], text=str(vertex)))
                    else:
                        self.nodes.append(
                            Node(self.canvas, self.__node_radius, first_node_pos[0], first_node_pos[1], text=str(vertex)))
                else:
                    if data and vertex in data and data[vertex][0] < self.__scr_width and data[vertex][
                        1] < self.__scr_height - 30:
                        self.nodes.append(
                            Node(self.canvas, self.__node_radius, data[vertex][0], data[vertex][1], text=str(vertex)))
                    else:
                        self.nodes.append(Node(self.canvas,
                                               self.__node_radius,
                                               int(scr_center[0] - self.__node_radius - display_radius * math.sin(
                                                   math.radians(angle))),
                                               int(scr_center[1] - self.__node_radius - display_radius * math.cos(
                                                   math.radians(angle))),
                                               text=str(vertex)))
                i += 1
                angle += arch_angle

            # Create the edges
            i = 0
            self.edges = []
            for vertex in self.__graph._vertices:
                for adj in self.__graph._vertices[vertex]:
                    for node in self.nodes:
                        if node.id == str(adj.vertex):
                            self.edges.append(Edge(self.canvas, self.nodes[i], node, adj.weight))
                            node.asociated_edges_IN.append(self.edges[-1])
                            self.nodes[i].asociated_edges_OUT.append(self.edges[-1])
                i += 1

            # Display the edges
            if self.__graph._directed:
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

            # Display author
            self.canvas.create_text(self.__scr_width // 2, self.__YMARGIN + 3, text="by @seniorbeto", fill="#695210",
                                    font=("Courier", 10))

        def __on_closing(self):
            data = {}
            for node in self.nodes:
                data[node.id] = (node.pos_x, node.pos_y)
            with open(self.__JSON_SAVE_DIR, "w", encoding="utf-8", newline="") as file:
                json.dump(data, file, indent=2)
            self.root.destroy()

        def __get_data(self):
            try:
                with open(self.__JSON_SAVE_DIR, "r", encoding="utf-8", newline="") as file:
                    data = json.load(file)
            except FileNotFoundError:
                data = None
            return data

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
                        overlaped = edge.overlaped
                        i.asociated_edges_IN.remove(edge)
                        self.canvas.delete(edge.line)
                        self.canvas.delete(edge.window)
                        del edge
                        edge = Edge(self.canvas, edge_start, i, weight, overlaped=overlaped)
                        edge.show()
                        i.asociated_edges_IN.append(edge)
                    for adj in self.__graph._vertices[i.id]:
                        for nd in self.nodes:
                            if nd.id == str(adj.vertex):
                                for edge in nd.asociated_edges_IN:
                                    if edge.start_node == i:
                                        edge_end = edge.end_node
                                        weight = edge.weight
                                        overlaped = edge.overlaped
                                        nd.asociated_edges_IN.remove(edge)
                                        self.canvas.delete(edge.line)
                                        self.canvas.delete(edge.window)
                                        del edge
                                        edge = Edge(self.canvas, i, edge_end, weight, overlaped=overlaped)
                                        edge.show()
                                        nd.asociated_edges_IN.append(edge)


            self.selected_node = (node, x, y)

class Node:
    def __init__(self, canvas: tk.Canvas, radius:int, posx: int, posy: int, text: str, bg: str = "White"):
        self.asociated_edges_IN = []
        self.asociated_edges_OUT = []
        self.canvas = canvas
        self.id = text
        self.radius = radius
        self.pos_x = posx
        self.pos_y = posy
        self.circle = canvas.create_oval(self.pos_x, self.pos_y, self.pos_x + self.radius*2, self.pos_y + self.radius*2, fill="#e3d7c5", width=2,)
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
    def __init__(self, canvas: tk.Canvas, start: Node, end: Node, weight: int = 1, overlaped: bool = False):
        self.canvas = canvas
        self.overlaped = overlaped
        self.start_node = start
        self.end_node = end
        self.weight = weight
        self.start = self.__calculate_start(start, end)
        self.end = self.__calculate_end(start, end)

    def terminate(self):
        self.canvas.delete(self.line)
        self.canvas.delete(self.window)

    def show(self):
        self.line = self.canvas.create_line(self.start[0], self.start[1], self.end[0], self.end[1], arrow=tk.LAST, width=1.5)
        if not self.overlaped:
            self.window = self.canvas.create_window((self.start[0] + self.end[0]) // 2, (self.start[1] + self.end[1]) // 2,
                                               window=tk.Label(self.canvas,bg="#c7b9a5" ,text=str(self.weight)))
        else:
            self.window = self.canvas.create_window((self.start[0] * 0.2 + self.end[0] * 0.8),
                                               (self.start[1] * 0.2 + self.end[1] * 0.8),
                                               window=tk.Label(self.canvas, bg="#c7b9a5", text=str(self.weight)))

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