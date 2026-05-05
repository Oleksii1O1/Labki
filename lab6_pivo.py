def solve_beer(n: int, b: int, preferences: str) -> int:

    preferences = preferences.replace(" ", "")

    # emp_likes[i] - множина індексів пива, які подобаються працівнику i
    emp_likes = []
    for i in range(n):
        liked_beers = set()
        for j in range(b):
            if preferences[i * b + j] == "Y":
                liked_beers.add(j)
        emp_likes.append(liked_beers)

    # beer_covers[j] - множина індексів працівників, яким подобається пиво j
    beer_covers = []
    for j in range(b):
        covered_emps = set()
        for i in range(n):
            if preferences[i * b + j] == "Y":
                covered_emps.add(i)
        beer_covers.append(covered_emps)

    best_ans = b

    def dfs(uncovered_emps: set, current_count: int):
        nonlocal best_ans

        # Якщо поточна кількість вже більша або дорівнює найкращому знайденому,
        # відсікаємо цю гілку (pruning)
        if current_count >= best_ans:
            return

        # Якщо всі працівники покриті, оновлюємо найкращий результат
        if not uncovered_emps:
            best_ans = current_count
            return

        # Евристика: обираємо непокритого працівника,
        # якому подобається НАЙМЕНША кількість видів пива.
        chosen_emp = min(uncovered_emps, key=lambda e: len(emp_likes[e]))

        # Перебираємо всі види пива, які подобаються обраному працівнику
        for beer in emp_likes[chosen_emp]:
            new_uncovered = uncovered_emps - beer_covers[beer]
            dfs(new_uncovered, current_count + 1)

    dfs(set(range(n)), 0)
    return best_ans


def main():
    try:
        # Зчитування даних з файлу
        with open("pivo_in.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            return

        # Парсинг першого рядка (N та B)
        n, b = map(int, lines[0].split())
        
        # Парсинг другого рядка (уподобання)
        preferences = lines[1]

        # Обчислення результату
        result = solve_beer(n, b, preferences)

        # Запис результату у вихідний файл
        with open("pivo_out.txt", "w", encoding="utf-8") as f:
            f.write(str(result) + "\n")

    except FileNotFoundError:
        print("Помилка: Файл pivo_in.txt не знайдено у поточній директорії.")
    except Exception as e:
        print(f"Сталася системна помилка під час обробки файлів: {e}")


if __name__ == "__main__":
    main()