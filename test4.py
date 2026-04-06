import unittest
import random
from red_black_priority_queue import RedBlackPriorityQueue

class TestRedBlackPriorityQueue(unittest.TestCase):
    def setUp(self):
        """Ініціалізація нової черги перед кожним тестом."""
        self.pq = RedBlackPriorityQueue()

    def test_empty_queue(self):
        """Перевірка операцій на порожній черзі."""
        self.assertIsNone(self.pq.peek())
        self.assertIsNone(self.pq.pop())

    def test_single_insert(self):
        """Перевірка вставки та витягування одного елемента."""
        self.pq.insert("Завдання 1", 10)
        self.assertEqual(self.pq.peek(), ("Завдання 1", 10))
        self.assertEqual(self.pq.pop(), ("Завдання 1", 10))
        
        # Після видалення черга має бути порожньою
        self.assertIsNone(self.pq.peek())

    def test_peek_highest_priority(self):
        """Перевірка, чи peek завжди повертає елемент з найвищим пріоритетом."""
        self.pq.insert("A", 10)
        self.pq.insert("B", 50)
        self.pq.insert("C", 30)
        self.assertEqual(self.pq.peek(), ("B", 50))

    def test_pop_order(self):
        """Перевірка, чи елементи витягуються у правильному порядку (від більшого до меншого)."""
        priorities = [15, 10, 50, 20, 5, 100, 0]
        for p in priorities:
            self.pq.insert(f"Завдання_{p}", p)
        
        # Очікуваний порядок - це відсортований за спаданням список пріоритетів
        expected_priorities = sorted(priorities, reverse=True)
        
        for expected_prio in expected_priorities:
            val, prio = self.pq.pop()
            self.assertEqual(prio, expected_prio)
            self.assertEqual(val, f"Завдання_{expected_prio}")

    def test_equal_priorities(self):
        """Перевірка обробки елементів з однаковим пріоритетом."""
        self.pq.insert("A1", 50)
        self.pq.insert("A2", 50)
        self.pq.insert("B", 40)
        
        # Витягуємо перші два елементи з найвищим пріоритетом (50)
        val1, prio1 = self.pq.pop()
        val2, prio2 = self.pq.pop()
        
        self.assertEqual(prio1, 50)
        self.assertEqual(prio2, 50)
        
        # Перевіряємо, що ми дістали саме A1 та A2
        popped_values = {val1, val2}
        self.assertEqual(popped_values, {"A1", "A2"})
        
        # Третій елемент має бути B з пріоритетом 40
        val3, prio3 = self.pq.pop()
        self.assertEqual(val3, "B")
        self.assertEqual(prio3, 40)

    def test_stress_random_inserts(self):
        """Стрес-тест із великою кількістю випадкових значень."""
        items = [(f"Item_{i}", random.randint(1, 1000)) for i in range(1000)]
        
        for val, prio in items:
            self.pq.insert(val, prio)
            
        # Сортуємо оригінальний масив за пріоритетом за спаданням для перевірки
        sorted_items = sorted(items, key=lambda x: x[1], reverse=True)
        
        for expected_val, expected_prio in sorted_items:
            val, prio = self.pq.pop()
            self.assertEqual(prio, expected_prio)

if __name__ == '__main__':
    unittest.main(verbosity=2)