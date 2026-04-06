import unittest
from lab2 import min_cost


class TestDiscountAlgorithm(unittest.TestCase):

    def test_example_1(self):
        self.assertAlmostEqual(min_cost([50, 20, 30, 17, 100], 10), 207.00, places=2)

    def test_example_2(self):
        self.assertAlmostEqual(min_cost([1, 2, 3, 4, 5, 6, 7], 100), 15.00, places=2)

    def test_example_3(self):
        self.assertAlmostEqual(min_cost([1, 1, 1], 33), 2.67, places=2)

    def test_empty(self):
        self.assertEqual(min_cost([], 50), 0.0)

    def test_single_item(self):
        self.assertEqual(min_cost([0], 50), 0.00)


if __name__ == "__main__":
    unittest.main()