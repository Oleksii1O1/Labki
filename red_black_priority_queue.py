RED = 1
BLACK = 0

class Node:
    # Оптимізація пам'яті: забороняємо створення __dict__ для кожного вузла
    __slots__ = ['value', 'priority', 'color', 'left', 'right', 'parent']

    def __init__(self, value, priority):
        self.value = value
        self.priority = priority
        self.color = RED
        self.left = None
        self.right = None
        self.parent = None

class RedBlackPriorityQueue:
    def __init__(self):
        self.TNULL = Node(None, None)
        self.TNULL.color = BLACK
        self.root = self.TNULL

    def peek(self):
        """O(log n) - Повертає елемент з найвищим пріоритетом (крайній лівий)."""
        if self.root is self.TNULL:
            return None
        
        node = self.root
        while node.left is not self.TNULL:
            node = node.left
            
        return (node.value, node.priority)

    def pop(self):
        """O(log n) - Видаляє та повертає елемент з найвищим пріоритетом."""
        if self.root is self.TNULL:
            return None

        # Знаходимо максимум (крайній лівий вузол)
        z = self.root
        while z.left is not self.TNULL:
            z = z.left

        val, prio = z.value, z.priority
        y_original_color = z.color
        
        # Оскільки z - крайній лівий, у нього ТОЧНО немає лівої дитини.
        # Тому ми просто "підтягуємо" його праву дитину на його місце.
        x = z.right
        self._transplant(z, x)

        # Якщо ми видалили чорний вузол, чорна висота дерева порушилась, треба балансувати
        if y_original_color == BLACK:
            self._delete_fixup(x)

        return (val, prio)

    def insert(self, value, priority):
        """O(log n) - Вставка нового елемента."""
        new_node = Node(value, priority)
        new_node.left = self.TNULL
        new_node.right = self.TNULL

        y = None
        x = self.root

        # Спускаємось по дереву: більші та рівні пріоритети йдуть ВЛІВО
        while x is not self.TNULL:
            y = x
            if new_node.priority >= x.priority:
                x = x.left
            else:
                x = x.right

        new_node.parent = y
        if y is None:
            self.root = new_node
        elif new_node.priority >= y.priority:
            y.left = new_node
        else:
            y.right = new_node

        # Якщо це корінь, він має бути чорним
        if new_node.parent is None:
            new_node.color = BLACK
            return

        # Якщо дідуся немає, балансувати не треба
        if new_node.parent.parent is None:
            return

        # Відновлюємо властивості дерева
        self._insert_fixup(new_node)

    # --- Внутрішні методи (Повороти та Каскади) ---

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left is not self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right is not self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x is x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def _transplant(self, u, v):
        """Замінює піддерево з коренем u на піддерево з коренем v."""
        if u.parent is None:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _insert_fixup(self, k):
        while k.parent is not None and k.parent.color == RED:
            if k.parent is k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == RED:
                    u.color = BLACK
                    k.parent.color = BLACK
                    k.parent.parent.color = RED
                    k = k.parent.parent
                else:
                    if k is k.parent.left:
                        k = k.parent
                        self._right_rotate(k)
                    k.parent.color = BLACK
                    k.parent.parent.color = RED
                    self._left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == RED:
                    u.color = BLACK
                    k.parent.color = BLACK
                    k.parent.parent.color = RED
                    k = k.parent.parent
                else:
                    if k is k.parent.right:
                        k = k.parent
                        self._left_rotate(k)
                    k.parent.color = BLACK
                    k.parent.parent.color = RED
                    self._right_rotate(k.parent.parent)
            if k is self.root:
                break
        self.root.color = BLACK

    def _delete_fixup(self, x):
        while x is not self.root and x.color == BLACK:
            if x is x.parent.left:
                w = x.parent.right
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self._right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = BLACK

    def print_tree(self):
        """Допоміжний метод для візуалізації поточного стану дерева."""
        def print_helper(curr_ptr, indent, last):
            if curr_ptr != self.TNULL:
                import sys
                sys.stdout.write(indent)
                if last:
                    sys.stdout.write("R----")
                    indent += "     "
                else:
                    sys.stdout.write("L----")
                    indent += "|    "

                s_color = "RED" if curr_ptr.color == RED else "BLACK"
                print(f"[{curr_ptr.priority}] ({s_color})")
                print_helper(curr_ptr.left, indent, False)
                print_helper(curr_ptr.right, indent, True)

        print_helper(self.root, "", True)


# --- Приклад використання ---
if __name__ == "__main__":
    pq = RedBlackPriorityQueue()
    
    # Вставка: (значення, пріоритет)
    pq.insert("Завдання А", 10)
    pq.insert("Завдання Б", 50)
    pq.insert("Завдання В", 30)
    pq.insert("Завдання Г", 50) # Рівний пріоритет (піде вліво)
    pq.insert("Завдання Д", 5)
    
    print("Структура дерева (число = пріоритет):")
    pq.print_tree()
    print("-" * 30)
    
    print(f"Peek (перегляд найвищого): {pq.peek()}")

    
    print("Витягування елементів (від найвищого пріоритету до найнижчого):")
    while True:
        item = pq.pop()
        if not item:
            break
        print(f"Отримано: {item[0]} з пріоритетом {item[1]}")