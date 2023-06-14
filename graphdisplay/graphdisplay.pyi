# Coding: utf-8
"""
DESCRIPTION:
------------
graphdisplay is a Python package for easy visualization of graphs and trees. It is built on top of the tkinter module,
and is designed to be easy to use and integrate into your own projects. It also includes graph and tree data structures
implementation based on the official Data Structures and Algorithms course at Carlos III University of Madrid.

It is an open source project fully developed by Alberto Penas Díaz, used under a MIT license at: https://github.com/seniorbeto/graphdisplay

USE EXAMPLES:
-------------
1.->
    from graphdisplay import GraphGUI, Graph

    labels = ['A', 'B', 'C', 'D', 'E']
    g = Graph(labels)

    # Now, we add the edges
    g.add_edge('A', 'C', 12)  # A->(12)C
    g.add_edge('A', 'D', 60)  # A->(60)D
    g.add_edge('B', 'A', 10)  # B->(10)A
    g.add_edge('C', 'B', 20)  # C->(20)B
    g.add_edge('C', 'D', 32)  # C->(32)D
    g.add_edge('E', 'A', 7)   # E->(7)A

    GraphGUI(g)

2.->
    from graphdisplay import BinarySearchTree, GraphGUI
    from random import randint

    tree = BinarySearchTree()
    for i in range(100):
        tree.insert(randint(1, 1000))

    GraphGUI(tree)
"""
from typing import Any, Tuple, Dict, List, Callable
from .trees.binary_tree import BinaryNode, BinaryTree
from .graphs import Graph
import tkinter as tk


def measure_time(func: Callable) -> Callable:
    """
    Decorator function to measure the time of a function.

    Parameters
    ----------
    func : Any
        The function to be decorated.

    Returns
    -------
    Any
        The decorated function.
    """
    ...

class GraphGUI:
    """
    Main class that creates a GraphGUI object, which will display the graph in an external window. Nodes can be moved with the mouse.
    For full documentation, please visit: https://github.com/seniorbeto/graphdisplay


    Parameters
    ----------
    graph : Any
        The graph to be displayed.

    Raises
    ------
    Exception
        If more than 5 instances of GraphGUI have been generated.
    RecursionError
        If, while displaying a tree-like graph, the recursion limit is reached.
    RuntimeError
        For how multiprocessing works in python, it doesn't allow generating multiple processes
        without using a "if __name__ == "__main__":" statement. By implementing a try/expect, we
        can temporarily deal with this issue. Nevertheless, by doing this, there is a high chance
        to run into code-duplication and zombie processes generations. This raises a RuntimeError
        exception, but since it is not a critical error, it is shown as a warning and the program
        runs normally.

    Returns
    -------
    GraphGUI.__GraphGUI : Any
        The GraphGUI object.
    """
    def __new__(cls: type, graph: Any) -> None:...
    def __getattr__(self, name: Any) -> Any: ...
    def __setattr__(self, name: Any, value: Any) -> None: ...
    @staticmethod
    def _generate(graph: Any, instance: int) -> GraphGUI.__GraphGUI: ...

    class __GraphGUI:
        """
        Creates a GraphGUI object, which will display the graph in an external window. Nodes can be moved with the mouse.

        Parameters
        ----------
        graph : Any
            The graph to be displayed.
        instance : int
            The instance number of the graph to be displayed.

        Attributes
        ----------
        root : tk.Tk
            The root window of the GraphGUI object.
        json_manager: JsonManager
            The JsonManager object associated to the GraphGUI object.
        __ACTUAL_INSTANCE : int
            The instance number of the graph to be displayed.
        _graph : Graph | BinaryTree
            The graph to be displayed.
        __node_radius : int
            The radius of the nodes in the canvas.
        __scr_width : int
            The width of the screen.
        __scr_height : int
            The height of the screen.
        __XMARGIN : int
            The margin of the canvas in the x axis.
        __YMARGIN : int
            The margin of the canvas in the y axis.
        _theme : str
            The theme of the canvas.
        nodes : dict[Any, Node]
            The dictionary of nodes in the canvas.
        edges : list[Edge]
            The list of edges in the canvas.
        __canvas_node_relation : dict[int, Node]
            The dictionary of nodes in the canvas related to their tkinter-canvas id.
        _is_tree : bool
            True if the graph is a tree, False otherwise.
        __canvas_frame : tk.Frame
            The frame where the canvas is displayed.
        canvas : tk.Canvas
            The canvas where the graph is displayed.
        """
        def __init__(self, graph: Any, instance: int) -> None: ...
        def set_colors(self, theme: str) -> None: ...
        def __menu_display(self) -> None: ...
        def __call_tools_window(self) -> None: ...
        def __call_about_window(self) -> None: ...
        def __call_manager_config(self) -> None: ...
        def __call_manager_delete(self) -> None: ...
        def __call_manager_load(self) -> None: ...
        def __call_manager_save(self) -> None: ...
        def get_current_position(self) -> dict[Any, tuple[int, int]]: ...
        def display_reset(self, new_data: dict[Any, tuple[int, int]] | None = None) -> None: ...
        def __display(self, data: dict[Any, tuple[int, int]] | None = None) -> None:
            """
            Main display for all nodes in the canvas, whose position is determined in "data".
            If data is None, the default display will be showed. This is, in case of a simple graph,
            the first vertex in the middle of the screen and the rest surrounding it in a polygon shape.
            In case of a tree, it is always display in a tree-like structure.

            This function also checks if some node position has been stored outside the frames of the window,
            in which case will correct.
            """
            pass
        def __get_children(self, elem: Any) -> Tuple[Any, Any]: ...
        def __search_node(self, elem: Any) -> BinaryNode: ...
        def __search_node_aux(self, node: BinaryNode, elem: Any) -> BinaryNode: ...
        def __levelorder(self, node: BinaryNode) -> dict[Any, int]: ...
        def __on_closing(self) -> None: ...
        def on_press_left(self, event: tk.Event) -> None: ...
        def on_press(self, event: tk.Event) -> None: ...
        def move(self, event: tk.Event) -> Node:
            """
            It moves a node if it has been selected on the right mouse click protocol. After moving it, it updates
            automatically the coordenates of all edges attached to the node. Returns the node that has been moved.
            """
            ...
        def set_node_radius(self, value: int) -> None: ...

