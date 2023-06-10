"""
DESCRIPTION:
graphdisplay is a Python package for easy visualization of graphs and trees. It is built on top of the tkinter module,
and is designed to be easy to use and integrate into your own projects. It also includes graph and tree data structures
implementation based on the official Data Structures and Algorithms course at Carlos III University of Madrid.

It is an open source project fully developed by Alberto Penas Díaz, used under a MIT license at: https://github.com/seniorbeto/graphdisplay

USE EXAMPLES:

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

from .graphdisplay import GraphGUI
from .graphs import Graph
from .trees import AVLTree, BinarySearchTree

__all__ = ["GraphGUI",
           "Graph",
           "AVLTree",
           "BinarySearchTree"]

