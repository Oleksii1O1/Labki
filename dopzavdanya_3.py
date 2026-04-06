import os

class BinaryTree:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def print_tree(self):
        # Використовуємо словник замість масиву, щоб полотно було "нескінченним"
        canvas = {}

        def draw(node, r, c, dir_x, h_step, v_step):
            if not node:
                return

            # Малюємо число
            val_str = str(node.value)
            for i, char in enumerate(val_str):
                canvas[(r, c + i)] = char

            # Плавне зменшення кроку (щоб гілки не налізали одна на одну)
            next_h = max(5, int(h_step * 0.75))
            next_v = max(4, int(v_step * 0.75))

            if node.left:
                # Лівий нащадок ЗАВЖДИ йде вгору (r - v_step)
                symbol = "/" if dir_x == -1 else "\\"
                for i in range(1, v_step):
                    curr_r = r - i
                    curr_c = c + dir_x * int(i * (h_step / v_step))
                    canvas[(curr_r, curr_c)] = symbol
                
                draw(node.left, r - v_step, c + dir_x * h_step, dir_x, next_h, next_v)

            if node.right:
                # Правий нащадок ЗАВЖДИ йде вниз (r + v_step)
                symbol = "\\" if dir_x == -1 else "/"
                for i in range(1, v_step):
                    curr_r = r + i
                    curr_c = c + dir_x * int(i * (h_step / v_step))
                    canvas[(curr_r, curr_c)] = symbol
                
                draw(node.right, r + v_step, c + dir_x * h_step, dir_x, next_h, next_v)

        # 1. Малюємо корінь у нульових координатах
        root_r, root_c = 0, 0
        val_str = str(self.value)
        for i, ch in enumerate(val_str):
            canvas[(root_r, root_c + i)] = ch

        # 2. Відводимо ліву і праву гілки від кореня
        if self.left:
            for i in range(1, 12): 
                canvas[(root_r, root_c - i)] = "─"
            draw(self.left, root_r, root_c - 13, -1, 16, 12)

        if self.right:
            for i in range(1, 12): 
                canvas[(root_r, root_c + len(val_str) + i - 1)] = "─"
            draw(self.right, root_r, root_c + 11 + len(val_str), 1, 16, 12)

        # 3. Визначаємо реальні межі нашого малюнка
        if not canvas: return
        min_r = min(r for r, c in canvas.keys())
        max_r = max(r for r, c in canvas.keys())
        min_c = min(c for r, c in canvas.keys())
        max_c = max(c for r, c in canvas.keys())

        # 4. Друкуємо рівно від найвищої до найнижчої точки
        print("\n")
        for r in range(min_r, max_r + 1):
            line = []
            for c in range(min_c, max_c + 1):
                line.append(canvas.get((r, c), " "))
            print("".join(line).rstrip())
        print("\n")


def build_from_simple_list(arr):
    if not arr: return None
    mid = len(arr) // 2
    node = BinaryTree(arr[mid])
    node.left = build_from_simple_list(arr[:mid])
    node.right = build_from_simple_list(arr[mid+1:])
    return node

def main():
    filename = "tree.txt"
    
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write(" ".join(map(str, range(1, 21))))

    with open(filename, "r") as f:
        content = f.read().split()

    numbers = []
    for x in content:
        try:
            numbers.append(int(x))
        except ValueError:
            pass
    
    numbers.sort()
    
    root = build_from_simple_list(numbers)

    if root:
        root.print_tree()

if __name__ == "__main__":
    main()