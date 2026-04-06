class BinaryTree:
    def __init__(self, value, left=None, right=None, parent=None):
        self.value  = value
        self.left   = left
        self.right  = right
        self.parent = parent


def find_successor(tree: BinaryTree, node: BinaryTree) -> BinaryTree:
    # ── Випадок 1: є праве піддерево ──────────────────────────
    # Наступник = найлівіший вузол правого піддерева
    if node.right is not None:
        return get_leftmost(node.right)

    # ── Випадок 2: немає правого піддерева ────────────────────
    # Піднімаємось через parent поки не прийдемо з лівого боку
    current = node
    parent  = node.parent

    while parent is not None and parent.right is current:
        # Поточний вузол — правий нащадок → йдемо вище
        current = parent
        parent  = parent.parent

    return parent


def get_leftmost(node: BinaryTree) -> BinaryTree:
    """Знаходить найлівіший (найменший) вузол у піддереві"""
    current = node
    while current.left is not None:
        current = current.left
    return current


def print_tree(node, level=0, prefix="Root: "):
    if node is not None:
        print(" " * (level * 4) + prefix + str(node.value))
        if node.left or node.right:
            if node.left:
                print_tree(node.left, level + 1, "L--- ")
            else:
                print(" " * ((level + 1) * 4) + "L--- None")
            
            if node.right:
                print_tree(node.right, level + 1, "R--- ")
            else:
                print(" " * ((level + 1) * 4) + "R--- None")
                
def draw_tree_graphic(node):
    def get_lines(node):
        if node is None:
            return [], 0, 0, 0
        
        line1 = []
        line2 = []
        node_repr = str(node.value)
        new_root_width = gap_size = len(node_repr)

        # Рекурсивно отримуємо гілки
        l_lines, l_width, l_root_start, l_root_end = get_lines(node.left)
        r_lines, r_width, r_root_start, r_root_end = get_lines(node.right)

        if l_width > 0:
            l_root = (l_root_start + l_root_end) // 2
            line1.append(' ' * (l_root + 1))
            line1.append('_' * (l_width - l_root - 1))
            line2.append(' ' * l_root + '/')
            line2.append(' ' * (l_width - l_root - 1))
            new_root_start = l_width + 1
            gap_size = 1
        else:
            new_root_start = 0
            gap_size = 0

        line1.append(node_repr)
        line2.append(' ' * new_root_width)

        if r_width > 0:
            r_root = (r_root_start + r_root_end) // 2
            line1.append('_' * r_root)
            line1.append(' ' * (r_width - r_root))
            line2.append(' ' * r_root + '\\')
            line2.append(' ' * (r_width - r_root))
            gap_size += 1
        new_root_end = new_root_start + new_root_width - 1

        # Комбінуємо рядки
        merged_lines = [''.join(line1), ''.join(line2)]
        for i in range(max(len(l_lines), len(r_lines))):
            l_line = l_lines[i] if i < len(l_lines) else ' ' * l_width
            r_line = r_lines[i] if i < len(r_lines) else ' ' * r_width
            merged_lines.append(l_line + ' ' * (gap_size + new_root_width - (new_root_width if gap_size > 0 else 0)) + r_line)
        
        return merged_lines, len(merged_lines[0]), new_root_start, new_root_end

    lines, *_ = get_lines(node)
    for line in lines:
        print(line)

root        = BinaryTree(10)

root.left   = BinaryTree(5,  parent=root)
root.right  = BinaryTree(15, parent=root)

root.left.left  = BinaryTree(3, parent=root.left)
root.left.right = BinaryTree(7, parent=root.left)

root.right.right      = BinaryTree(20, parent=root.right)
root.right.right.left = BinaryTree(12, parent=root.right.right)

# In-order: 3 → 5 → 7 → 10 → 12 → 15 → 20

tests = [
    (root.left.left,        3,   5),
    (root.left,             5,   7),
    (root.left.right,       7,   10),
    (root,                  10,  15),   # ← було 12, правильно 15
    (root.right,            15,  12),   # ← було 20, правильно 12
    (root.right.right.left, 12,  20),   # ← було 15, правильно 20
    (root.right.right,      20,  None),
]

print("Тестування:")
for node, val, expected in tests:
    result = find_successor(root, node)
    result_val = result.value if result else None
    status = "True" if result_val == expected else "False"
    print(f"  {status}  successor({val}) = {result_val}  (очікується {expected})")

print("\nВізуалізація дерева:")
print_tree(root)
print("Графічне відображення дерева:")
draw_tree_graphic(root)