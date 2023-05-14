"""
Implementation of an Auto Balanced Tree by Alberto Penas Díaz (https://github.com/seniorbeto) and
Natalia Rodríguez Navarro (https://github.com/NataaNK) for the subject Data Structures and Algorithms 2021.
University of Carlos III de Madrid.
"""
from .binary_search_tree import BinarySearchTree
from .binary_search_tree import BinaryNode


class AVLTree(BinarySearchTree):

    # Override insert method from base class to keep it as AVL
    def insert(self, elem: object) -> None:
        """inserts a new node, with key and element elem"""
        self._root = self._insert(self._root, elem)

    def _insert(self, node: BinaryNode, elem: object) -> BinaryNode:
        """gets a node, searches the place to insert a new node with element e (using super()._insert),  and then,
        the function has to balance the node returned by the function super.()_insert"""

        node = super()._insert(node, elem)
        node = self._rebalance(node)

        return node

    # Override remove method from base class to keep it as AVL
    def remove(self, elem: object) -> None:
        self._root = self._remove(self._root, elem)

    def _remove(self, node: BinaryNode, elem: object) -> BinaryNode:
        """ gets a node, searches the node with element elem in the subtree that hangs down node , and
        then remove this node (using super()._remove). After this, the function has to balance the node returned by the function super()._remove"""

        node = super()._remove(node, elem)
        node = self._rebalance(node)

        return node

    def _rebalance(self, node: BinaryNode) -> BinaryNode:
        """ gets node and CHECKS IF IT IS NEEDED TO balances it"""
        if node:
            if abs(self._height(node.right) - self._height(node.left)) >= 2:
                if self._height(node.right) > self._height(node.left):
                    if self._height(node.right.left) > self._height(node.right.right):
                        node = self.__R_right_left(node)
                    else:
                        node = self.__R_left(node)
                else:
                    if self._height(node.left.right) > self._height(node.left.left):
                        node = self.__R_left_right(node)
                    else:
                        node = self.__R_right(node)
        return node

    def __R_right(self, node: BinaryNode) -> BinaryNode:
        """
        Recibe un nodo y lo rota a la derecha. Devuelve el nodo que estará en su lugar
        """
        pivote = node.left
        node.left = pivote.right
        pivote.right = node
        if node == self._root:
            self._root = pivote
        return pivote

    def __R_left(self, node: BinaryNode) -> BinaryNode:
        """
        Recibe un nodo y lo rota a la izquierda. Devuelve el nodo que estará en su lugar
        """
        pivote = node.right
        node.right = pivote.left
        pivote.left = node
        if node == self._root:
            self._root = pivote
        return pivote

    def __R_right_left(self, node: BinaryNode) -> BinaryNode:
        """
        Doble rotación derecha-izquierda. Devuelve el nodo que estará en su lugar
        """
        node.right = self.__R_right(node.right)
        return self.__R_left(node)

    def __R_left_right(self, node: BinaryNode) -> BinaryNode:
        """
        Doble rotación izquierda-derecha. Devuelve el nodo que estará en su lugar
        """
        node.left = self.__R_left(node.left)
        return self.__R_right(node)