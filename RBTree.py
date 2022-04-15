class Node:

    def __init__(self, key, value, red=True, left=None, right=None, parent=None):
        self.key = key
        self.value = value
        self.red = red
        self.left = left
        self.right = right
        self.parent = parent

    def has_left_child(self):
        """return left child"""
        return self.left

    def has_right_child(self):
        """return right child"""
        return self.right

    def isLeftChild(self):
        """check what kind of child node is"""
        return self.parent.left == self


class RBTree:

    def __init__(self):
        self.root = None
        self.size = 0

    def __setitem__(self, key, value):
        if self.root is None:
            self.root = Node(key, value, red=False)
        else:
            new_node = self.insert(key, value, self.root)
            self.check_color(new_node)
        self.size += 1

    def __getitem__(self, key):
        """Return value by key"""
        if self.root is None:
            return None
        node = self.get(key, self.root)
        if node is None:
            raise KeyError
        return node.value

    def __delitem__(self, key):
        node = self.get(key, self.root)
        if node is not None:
            return self.remove(node)
        raise KeyError

    def insert(self, key, value, current_node):
        if key < current_node.key:
            if current_node.has_left_child():
                return self.insert(key, value, current_node.left)
            else:
                current_node.left = Node(key, value, parent=current_node)
                return current_node.left
        else:
            if current_node.has_right_child():
                return self.insert(key, value, current_node.right)
            else:
                current_node.right = Node(key, value, parent=current_node)
                return current_node.right

    def get(self, key, current_node):
        """recursive implementation of node search by key"""
        if current_node is None:
            return None
        if current_node.key == key:
            return current_node
        if key < current_node.key:
            return self.get(key, current_node.left_child)
        return self.get(key, current_node.right_child)

    def remove(self, node):
        if node is None:
            raise KeyError
        if node.red:
            # удаление красного узла с двумя детьми
            if node.has_left_child():
                min_right = self.min_in_right(node)
                max_left = self.max_in_left(node)
                if min_right.red:
                    self.swap(node, min_right)
                    return self.remove(min_right)
                self.swap(node, max_left)
                return self.remove(max_left)
            # удаление красного узла без детей
            if node.isLeftChild():
                node.parent.left = None
            node.parent.right = None
            return
        # удаление черного узла с правым ребенком
        if node.left is None and node.right is not None:
            node.key, node.value = node.right.key, node.right.value
            node.right = None
            return
        # удаление черного узла с левым ребенком
        elif node.left is not None and node.right is None:
            node.key, node.value = node.left.key, node.left.value
            node.left = None
            return
        # удаление черного узла без детей
        elif node.left is None and node.right is None:
            if node.isLeftChild():
                node.parent.left = None
            node.parent.right = None
            self.correct_tree(node.parent)
            return
        # удаление черного узла с двумя детьми
        min_right = self.min_in_right(node)
        max_left = self.max_in_left(node)
        if min_right.left is not None or min_right.right is not None:
            self.swap(node, min_right)
            return self.remove(min_right)
        self.swap(node, max_left)
        return self.remove(max_left)

    @staticmethod
    def swap(node1, node2):
        temporary_node = node1
        node1.key, node1.value = node2.key, node2.value
        node2.key, node2.value = temporary_node.key, temporary_node.value

    @staticmethod
    def min_in_right(node):
        while node.left is not None:
            node = node.left
        return node

    @staticmethod
    def max_in_left(node):
        while node.right is not None:
            node = node.right
        return node

    def check_color(self, node):
        if node == self.root:
            return
        if node.red is True and node.parent.red is True:
            self.correct_tree(node)
        return self.check_color(node.parent)

    def correct_tree(self, node):
        """
        if aunt is black: rotate
        if aunt is red: colorFlip
        """
        if node.parent.isLeftChild():
            # aunt is node.grandparent.right
            if node.parent.parent.right is None or node.parent.parent.right.red is False:
                return self.rotate(node)
            # color flip
            if node.parent.parent.right is not None:
                node.parent.parent.right.red = False
            node.parent.parent.red = True
            node.parent.red = False
            return
        # aunt is node.grandparent.left
        if node.parent.parent.left is None or node.parent.parent.left.red is False:
            return self.rotate(node)
        if node.parent.parent.left is not None:
            node.parent.parent.right.red = False
        node.parent.parent.red = True
        node.parent.red = False
        return

    def rotate(self, node):
        if node.isLeftChild():
            if node.parent.isLeftChild():
                self.right_rotate(node.parent.parent)
                node.red = True
                node.parent.red = False
                if node.parent.right is not None:
                    node.parent.right.red = True
                return
            self. rl_rotate(node.parent.parent)
            node.red = False
            node.right.red = True
            node.left.red = True
            return
        if node.parent.isLeftChild():
            self.lr_rotate(node.parent.parent)
            node.red = False
            node.right.red = True
            node.left.red = True
            return
        self.left_rotate(node.parent.parent)
        node.red = True
        node.parent.red = False
        if node.parent.left is not None:
            node.parent.left.red = True
        return

    def left_rotate(self, node):
        temporary_node = node.right
        node.right = temporary_node.left
        if node.right is not None:
            node.right.parent = node
        if node == self.root:
            self.root = temporary_node
            temporary_node.parent = None
        else:
            temporary_node.parent = node.parent
            if node.isLeftChild():
                node.parent.left = temporary_node
            else:
                node.parent.right = temporary_node
        temporary_node.left = node
        node.parent = temporary_node

    def right_rotate(self, node):
        temporary_node = node.left
        node.left = temporary_node.right
        if node.left is not None:
            node.left.parent = node
        if node == self.root:
            self.root = temporary_node
            temporary_node.parent = None
        else:
            temporary_node.parent = node.parent
            if node.isLeftChild():
                node.parent.left = temporary_node
            else:
                node.parent.right = temporary_node
        temporary_node.right = node
        node.parent = temporary_node

    def rl_rotate(self, node):
        self.right_rotate(node.right)
        self.left_rotate(node)

    def lr_rotate(self, node):
        self.left_rotate(node.left)
        self.right_rotate(node)



