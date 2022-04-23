import unittest
from src.RBTree import RBTree


class RBTreeTest(unittest.TestCase):
    """
    A basic class
    """
    def setUp(self) -> None:
        self.rb_tree = RBTree()

    def tearDown(self) -> None:
        pass

        # ***************TEST DELETIONS***************

    def test_deletion_root(self):
        self.rb_tree[5] = 0
        self.rb_tree[3] = 0
        self.rb_tree[8] = 0
        """
      REMOVE--> __5__                     __8B__
               /     \     --Result-->   /
             3R      8R                3R
        """
        del self.rb_tree[5]

        node_8 = self.rb_tree.root
        self.assertEqual(node_8.key, 8)
        self.assertFalse(node_8.red)
        self.assertEqual(node_8.parent, None)
        self.assertEqual(node_8.left.key, 3)
        self.assertEqual(node_8.right, None)
        node_3 = node_8.left
        self.assertTrue(node_3.red)
        self.assertEqual(node_3.parent, node_8)
        self.assertEqual(node_3.left, None)
        self.assertEqual(node_3.right, None)

    def test_deletion_root_2_nodes(self):
        self.rb_tree[5] = 0
        self.rb_tree[8] = 0
        """
                __5B__ <-- REMOVE        __8B__
                     \      Should become--^
                     8R
        """
        del self.rb_tree[5]

        root = self.rb_tree.root
        self.assertEqual(root.key, 8)
        self.assertEqual(root.parent, None)
        self.assertEqual(root.red, False)
        self.assertEqual(root.left, None)
        self.assertEqual(root.right, None)

    def test_delete_single_red_node(self):
        self.rb_tree[20] = 0
        self.rb_tree[10] = 0
        self.rb_tree[5] = 0
        self.rb_tree[15] = 0
        """
                ___10___
               /         \
             5B          20B
                        /
                     15R <--- REMOVE
        """
        del self.rb_tree[15]
        node_20 = self.rb_tree.get(20, self.rb_tree.root)
        self.assertEqual(node_20.left, None)
        self.assertFalse(node_20.red)
        self.assertEqual(self.rb_tree.size, 3)
        self.assertIsNone(self.rb_tree[15])  # assure its not in the tree

    def test_deletion_red_node_with_two_children(self):
        self.rb_tree[10] = 0
        self.rb_tree[5] = 0
        self.rb_tree[-5] = 0
        self.rb_tree[7] = 0
        self.rb_tree[35] = 0
        self.rb_tree[20] = 0
        self.rb_tree[38] = 0
        self.rb_tree[36] = 0

        del self.rb_tree[35]

        """
                    10B
                  /     \
                5R       35R   <-- REMOVE THIS
               /  \     /   \
            -5B   7B   20B  38B   We get it's in-order successor, which is 36
                           /
                          36R     36 Is red and has no children, so we easily swap it's value with 35 and remove 36
                      10B
                    /     \
     RESULT IS    5R       36R
                 /  \     /   \
              -5B   7B   20B  38B
        """

        node_10 = self.rb_tree.root
        self.assertEqual(node_10.key, 10)
        self.assertEqual(node_10.right.key, 36)
        node_36 = node_10.right
        self.assertEqual(node_36.parent, self.rb_tree.root)
        self.assertEqual(node_36.left.key, 20)
        self.assertEqual(node_36.right.key, 38)
        node_20 = node_36.left
        node_38 = node_36.right
        self.assertEqual(node_20.parent.key, 36)
        self.assertEqual(node_38.parent.key, 36)
        self.assertEqual(node_38.left, None)

    def test_deletion_black_node_black_successor_no_child_case_4(self):
        self.rb_tree[10] = 0
        self.rb_tree[-10] = 0
        self.rb_tree[30] = 0
        self.rb_tree[20] = 0
        self.rb_tree[38] = 0
        del self.rb_tree[10]

        """
                  ___10B___   <----- REMOVE THIS       ___20B___
                 /         \                          /         \
               -10B        30B                      -10B        30B
                          /   \                                    \
         successor --> 20R    38R                                  38R
        """

        self.assertEqual(self.rb_tree.size, 4)
        self.assertTrue(self.rb_tree.black_height(self.rb_tree.root))

    def test_black_node_no_children_case5(self):
        #ЧЧ5
        self.rb_tree[10] = 0
        self.rb_tree[-10] = 0
        self.rb_tree[30] = 0
        self.rb_tree[20] = 0
        self.rb_tree[38] = 0
        del self.rb_tree[-10]
        """
                          ___10B___               after:       ___10B___
                         /         \                          /         \
                       -10B        30B                      -10B        30B
                                  /   \                                    \
                    remove --> 20R    38R                                  38R
        """
        self.assertTrue(self.rb_tree.black_height(self.rb_tree.root))

    def test_black_node_no_children_case(self):
        # КЧ2 сведенный к ЧЧ5
        self.rb_tree[5] = 0
        self.rb_tree[6] = 0
        self.rb_tree[2] = 0
        self.rb_tree[8] = 0
        self.rb_tree[10] = 0
        self.rb_tree[7] = 0

        del self.rb_tree[10]

        """
           ___5B___               after:       ___5B___
         /         \                          /        \
        2B          8R                       2B         7R
                  /   \                               /    \
                 6B    10B - remove                 6B     8B
                  \
                   7R
                """
        self.assertTrue(self.rb_tree.black_height(self.rb_tree.root))

    def test_black_node_no_children_case2(self):
        # КЧ2 сведенный к ЧЧ5
        self.rb_tree[5] = 0
        self.rb_tree[2] = 0
        self.rb_tree[7] = 0
        self.rb_tree[8] = 0
        self.rb_tree[10] = 0
        self.rb_tree[6] = 0

        del self.rb_tree[10]

        """
           ___5B___               after:       ___5B___
         /         \                          /        \
        2B          8R                       2B         7R
                  /   \                               /    \
                 7B    10B - remove                 6B     8B
                /
               6R
                """
        self.assertTrue(self.rb_tree.black_height(self.rb_tree.root))