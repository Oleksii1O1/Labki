def read_adjacency_matrix(file_path):
    matrix = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            row = [int(val) for val in line.split()]
            if row:
                matrix.append(row)
    return matrix


def calculate_minimum_cable_length(matrix):
    if not matrix or not matrix[0]:
        return 0

    n = len(matrix)
    visited = [False] * n
    
    # Використовуємо вбудовану константу нескінченності замість імпорту math.inf
    inf = float('inf')
    min_weight = [inf] * n
    min_weight[0] = 0
    
    total_length = 0

    for _ in range(n):
        # 1. Знаходимо невідвідану вершину з мінімальною вагою ребра
        u = -1
        current_min = inf
        for i in range(n):
            if not visited[i] and min_weight[i] < current_min:
                current_min = min_weight[i]
                u = i

        # Якщо всі досяжні вершини відвідані (або граф незв'язний)
        if u == -1:
            break

        # 2. Позначаємо вершину як відвідану та додаємо довжину до загальної
        visited[u] = True
        total_length += current_min

        # 3. Оновлюємо мінімальні ваги для всіх суміжних невідвіданих вершин
        for v in range(n):
            if matrix[u][v] > 0 and not visited[v] and matrix[u][v] < min_weight[v]:
                min_weight[v] = matrix[u][v]

    return total_length


def write_result_to_file(length, output_path):
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(f"{length}\n")


def main():
    input_file = "islands.csv"
    output_file = "result.txt"

    try:
        matrix = read_adjacency_matrix(input_file)
        result = calculate_minimum_cable_length(matrix)
        write_result_to_file(result, output_file)
        print(f"Готово. Результат записано у {output_file}")
    except FileNotFoundError:
        print(f"Помилка: Файл {input_file} не знайдено.")
    except Exception as e:
        print(f"Критична помилка при зчитуванні: {e}")


if __name__ == "__main__":
    main()