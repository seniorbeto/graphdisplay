# -*- coding: utf-8 -*-
# Implementation of Binary Tree


class BinaryNode:

    def __init__(self, elem: object, node_left: 'BinaryNode' = None, node_right: 'BinaryNode' = None) -> None:
        self.elem = elem
        self.left = node_left
        self.right = node_right

    def __eq__(self, other: 'BinaryNode') -> bool:
        """checks if two nodes (subtrees) are equal o not"""
        return other is not None and self.elem == other.elem and self.left == other.left and self.right == other.right

    def __str__(self):
        return str(self.elem)


class BinaryTree:
    def __init__(self) -> None:
        """creates an empty binary trees
        I only has an attribute: _root"""
        self._root = None

    def __eq__(self, other: 'BinaryTree') -> bool:
        """checks if two binary trees are equal o not"""
        return other is not None and self._root == other._root

    def size(self) -> int:
        """Returns the number of nodes"""
        return self._size(self._root)

    def _size(self, node: BinaryNode) -> int:
        """return the size of the subtree from node"""
        if node is None:
            return 0
        else:
            return 1 + self._size(node.left) + self._size(node.right)

    def height(self) -> int:
        """Returns the height of the trees"""
        return self._height(self._root)

    def _height(self, node: BinaryNode) -> int:
        """return the height of node"""
        if node is None:
            return -1
        else:
            return 1 + max(self._height(node.left), self._height(node.right))

    def preorder(self) -> None:
        """prints the preorder (root, left, right) traversal of the trees"""
        # self.draw()
        print('Preorder traversal: ', end=' ')  # end=' ' avoid the newline
        self._preorder(self._root)
        print()

    def _preorder(self, node: BinaryNode) -> None:
        """prints the preorder (root, left, right) traversal of the subtree
        than hangs from node"""
        if node is not None:
            print(node.elem, end=' ')  # end=' ' avoid new line
            self._preorder(node.left)
            self._preorder(node.right)

    def preorder_list(self) -> list:
        """returns a list with the preorder traversal"""
        # self.draw()
        result = []
        self._preorder_list(self._root, result)
        return result

    def _preorder_list(self, node: BinaryNode, pre_list: list) -> None:
        """populates pre_list with the preorder traversal of the subtree node"""
        if node is not None:
            pre_list.append(node.elem)
            self._preorder_list(node.left, pre_list)
            self._preorder_list(node.right, pre_list)

    def postorder(self) -> None:
        """prints the postorder (left, right, root)  traversal of the trees"""
        # self.draw()
        print('Postorder traversal: ', end=' ')  # end=' ' avoid the newline
        self._postorder(self._root)
        print()

    def _postorder(self, node: BinaryNode) -> None:
        """prints the postorder (left, right, root) traversal of the subtree
        than hangs from node"""
        if node is not None:
            self._postorder(node.left)
            self._postorder(node.right)
            print(node.elem, end=' ')  # end=' ' avoid new line

    def postorder_list(self) -> list:
        """returns a list with the postorder traversal of the trees"""
        # self.draw()
        result = []
        self._postorder_list(self._root, result)
        return result

    def _postorder_list(self, node: BinaryNode, post_list: list) -> None:
        """populates post_list with the postorder traversal of the subtree node"""
        if node is not None:
            self._postorder_list(node.left, post_list)
            self._postorder_list(node.right, post_list)
            post_list.append(node.elem)

    def inorder(self) -> None:
        """prints the inorder (left, root, right)  traversal of the trees"""
        # self.draw()
        print('Inorder traversal: ', end=' ')  # end=' ' avoid the newline
        self._inorder(self._root)
        print()

    def _inorder(self, node: BinaryNode) -> None:
        """prints the inorder (left, root, right) traversal of the subtree
        than hangs from node"""
        if node is not None:
            self._inorder(node.left)
            print(node.elem, end=' ')  # end=' ' avoid new line
            self._inorder(node.right)

    def inorder_list(self) -> list:
        """returns a list with the inorder traversal of the trees"""
        # self.draw()
        result = []
        self._inorder_list(self._root, result)
        return result

    def _inorder_list(self, node: BinaryNode, in_list: list) -> None:
        """populates in_list with the inorder traversal of the subtree node"""
        if node is not None:
            self._postorder_list(node.left, in_list)
            in_list.append(node.elem)
            self._postorder_list(node.right, in_list)



    def draw(self) -> None:
        """function to draw a trees. """
        if self._root:
            self._draw('', self._root, False)
        else:
            print('trees is empty')
        print('\n\n')

    def _draw(self, prefix: str, node: BinaryNode, is_left: bool) -> None:
        if node is not None:
            self._draw(prefix + "     ", node.right, False)
            print(prefix + "|-- " + str(node.elem))
            self._draw(prefix + "     ", node.left, True)


if __name__ == '__main__':
    pass