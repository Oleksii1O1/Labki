import os
import sys
import unittest

# Додаємо теку src до шляху пошуку модулів для імпорту
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from Lab8 import solve_ijones

class TestIJones(unittest.TestCase):
  
    def test_example_1(self):
        width, height = 3, 3
        grid = [
            "aaa",
            "cab",
            "def"
        ]
        self.assertEqual(solve_ijones(width, height, grid), 5)

    def test_example_2(self):
        width, height = 10, 1
        grid = [
            "abcdefaghi"
        ]
        self.assertEqual(solve_ijones(width, height, grid), 2)

    def test_example_3(self):
        width, height = 7, 6
        grid = [
            "aaaaaaa",
            "aaaaaaa",
            "aaaaaaa",
            "aaaaaaa",
            "aaaaaaa",
            "aaaaaaa"
        ]
        self.assertEqual(solve_ijones(width, height, grid), 201684)

    def test_single_cell(self):
        width, height = 1, 1
        grid = ["a"]
        self.assertEqual(solve_ijones(width, height, grid), 1)


if __name__ == "__main__":
    unittest.main()