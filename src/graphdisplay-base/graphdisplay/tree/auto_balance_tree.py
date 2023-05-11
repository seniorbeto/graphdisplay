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
        #  Se pasan de abajo a arriba los nodos del árbol desde el que se inserta
        #  para equilibrarlos con la función si estuvieran desequilibrados
        node = self._rebalance(node)

        return node

    # Override remove method from base class to keep it as AVL
    def remove(self, elem: object) -> None:
        self._root = self._remove(self._root, elem)

    def _remove(self, node: BinaryNode, elem: object) -> BinaryNode:
        """ gets a node, searches the node with element elem in the subtree that hangs down node , and
        then remove this node (using super()._remove). After this, the function has to balance the node returned by the function super()._remove"""

        node = super()._remove(node, elem)
        #  Se pasa a la función de equilibrado los nodos del árbol de abajo a arriba
        #  desde el que se elimina
        node = self._rebalance(node)

        return node

    def _rebalance(self, node: BinaryNode) -> BinaryNode:
        """ gets node and CHECKS IF IT IS NEEDED TO balances it"""
        #  La función 'remove' pasa como resultado de su primera llamada
        #  recursiva 'None' (al eliminar el nodo). Si node es 'None' lo devolvemos
        if node:
            #  Si el factor de equlibrio >= 2, entonces el nodo está desequilibrado
            if abs(self._height(node.right) - self._height(node.left)) >= 2:
                #  Para equilibrarlo, identificamos la forma del desequilibro
                #  y efectuamos la rotación más adecuada

                #  Desequilibrio por la derecha
                if self._height(node.right) > self._height(node.left):
                    #  Desequilibrio derecha-izquierda ('zigzag')
                    if self._height(node.right.left) > self._height(node.right.right):
                        #  Doble rotación derecha-izquierda
                        node = self.__R_right_left(node)
                    #  Desequilibrio derecha-derecha
                    else:
                        #  Rotación simple izquierda
                        node = self.__R_left(node)
                #  Análogo en la izquierda
                else:
                    if self._height(node.left.right) > self._height(node.left.left):
                        node = self.__R_left_right(node)
                    else:
                        node = self.__R_right(node)
        #  Devolvemos el nodo con sus cambios
        return node

    #  Método privado: si fuera público, un usuario podría desequilibrar el árbol
    def __R_right(self, node: BinaryNode) -> BinaryNode:
        """
        Recibe un nodo y lo rota a la derecha. Devuelve el nodo que estará en su lugar
        """

        #  El padre ahora tendrá como hijo el hijo izquierdo de 'node'
        pivote = node.left
        #  El hijo derecho del hijo izquierdo (pivote.right) será el hijo izquierdo
        #  de 'node'
        node.left = pivote.right
        #  El hijo derecho del hijo izquierdo, ahora será 'node'
        pivote.right = node
        #  Si se rota la raíz cambiamos el atributo
        if node == self._root:
            self._root = pivote
        return pivote

    def __R_left(self, node: BinaryNode) -> BinaryNode:
        """
        Recibe un nodo y lo rota a la izquierda. Devuelve el nodo que estará en su lugar
        """
        #  Análogo a "__R_right()"
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
        #  Rotamos primero a la derecha su nodo derecho, porque crea un
        #  desequilibrio por su izquierda. El nuevo hijo derecho de 'node', será
        #  el resultante de la rotación
        node.right = self.__R_right(node.right)
        #  Sobre el nodo (ahora solo con desequilibrio derecha-derecha) efectuamos
        #  rotación izquierda
        return self.__R_left(node)

    def __R_left_right(self, node: BinaryNode) -> BinaryNode:
        """
        Doble rotación izquierda-derecha. Devuelve el nodo que estará en su lugar
        """
        #  Análogo a "__R_left_right()"
        node.left = self.__R_left(node.left)
        return self.__R_right(node)