class Node:
    """
    Node class representing a vertex in the graph or tree GUI. It stores the canvas object of the node, the radius,
    the position, the text and all the edges associated to it (dividing them into two list so that it can be determined
    which of those vertices are pointing IN or OUT of the vertex).

    Parameters
    ----------
    canvas : tk.Canvas
        The canvas object where the node will be displayed.
    radius : int
        The radius of the node.
    posx : int
        The x coordinate of the node.
    posy : int
        The y coordinate of the node.
    text : str
        The text to be displayed in the node.
    bg : str, optional
        The background color of the node. The default is "white".

    Raises
    ------
    TypeError
        If the canvas object is not a tk.Canvas object, the radius not an integer (or < 0)
        or posx or posy are not integers.

    Attributes
    ----------
    __canvas: tk.Canvas
        The canvas object where the node will be displayed.
    __id: Any
        The id of the node in the canvas.
    __radius: int
        The radius of the node.
    __posx: int
        The x coordinate of the node.
    __posy: int
        The y coordinate of the node.
    __circle: int
        the tkinter-canvas id of the circle representing the node.
    __text: int
        the tkinter-canvas id of the text shown inside the node.
    associated_edges_IN: List[Edge]
        The list of edges pointing IN to the node.
    associated_edges_OUT: List[Edge]
        The list of edges pointing OUT of the node.
    """
    ...

    def __init__(self, canvas: tk.Canvas,
                 radius: int,
                 posx: int,
                 posy: int,
                 text: str,
                 bg: str = "white") -> None: ...
    def terminate(self) -> None: ...
    def __str__(self) -> str: ...


class Edge:
    """
    Class representing an edge between two nodes that have been already created in the canvas of the GraphGUI.
    The weight of the edge will be shown in the middle of the edge. The overlapped parameter is used to
    determine if the edge will be overlapped by the nodes or not, if it is, the weight will be shown in the rightmost
    side of the edge. The window_color parameter is used to determine the background color of the weight canvas label.

    Parameters
    ----------
    canvas : tk.Canvas
        The canvas object where the edge will be displayed.
    start : Node
        The node where the edge starts.
    end : Node
        The node where the edge ends.
    weight : Any | None
        The weight of the edge. If None, the weight will not be shown.
    overlapped : bool, optional
        Boolean value to determine if the edge will be overlapped by the nodes or not. The default is False.
    window_color : str, optional
        The background color of the weight canvas label. The default is "white".
    text_color : str, optional
        The text color of the weight canvas label. The default is "black".

    Raises
    ------
    TypeError
        If the canvas object is not a tk.Canvas object or start or end are not Node objects.

    Attributes
    ----------
    __canvas: tk.Canvas
        The canvas object where the edge will be displayed.
    __start_node: Node
        The node where the edge starts.
    __end_node: Node
        The node where the edge ends.
    __weight: Any | None
        The weight of the edge. If None, the weight will not be shown.
    overlapped: bool
        Boolean value to determine if the edge will be overlapped by the nodes or not.
    __window_color: str
        The background color of the weight canvas label.
    __text_color: str
        The text color of the weight canvas label.
    __start: tuple[int, int]
        The position of the start node.
    __end: tuple[int, int]
        The position of the end node.

    """

    def __init__(self, canvas: tk.Canvas,
                 start: Node,
                 end: Node,
                 weight: int = 1,
                 overlapped: bool = False,
                 window_color: str = "white",
                 text_color: str = "black") -> None:
        ...
    def __str__(self)-> str: ...
    def update_position(self) -> None: ...
    def terminate(self) -> None: ...
    def show(self) -> None: ...
    def __recalculate(self) -> None: ...
    def __get_displacement(self) -> tuple[int, int, int, int]: ...
    def __calculate_start(self, start: Node, end: Node) -> tuple[int, int]: ...
    def __calculate_end(self, start: Node, end: Node) -> tuple[int, int]: ...
