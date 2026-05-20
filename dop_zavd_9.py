import tkinter as tk
from tkinter import messagebox, filedialog
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


def load_from_file() -> None:
 
    filepath = filedialog.askopenfilename(
        title="Оберіть текстовий файл (наприклад, input.txt)",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    
    if not filepath:
        return  

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()

        if not lines:
            messagebox.showwarning("Увага", "Обраний файл порожній.")
            return

        entry_needle.delete(0, tk.END)
        text_haystack.delete("1.0", tk.END)

        if len(lines) >= 1:
            entry_needle.insert(0, lines[0])
            
        if len(lines) >= 2:
            text_haystack.insert(tk.END, "\n".join(lines[1:]))

        messagebox.showinfo(
            "Успіх", 
            f"Дані успішно завантажено з файлу:\n{os.path.basename(filepath)}"
        )

    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося прочитати файл:\n{e}")


def run_search() -> None:
    needle = entry_needle.get().strip()
    haystack_content = text_haystack.get("1.0", tk.END).strip('\n')
    lines = haystack_content.split('\n')

    text_haystack.tag_remove("match", "1.0", tk.END)
    text_result.delete("1.0", tk.END)

    if not needle:
        messagebox.showwarning("Увага", "Будь ласка, введіть шукане слово (needle).")
        return

    if not haystack_content:
        messagebox.showwarning("Увага", "Будь ласка, введіть текст для пошуку.")
        return

    total_matches = 0

    for line_index, line in enumerate(lines):
        row = line_index + 1
        indices = search_with_dfa(line, needle)
        
        if indices:
            total_matches += len(indices)
            text_result.insert(tk.END, f"Рядок {row}: Знайдено {len(indices)} збіг(ів). Індекси: {', '.join(map(str, indices))}\n")
            
            for start_idx in indices:
                start_pos = f"{row}.{start_idx}"
                end_pos = f"{row}.{start_idx + len(needle)}"
                text_haystack.tag_add("match", start_pos, end_pos)
        else:
            text_result.insert(tk.END, f"Рядок {row}: Збігів не знайдено.\n")

    text_result.insert(tk.END, f"\nЗагальна кількість збігів у тексті: {total_matches}\n")
    text_haystack.tag_config("match", background="yellow", foreground="red", font=("Consolas", 12, "bold"))


def setup_gui() -> None:
    global entry_needle, text_haystack, text_result

    root = tk.Tk()
    root.title("DFA Візуалізатор Пошуку")
    root.geometry("700x650")
    root.configure(padx=10, pady=10)

    frame_file = tk.Frame(root)
    frame_file.pack(fill=tk.X, pady=(0, 15))
    
    btn_load = tk.Button(
        frame_file, 
        text="📂 Завантажити файл (input.txt)", 
        font=("Arial", 11), 
        command=load_from_file
    )
    btn_load.pack(side=tk.LEFT)

    # --- Блок: Шукане слово ---
    frame_top = tk.Frame(root)
    frame_top.pack(fill=tk.X, pady=(0, 10))

    tk.Label(frame_top, text="Шукане слово (needle):", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
    entry_needle = tk.Entry(frame_top, font=("Consolas", 12), width=30)
    entry_needle.pack(side=tk.LEFT, padx=10)

    btn_search = tk.Button(
        frame_top, text="🔍 Знайти", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", command=run_search
    )
    btn_search.pack(side=tk.RIGHT)

    tk.Label(root, text="Текст для пошуку (haystack):", font=("Arial", 12, "bold")).pack(anchor=tk.W)
    
    text_haystack = tk.Text(root, height=10, font=("Consolas", 12), wrap=tk.WORD)
    text_haystack.pack(fill=tk.BOTH, expand=True, pady=(5, 15))

    tk.Label(root, text="Результати роботи автомата:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
    
    text_result = tk.Text(root, height=10, font=("Consolas", 11), bg="#f0f0f0", state=tk.NORMAL)
    text_result.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

    root.mainloop()


if __name__ == "__main__":
    setup_gui()