import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from lab_9 import search_with_dfa


class TestDFASearch(unittest.TestCase):
    
    def test_standard_search(self):
        haystack = "AABAACAADAABAABA"
        needle = "AABA"
        self.assertEqual(search_with_dfa(haystack, needle), [0, 9, 12])

    def test_no_match(self):
        haystack = "Текст для пошуку"
        needle = "Автомат"
        self.assertEqual(search_with_dfa(haystack, needle), [])

    def test_empty_needle(self):
        self.assertEqual(search_with_dfa("Довільний текст", ""), [])

    def test_empty_haystack(self):
        self.assertEqual(search_with_dfa("", "Шукаю"), [])

    def test_overlapping_matches(self):
        haystack = "AAAA"
        needle = "AA"
        self.assertEqual(search_with_dfa(haystack, needle), [0, 1, 2])

    def test_cyrillic_search(self):
        haystack = "абабагаламага"
        needle = "аба"
        self.assertEqual(search_with_dfa(haystack, needle), [0, 2])


if __name__ == "__main__":
    unittest.main()