import os


def build_transition_table(needle: str) -> list:
    m = len(needle)
    tf = [{} for _ in range(m + 1)]
    unique_chars = set(needle)

    for state in range(m + 1):
        for char in unique_chars:
            next_state = 0
            if state < m and char == needle[state]:
                next_state = state + 1
            else:
                temp_str = needle[:state] + char
                for ns in range(state, 0, -1):
                    if temp_str.endswith(needle[:ns]):
                        next_state = ns
                        break
            tf[state][char] = next_state

    return tf


def search_with_dfa(haystack: str, needle: str) -> list:
    if not needle or not haystack:
        return []

    tf = build_transition_table(needle)
    m = len(needle)
    n = len(haystack)
    state = 0
    results = []

    for i in range(n):
        state = tf[state].get(haystack[i], 0)
        if state == m:
            results.append(i - m + 1)

    return results


def process_files(input_filepath: str, output_filepath: str) -> None:
    if not os.path.exists(input_filepath):
        raise FileNotFoundError(f"Файл {input_filepath} відсутній.")

    with open(input_filepath, "r", encoding="utf-8") as infile:
        lines = infile.read().splitlines()

    if len(lines) < 2:
        raise ValueError("Файл має містити 'needle' у 1-му рядку та 'haystack' далі.")

    needle = lines[0]
    haystack = "\n".join(lines[1:])

    indices = search_with_dfa(haystack, needle)

    with open(output_filepath, "w", encoding="utf-8") as outfile:
        if indices:
            outfile.write(f"Індекси: {', '.join(map(str, indices))}\n")
        else:
            outfile.write("Збігів не знайдено.\n")


if __name__ == "__main__":
    process_files("input.txt", "output.txt")