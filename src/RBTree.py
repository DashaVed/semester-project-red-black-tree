class Node:
    """
    A class for nodes
    """

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

    def is_left_child(self):
        """check what kind of child node is"""
        return self.parent.left == self


class RBTree:

    """
    A basic class for red-black tree
    """

    def __init__(self):
        self.root = None
        self.size = 0

    def __setitem__(self, key, value):
        if self.root is None:
            self.root = Node(key, value, red=False)
        else:
            new_node = self.insert(key, value, self.root)
            self.check_color(new_node)
            self.root.red = False
        self.size += 1

    def insert(self, key, value, current_node):
        """Method fot inserting node"""
        if key < current_node.key:
            if current_node.has_left_child():
                return self.insert(key, value, current_node.left)
            current_node.left = Node(key, value, parent=current_node)
            return current_node.left
        if current_node.has_right_child():
            return self.insert(key, value, current_node.right)
        current_node.right = Node(key, value, parent=current_node)
        return current_node.right

    def check_color(self, node):
        """check violation"""
        if node == self.root or node is None:
            return
        if node.red is True and node.parent.red is True:
            self.correct_tree(node)
        return self.check_color(node.parent)

    def correct_tree(self, node):
        """
        if aunt is black: rotate
        if aunt is red: colorFlip
        """
        if node.parent.is_left_child():
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
            node.parent.parent.left.red = False
        node.parent.parent.red = True
        node.parent.red = False
        return

    def rotate(self, node):
        if node.is_left_child():
            if node.parent.is_left_child():
                self.right_rotate(node.parent.parent)
                node.red = True
                node.parent.red = False
                if node.parent.right is not None:
                    node.parent.right.red = True
                return
            self.rl_rotate(node.parent.parent)
            node.red = False
            node.right.red = True
            node.left.red = True
            return
        if node.parent.is_left_child():
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

    def __getitem__(self, key):
        """Return value by key"""
        if self.root is None:
            return None
        node = self.get(key, self.root)
        if node is None:
            return None
        return node.value

    def get(self, key, current_node):
        """recursive implementation of node search by key"""
        if current_node is None:
            return None
        if current_node.key == key:
            return current_node
        if key < current_node.key:
            return self.get(key, current_node.left)
        return self.get(key, current_node.right)

    def __delitem__(self, key):
        node = self.get(key, self.root)
        if node is not None:
            self.size -= 1
            self.remove(node)
            self.root.red = False
            if self.black_height(self.root):
                return
            else:
                print('error')
        return None

    def remove(self, node):
        """Method for removing node"""
        if node is None:
            return
        if node.red:
            # удаление красного узла с двумя детьми
            if node.left is not None and node.right is not None:
                min_right = self.min_in_right(node.right)
                max_left = self.max_in_left(node.left)
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
            else:
                node.parent.right = None
            self.fix_delete(node.parent)
            return
        # удаление черного узла с двумя детьми
        else:
            min_right = self.min_in_right(node.right)
            max_left = self.max_in_left(node.left)
            if min_right.left is not None or min_right.right is not None:
                self.swap(node, min_right)
                return self.remove(min_right)
            self.swap(node, max_left)
            return self.remove(max_left)

    def fix_delete(self, node):
        """correct tree after deleting"""
        if node is None:
            return
        if node.red:
            if node.left is None:
                # КЧ2
                if node.right.right is not None and node.right.right.red is True:
                    self.left_rotate(node)
                    node.red = False
                    node.parent.red = True
                    node.parent.right.red = False
                    return
                # КЧ1
                if node.right.left is None or node.right.left.red is False:
                    node.red = False
                    node.right.red = True
                    return
            # КЧ2 зеркально
            if node.left.left is not None and node.left.left.red is True:
                self.right_rotate(node)
                node.red = False
                node.parent.red = True
                node.parent.left.red = False
                return
            # КЧ1 зеркально
            if node.left.right is None or node.left.right.red is False:
                node.red = False
                node.left.red = True
                return
        if node.right is None:
            if node.left.red is True:
                #ЧК3
                if node.left.right.left is None or node.left.right.left.red is False:
                    self.right_rotate(node)
                    node.parent.red = False
                    node.left.red = True
                    return
                #ЧК4
                self.lr_rotate(node)
                node.parent.left.right.red = False
                return
            #ЧЧ6
            if node.left.right is None or node.left.right.red is  False:
                node.left.red = True
                return self.fix_delete(node.parent)
            # ЧЧ5
            self.lr_rotate(node)
            node.parent.red = True
            node.red = False
            return
        if node.right.red is True:
            # ЧК3 зеркально
            if node.right.left.right is None or node.right.left.right.red is False:
                self.left_rotate(node)
                node.parent.red = False
                node.right.red = True
                return
            # ЧК4 зеркально
            self.rl_rotate(node)
            node.parent.right.left.red = False
            return
        # ЧЧ6 зеркально
        if node.right.left is None or node.right.left.red is False:
            node.right.red = True
            return self.fix_delete(node.parent)
        # ЧЧ5 зеркально
        self.rl_rotate(node)
        node.parent.red = True
        node.red = False
        return

    @staticmethod
    def swap(node1, node2):
        """change key, value between two nodes"""
        temporary_node = node1
        node1.key, node1.value = node2.key, node2.value
        node2.key, node2.value = temporary_node.key, temporary_node.value

    @staticmethod
    def min_in_right(node):
        """finding the minimum node in the right subtree"""
        while node.left is not None:
            node = node.left
        return node

    @staticmethod
    def max_in_left(node):
        """finding the maximum node in the left subtree"""
        while node.right is not None:
            node = node.right
        return node

    def left_rotate(self, node):
        temporary_node = node.right
        node.right = temporary_node.left
        if node.right is not None:
            node.right.parent = node
        if node.parent is None:
            self.root = temporary_node
            temporary_node.parent = None
        else:
            temporary_node.parent = node.parent
            if node.is_left_child():
                temporary_node.parent.left = temporary_node
            else:
                temporary_node.parent.right = temporary_node
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
            if node.is_left_child():
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

    def black_height(self, node):
        """number of black nodes"""
        if node is None:
            return 1
        right_black = self.black_height(node.right)
        left_black = self.black_height(node.left)
        if right_black != left_black:
            return False
        if node.red is False:
            left_black += 1
        return True

    def print_tree(self):
        """Function to call print method"""
        print(self.root.key)
        self.__print_call(self.root, "", True)

    def __print_call(self, node, indent, last):
        """Function to print a tree"""
        if node is not None:
            print(indent, end=' ')
            if last:
                print("R----", end=' ')
                indent += "     "
            else:
                print("L----", end=' ')
                indent += "|    "

            s_color = "RED" if node.red else "BLACK"
            print(str(node.key) + "(" + s_color + ")")
            self.__print_call(node.left, indent, False)
            self.__print_call(node.right, indent, True)


if __name__ == "__main__":
    rb_tree = RBTree()

    rb_tree[5] = 0
    rb_tree[2] = 0
    rb_tree[7] = 0
    rb_tree[8] = 0
    rb_tree[10] = 0
    rb_tree[6] = 0
    rb_tree.print_tree()

    print("\nAfter deleting an element")
    del rb_tree[10]
    rb_tree.print_tree()
