def solve_ijones(width: int, height: int, grid: list[str]) -> int:

    if width == 0 or height == 0:
        return 0

    sum_ways = [0] * 26
    prev_ways = [1] * height

    for y in range(height):
        char_idx = ord(grid[y][0]) - 97
        sum_ways[char_idx] += 1

    for x in range(1, width):
        curr_ways = [0] * height

        for y in range(height):
            char_idx = ord(grid[y][x]) - 97

            ways = sum_ways[char_idx]


            if grid[y][x - 1] != grid[y][x]:
                ways += prev_ways[y]

            curr_ways[y] = ways

        for y in range(height):
            char_idx = ord(grid[y][x]) - 97
            sum_ways[char_idx] += curr_ways[y]

        prev_ways = curr_ways

    if height == 1:
        return prev_ways[0]
    return prev_ways[0] + prev_ways[height - 1]


def main() -> None:
    with open("ijones.in", "r", encoding="utf-8") as file_in:
        lines = file_in.read().splitlines()

    if not lines:
        return

    first_line = lines[0].strip().split()
    if len(first_line) < 2:
        return

    width = int(first_line[0])
    height = int(first_line[1])

    grid = [lines[i].strip() for i in range(1, height + 1) if i < len(lines)]

    result = solve_ijones(width, height, grid)

    with open("ijones.out", "w", encoding="utf-8") as file_out:
        file_out.write(f"{result}\n")


if __name__ == "__main__":
    main()