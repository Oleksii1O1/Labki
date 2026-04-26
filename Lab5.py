import ast
from collections import deque


def parse_input(filename="input.txt"):
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Line 1: height, width
    height, width = map(int, lines[0].split(","))

    # Line 2: start row, start col
    start_row, start_col = map(int, lines[1].split(","))

    # Line 3: replacement color (e.g. 'G' or 'C')
    replacement_color = lines[2].strip().strip("'\"")

    # Remaining lines: grid rows
    grid = []
    for line in lines[3:]:
        row = ast.literal_eval(line.rstrip(","))
        grid.append(row)

    return height, width, start_row, start_col, replacement_color, grid


def flood_fill_bfs(grid, start_row, start_col, replacement_color):
    """
    Flood Fill using BFS (Breadth-First Search).
    Finds all nodes connected to the start node with the same color
    and replaces them with replacement_color.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    target_color = grid[start_row][start_col]

    # If target color is already the replacement color — nothing to do
    if target_color == replacement_color:
        return grid

    queue = deque()
    queue.append((start_row, start_col))
    grid[start_row][start_col] = replacement_color

    # 4-directional movement (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        row, col = queue.popleft()

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            if (0 <= new_row < rows and
                    0 <= new_col < cols and
                    grid[new_row][new_col] == target_color):
                grid[new_row][new_col] = replacement_color
                queue.append((new_row, new_col))

    return grid


def write_output(grid, filename="output.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for row in grid:
            formatted = "[" + ", ".join(f"'{cell}'" for cell in row) + "]"
            f.write(formatted + "\n")


def print_grid(grid, title=""):
    if title:
        print(f"\n{title}")
    for row in grid:
        print("[" + ", ".join(f"'{cell}'" for cell in row) + "]")


def main():
    # --- Parse input ---
    height, width, start_row, start_col, replacement_color, grid = parse_input("input.txt")

    print(f"Grid size: {height}x{width}")
    print(f"Start node: ({start_row}, {start_col})")
    print(f"Target color at start: '{grid[start_row][start_col]}'")
    print(f"Replacement color: '{replacement_color}'")

    print_grid(grid, "Before Flood Fill:")

    # --- Apply Flood Fill ---
    result = flood_fill_bfs(grid, start_row, start_col, replacement_color)

    print_grid(result, "After Flood Fill:")

    # --- Write output ---
    write_output(result, "output.txt")
    print("\nResult saved to output.txt")


if __name__ == "__main__":
    main()