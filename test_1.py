import unittest
from lab1 import is_subarray


class TestIsSubarray(unittest.TestCase):

    def test_basic_true(self):
        self.assertTrue(is_subarray([1, 2, 3], [1, 2, 3, 4]))

    def test_wrong_order(self):
        self.assertFalse(is_subarray([4, 2], [1, 2, 3, 4]))

    def test_skip_elements(self):
        self.assertTrue(is_subarray([1, 3, 5], [1, 2, 3, 4, 5]))


if __name__ == "__main__":
    unittest.main()