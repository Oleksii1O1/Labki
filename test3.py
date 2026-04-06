"""
Тести для binary tree (файл з оригінальним кодом lab3.py / binary_tree.py).

Сигнатура оригінальної функції:
    find_successor(tree: BinaryTree, node: BinaryTree) -> BinaryTree | None

Дерево, що використовується в більшості тестів:

        10
       /  \\
      5    15
     / \\     \\
    3   7    20
             /
            12

In-order: 3 → 5 → 7 → 10 → 15 → 12 → 20
"""

import sys
import os
import unittest

# Якщо файл з кодом лежить поряд — імпортуємо напряму.
# Змініть назву модуля якщо потрібно (lab3, binary_tree тощо).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


from lab3 import BinaryTree, find_successor, get_leftmost



# ---------------------------------------------------------------------------
# Допоміжна функція — будує тестове дерево
# ---------------------------------------------------------------------------


def build_tree() -> dict:
    """
    Будує тестове дерево та повертає словник з усіма вузлами.

    In-order: 3 → 5 → 7 → 10 → 15 → 12 → 20
    """
    root = BinaryTree(10)

    root.left = BinaryTree(5, parent=root)
    root.right = BinaryTree(15, parent=root)

    root.left.left = BinaryTree(3, parent=root.left)
    root.left.right = BinaryTree(7, parent=root.left)

    root.right.right = BinaryTree(20, parent=root.right)
    root.right.right.left = BinaryTree(12, parent=root.right.right)

    return {
        "root": root,
        "n3": root.left.left,
        "n5": root.left,
        "n7": root.left.right,
        "n10": root,
        "n15": root.right,
        "n12": root.right.right.left,
        "n20": root.right.right,
    }


# ---------------------------------------------------------------------------
# BinaryTree — базові тести класу
# ---------------------------------------------------------------------------


class TestBinaryTreeNode(unittest.TestCase):
    """Перевіряє коректне створення вузлів BinaryTree."""

    def test_node_stores_value(self):
        node = BinaryTree(42)
        self.assertEqual(node.value, 42)

    def test_default_children_are_none(self):
        node = BinaryTree(1)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)

    def test_default_parent_is_none(self):
        node = BinaryTree(1)
        self.assertIsNone(node.parent)

    def test_explicit_children_and_parent(self):
        parent = BinaryTree(10)
        left = BinaryTree(5, parent=parent)
        right = BinaryTree(15, parent=parent)
        parent.left = left
        parent.right = right

        self.assertIs(parent.left, left)
        self.assertIs(parent.right, right)
        self.assertIs(left.parent, parent)
        self.assertIs(right.parent, parent)

    def test_node_value_is_accessible(self):
        node = BinaryTree(99)
        self.assertEqual(node.value, 99)


# ---------------------------------------------------------------------------
# get_leftmost
# ---------------------------------------------------------------------------


class TestGetLeftmost(unittest.TestCase):
    """Перевіряє функцію get_leftmost."""

    def test_single_node_returns_itself(self):
        node = BinaryTree(5)
        self.assertIs(get_leftmost(node), node)

    def test_left_chain(self):
        """3 → 2 → 1; лівий кінець = 1."""
        n3 = BinaryTree(3)
        n2 = BinaryTree(2, parent=n3)
        n1 = BinaryTree(1, parent=n2)
        n3.left = n2
        n2.left = n1

        self.assertIs(get_leftmost(n3), n1)

    def test_no_left_child_returns_node(self):
        n5 = BinaryTree(5)
        n7 = BinaryTree(7, parent=n5)
        n5.right = n7

        self.assertIs(get_leftmost(n5), n5)

    def test_leftmost_in_full_tree(self):
        nodes = build_tree()
        self.assertEqual(get_leftmost(nodes["root"]).value, 3)


# ---------------------------------------------------------------------------
# find_successor — гілка "є праве піддерево"
# ---------------------------------------------------------------------------


class TestFindSuccessorWithRightSubtree(unittest.TestCase):
    """Вузол має праве піддерево → наступник = leftmost(right)."""

    def setUp(self):
        self.nodes = build_tree()
        self.root = self.nodes["root"]

    def test_root_successor_is_15(self):
        # root(10) → right=15; у 15 немає лівого нащадка → наступник 15
        result = find_successor(self.root, self.nodes["n10"])
        self.assertIsNotNone(result)
        self.assertEqual(result.value, 15)

    def test_node15_successor_is_12(self):
        # 15 → right=20 → leftmost(20)=12
        result = find_successor(self.root, self.nodes["n15"])
        self.assertIsNotNone(result)
        self.assertEqual(result.value, 12)

    def test_node5_successor_is_7(self):
        # 5 → right=7 → leftmost(7)=7 (листок)
        result = find_successor(self.root, self.nodes["n5"])
        self.assertIsNotNone(result)
        self.assertEqual(result.value, 7)


