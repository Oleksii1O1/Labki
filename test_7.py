import unittest
import os
import tempfile
import csv
from laba7 import (
    read_adjacency_matrix,
    calculate_minimum_cable_length,
    write_result_to_file,
)


class TestVeniceCables(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.input_file = os.path.join(self.test_dir.name, "islands.csv")
        self.output_file = os.path.join(self.test_dir.name, "result.txt")

    def tearDown(self):
        self.test_dir.cleanup()

    def create_csv(self, data: list[list[int]]):
        with open(self.input_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(data)

    def test_calculate_minimum_cable_length(self):
        matrix = [
            [0, 2, 0, 6, 0],
            [2, 0, 3, 8, 5],
            [0, 3, 0, 0, 7],
            [6, 8, 0, 0, 9],
            [0, 5, 7, 9, 0],
        ]
        self.assertEqual(calculate_minimum_cable_length(matrix), 16)

    def test_write_result_to_file(self):
        expected_val = 42
        write_result_to_file(expected_val, self.output_file)

        with open(self.output_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
        self.assertEqual(content, str(expected_val))

    def test_full_process(self):
        data = [[0, 5, 10], [5, 0, 3], [10, 3, 0]]
        self.create_csv(data)
        matrix = read_adjacency_matrix(self.input_file)
        result = calculate_minimum_cable_length(matrix)
        write_result_to_file(result, self.output_file)

        with open(self.output_file, "r", encoding="utf-8") as f:
            self.assertEqual(f.read().strip(), "8")


if __name__ == "__main__":
    unittest.main()