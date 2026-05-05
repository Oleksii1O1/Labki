
BASE_DIR = __file__.replace("\\", "/").rsplit("/", 1)[0]
INPUT_FILE = BASE_DIR + "/input1.txt"
OUTPUT_FILE = BASE_DIR + "/output1.txt"
DECAY = 10



class Queue:
    def __init__(self):
        self.data = []
        self.head = 0  

    def append(self, item):
        self.data.append(item)

    def popleft(self):
        item = self.data[self.head]
        self.head += 1
        return item

    def __bool__(self):
        return self.head < len(self.data)


def file_exists(filepath):
    try:
        open(filepath).close()
        return True
    except FileNotFoundError:
        return False


def read_input(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    if len(lines) < 3:
        raise ValueError("Файл порожній або неправильний формат!")

    rows, cols = map(int, lines[0].split())
    start_r, start_c = map(int, lines[1].split())
    max_signal = int(lines[2])

    grid = []
    for i in range(rows):
        if 3 + i >= len(lines):
            raise ValueError(f"Не вистачає рядків! Очікувалось {rows}, є {i}")
        row = list(lines[3 + i])
        for j in range(cols):
            if row[j] == 'R':
                start_r, start_c = i, j
                row[j] = '.'
        grid.append(row)

    return rows, cols, start_r, start_c, max_signal, grid


def simulate(rows, cols, start_r, start_c, max_signal, grid):
    signal = [[0] * cols for _ in range(rows)]

    queue = Queue()  
    queue.append((start_r, start_c, max_signal))
    signal[start_r][start_c] = max_signal

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while queue:
        r, c, s = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if nr < 0 or nc < 0 or nr >= rows or nc >= cols:
                continue
            if grid[nr][nc] == '#':
                continue
            new_s = s - DECAY
            if new_s <= 0:
                continue
            if signal[nr][nc] < new_s:
                signal[nr][nc] = new_s
                queue.append((nr, nc, new_s))

    return signal


def write_output(filename, signal):
    with open(filename, "w") as f:
        for row in signal:
            f.write(" ".join(map(str, row)) + "\n")


def main():
    print(f"Папка скрипта: {BASE_DIR}")
    print(f"Шукаю: {INPUT_FILE}")

    if not file_exists(INPUT_FILE):
        print("Файл 'input1.txt' не знайдено!")
        return

    try:
        rows, cols, sr, sc, max_signal, grid = read_input(INPUT_FILE)
        result = simulate(rows, cols, sr, sc, max_signal, grid)
        write_output(OUTPUT_FILE, result)
        print("Готово! 'output1.txt' оновлено.")
    except ValueError as e:
        print(f"Помилка: {e}")
    except Exception as e:
        print(f"Несподівана помилка: {e}")


if __name__ == "__main__":
    main()