# ---------------------------------------------------------------------------
# find_successor — гілка "немає правого піддерева"
# ---------------------------------------------------------------------------


class TestFindSuccessorWithoutRightSubtree(unittest.TestCase):
    """Вузол без правого піддерева → піднімаємось через parent."""

    def setUp(self):
        self.nodes = build_tree()
        self.root = self.nodes["root"]

    def test_node3_successor_is_5(self):
        # 3 — лівий нащадок 5 → наступник 5
        result = find_successor(self.root, self.nodes["n3"])
        self.assertIsNotNone(result)
        self.assertEqual(result.value, 5)

    def test_node7_successor_is_10(self):
        # 7 — правий нащадок 5; 5 — лівий нащадок 10 → наступник 10
        result = find_successor(self.root, self.nodes["n7"])
        self.assertIsNotNone(result)
        self.assertEqual(result.value, 10)

    def test_node12_successor_is_20(self):
        # 12 — лівий нащадок 20 → наступник 20
        result = find_successor(self.root, self.nodes["n12"])
        self.assertIsNotNone(result)
        self.assertEqual(result.value, 20)


# ---------------------------------------------------------------------------
# find_successor — найбільший вузол (наступника немає)
# ---------------------------------------------------------------------------


class TestFindSuccessorMaxNode(unittest.TestCase):
    """Найбільший вузол не має наступника → повертає None."""

    def test_max_node_returns_none(self):
        nodes = build_tree()
        result = find_successor(nodes["root"], nodes["n20"])
        self.assertIsNone(result)

    def test_single_node_tree_returns_none(self):
        single = BinaryTree(1)
        self.assertIsNone(find_successor(single, single))

    def test_right_chain_last_node_returns_none(self):
        """Дерево: 1 → 2 → 3 (тільки праві нащадки); наступника 3 немає."""
        n1 = BinaryTree(1)
        n2 = BinaryTree(2, parent=n1)
        n3 = BinaryTree(3, parent=n2)
        n1.right = n2
        n2.right = n3

        self.assertIsNone(find_successor(n1, n3))


# ---------------------------------------------------------------------------
# find_successor — повний in-order обхід дерева
# ---------------------------------------------------------------------------


class TestInOrderTraversal(unittest.TestCase):
    """Перевіряє, що ланцюжок find_successor відтворює in-order послідовність."""

    def _collect_inorder(self, root: BinaryTree) -> list:
        """Зібрати in-order обхід через get_leftmost + find_successor."""
        values = []
        current = get_leftmost(root)
        while current is not None:
            values.append(current.value)
            current = find_successor(root, current)
        return values

    def test_full_tree_inorder(self):
        nodes = build_tree()
        result = self._collect_inorder(nodes["root"])
        self.assertEqual(result, [3, 5, 7, 10, 15, 12, 20])

    def test_single_node_inorder(self):
        root = BinaryTree(42)
        result = self._collect_inorder(root)
        self.assertEqual(result, [42])

    def test_left_only_tree_inorder(self):
        """Дерево тільки з лівими нащадками: 5 → 3 → 1."""
        n5 = BinaryTree(5)
        n3 = BinaryTree(3, parent=n5)
        n1 = BinaryTree(1, parent=n3)
        n5.left = n3
        n3.left = n1

        result = self._collect_inorder(n5)
        self.assertEqual(result, [1, 3, 5])

    def test_right_only_tree_inorder(self):
        """Дерево тільки з правими нащадками: 1 → 2 → 3."""
        n1 = BinaryTree(1)
        n2 = BinaryTree(2, parent=n1)
        n3 = BinaryTree(3, parent=n2)
        n1.right = n2
        n2.right = n3

        result = self._collect_inorder(n1)
        self.assertEqual(result, [1, 2, 3])

    def test_balanced_tree_inorder(self):
        """Збалансоване дерево з 7 вузлів: in-order = 1..7."""
        #       4
        #      / \
        #     2   6
        #    / \ / \
        #   1  3 5  7
        root = BinaryTree(4)
        root.left = BinaryTree(2, parent=root)
        root.right = BinaryTree(6, parent=root)
        root.left.left = BinaryTree(1, parent=root.left)
        root.left.right = BinaryTree(3, parent=root.left)
        root.right.left = BinaryTree(5, parent=root.right)
        root.right.right = BinaryTree(7, parent=root.right)

        result = self._collect_inorder(root)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6, 7])


if __name__ == "__main__":
    unittest.main(verbosity=2)