import unittest
from unittest.mock import patch, mock_open
from lab6_pivo import solve_beer, main


class TestBeer(unittest.TestCase):
    def test_example_1_basic(self):
        """Перевірка першого базового прикладу з умови задачі."""
        n = 2
        b = 2
        preferences = "YN NY"
        self.assertEqual(solve_beer(n, b, preferences), 2)

    def test_example_2_optimal_cover(self):
        """Перевірка другого прикладу, де жадібний вибір міг би помилитися."""
        n = 6
        b = 3
        preferences = "YNN YNY YNY NYY NYY NYN"
        self.assertEqual(solve_beer(n, b, preferences), 2)

    def test_all_like_same_beer(self):
        """Випадок, коли всім працівникам подобається однаковий вид пива."""
        n = 3
        b = 3
        preferences = "YNN YNN YNN"
        self.assertEqual(solve_beer(n, b, preferences), 1)

    def test_everyone_likes_everything(self):
        """Випадок, коли абсолютно всі працівники люблять абсолютно всі види пива."""
        n = 4
        b = 4
        preferences = "YYYY YYYY YYYY YYYY"
        self.assertEqual(solve_beer(n, b, preferences), 1)

    def test_no_spaces_in_input(self):
        """Перевірка стійкості парсера до відсутності пробілів у рядку уподобань."""
        n = 2
        b = 2
        preferences = "YNNY"
        self.assertEqual(solve_beer(n, b, preferences), 2)

    @patch("builtins.open", new_callable=mock_open, read_data="2 2\nYN NY\n")
    def test_main_file_io(self, mock_file):
        """
        Перевірка повного циклу виконання (читання з pivo_in.txt та запис у pivo_out.txt)
        без створення реальних файлів на диску за допомогою mock.
        """
        main()

        # Перевіряємо, чи програма намагалася відкрити файл для запису
        mock_file.assert_any_call("pivo_out.txt", "w", encoding="utf-8")

        # Перевіряємо, чи був записаний правильний результат
        handle = mock_file()
        handle.write.assert_called_once_with("2\n")


if __name__ == "__main__":
    unittest.main()