

import heapq
import math
import tkinter as tk
from tkinter import filedialog, font as tkfont, messagebox
from typing import List, Optional, Tuple

# ─────────────────────────── Константи ────────────────────────────────────────
KM_SCALE     = 0.12
ISLAND_R     = 14
DELETE_R     = 22
WAVE_STEP    = 30
WAVE_AMP     = 4
WAVE_FREQ    = 0.045

C_OCEAN      = "#1a6ea0"
C_WAVE       = "#1f7bb5"
C_ISLAND     = "#e8d49c"
C_ISLAND_STR = "#b89450"
C_PALM       = "#5a8a3c"
C_LABEL      = "#5a3e1b"
C_MST        = "#5DCAA5"
C_MST_LABEL  = "#a8efd4"
C_MST_BG     = "#0a2e22"
C_ALL_EDGE   = "#4a9fd4"
C_STATS_BG   = "#f5f5f0"
C_SAVED      = "#1D9E75"
C_TEXT       = "#222222"
C_MUTED      = "#666660"
C_BADGE_BLUE = ("#e6f4ff", "#185fa5")
C_BADGE_WARN = ("#fff3cd", "#664d03")

CANVAS_W     = 760
CANVAS_H     = 430


# ═══════════════════════════════════════════════════════════════════════════════
#  ОРИГІНАЛЬНІ ФУНКЦІЇ (без змін)
# ═══════════════════════════════════════════════════════════════════════════════

def read_adjacency_matrix(file_path: str) -> List[List[int]]:
    matrix = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            row = [int(val) for val in line.split()]
            if row:
                matrix.append(row)
    return matrix


def calculate_minimum_cable_length(matrix: List[List[int]]) -> int:
    if not matrix or not matrix[0]:
        return 0

    n = len(matrix)
    visited = [False] * n
    min_heap = [(0, 0)]          # (вага, вершина)
    total_length = 0
    edges_count  = 0

    while min_heap and edges_count < n:
        weight, u = heapq.heappop(min_heap)

        if visited[u]:
            continue

        visited[u]    = True
        total_length += weight
        edges_count  += 1

        for v in range(n):
            if not visited[v] and matrix[u][v] > 0:
                heapq.heappush(min_heap, (matrix[u][v], v))

    return total_length


def write_result_to_file(length: int, output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(f"{length}\n")


# ═══════════════════════════════════════════════════════════════════════════════
#  ДОПОМІЖНІ ФУНКЦІЇ ДЛЯ ВІЗУАЛІЗАЦІЇ
# ═══════════════════════════════════════════════════════════════════════════════

def _dist(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def prim_mst_coords(points: List[Tuple[float, float]]) -> List[Tuple[int, int, float]]:
    """MST для координатних точок. Повертає [(i, j, відстань_px)]."""
    n = len(points)
    if n < 2:
        return []
    in_mst = [False] * n
    key    = [math.inf] * n
    par    = [-1] * n
    key[0] = 0.0
    heap   = [(0.0, 0)]
    edges  = []
    while heap:
        d, u = heapq.heappop(heap)
        if in_mst[u]:
            continue
        in_mst[u] = True
        if par[u] != -1:
            edges.append((par[u], u, d))
        for v in range(n):
            if not in_mst[v]:
                w = _dist(points[u], points[v])
                if w < key[v]:
                    key[v] = w
                    par[v] = u
                    heapq.heappush(heap, (w, v))
    return edges


def prim_mst_matrix(matrix: List[List[int]]) -> List[Tuple[int, int, int]]:
    """MST для матриці суміжності. Повертає [(i, j, вага)]."""
    n = len(matrix)
    if n < 2:
        return []
    visited  = [False] * n
    min_heap = [(0, 0, -1)]      # (вага, вершина, батько)
    edges    = []
    while min_heap:
        weight, u, parent = heapq.heappop(min_heap)
        if visited[u]:
            continue
        visited[u] = True
        if parent != -1:
            edges.append((parent, u, weight))
        for v in range(n):
            if not visited[v] and matrix[u][v] > 0:
                heapq.heappush(min_heap, (matrix[u][v], v, u))
    return edges


def all_edges_total_coords(points: List[Tuple[float, float]]) -> float:
    return sum(
        _dist(points[i], points[j])
        for i in range(len(points))
        for j in range(i + 1, len(points))
    )


def all_edges_total_matrix(matrix: List[List[int]]) -> int:
    n = len(matrix)
    return sum(
        matrix[i][j]
        for i in range(n)
        for j in range(i + 1, n)
        if matrix[i][j] > 0
    )


def circle_layout(n: int) -> List[Tuple[float, float]]:
    """Рівномірно розміщує n вершин по колу на полотні."""
    cx = CANVAS_W / 2
    cy = CANVAS_H / 2
    r  = min(CANVAS_W, CANVAS_H) * 0.37
    return [
        (
            cx + r * math.cos(2 * math.pi * i / n - math.pi / 2),
            cy + r * math.sin(2 * math.pi * i / n - math.pi / 2),
        )
        for i in range(n)
    ]


# ═══════════════════════════════════════════════════════════════════════════════
#  ГОЛОВНИЙ ЗАСТОСУНОК
# ═══════════════════════════════════════════════════════════════════════════════

class IslandApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Задача про підводний кабель - алгоритм Прима")
        root.resizable(False, False)
        root.configure(bg=C_STATS_BG)

        self.islands: List[Tuple[float, float]] = []
        self.matrix:  Optional[List[List[int]]] = None
        self._last_mst_total: int = 0

        self._build_ui()
        self._reset_islands()

    # ── Побудова інтерфейсу ────────────────────────────────────────────────────
    def _build_ui(self):
        bold  = tkfont.Font(family="Helvetica", size=11, weight="bold")
        small = tkfont.Font(family="Helvetica", size=9)

        # ─ Статистична панель ─
        stats_frame = tk.Frame(self.root, bg=C_STATS_BG, pady=8, padx=12)
        stats_frame.pack(fill="x")

        for col, (title, attr, color) in enumerate([
            ("Острови",     "lbl_count", C_TEXT),
            ("Мін. кабель", "lbl_mst",   C_TEXT),
            ("Зекономлено", "lbl_saved", C_SAVED),
        ]):
            card = tk.Frame(stats_frame, bg="white", relief="flat",
                            highlightthickness=1, highlightbackground="#ddd")
            card.grid(row=0, column=col, padx=6, pady=4, sticky="nsew")
            stats_frame.columnconfigure(col, weight=1)
            tk.Label(card, text=title, font=small,
                     bg="white", fg=C_MUTED).pack(pady=(6, 0))
            lbl = tk.Label(card, text="—", font=bold, bg="white", fg=color)
            lbl.pack(pady=(0, 6))
            setattr(self, attr, lbl)

        # ─ Бейдж режиму ─
        bg, fg = C_BADGE_BLUE
        self.mode_badge = tk.Label(
            stats_frame, text="  ручний режим  ",
            font=small, bg=bg, fg=fg, relief="flat", padx=4, pady=2,
        )
        self.mode_badge.grid(row=1, column=0, columnspan=3,
                             padx=6, pady=(0, 4), sticky="w")

        # ─ Полотно ─
        self.canvas = tk.Canvas(
            self.root,
            width=CANVAS_W, height=CANVAS_H,
            bg=C_OCEAN, cursor="crosshair",
            highlightthickness=0,
        )
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self._on_left_click)
        self.canvas.bind("<Button-2>", self._on_right_click)   # macOS
        self.canvas.bind("<Button-3>", self._on_right_click)   # Win / Linux

        # ─ Панель кнопок ─
        footer = tk.Frame(self.root, bg=C_STATS_BG, padx=12, pady=6)
        footer.pack(fill="x")

        self.hint_lbl = tk.Label(
            footer,
            text="Лівий клік — додати острів  •  Правий клік — видалити",
            font=small, bg=C_STATS_BG, fg=C_MUTED,
        )
        self.hint_lbl.pack(side="left")

        for text, cmd in [
            ("Зберегти результат", self._save_result),
            ("Завантажити CSV",    self._load_csv),
            ("Скинути",            self._reset_islands),
        ]:
            tk.Button(
                footer, text=text, font=small, relief="flat",
                bg="#e8e8e4", activebackground="#d4d4d0",
                command=cmd,
            ).pack(side="right", padx=(4, 0))

    # ── Скидання до ручного режиму ─────────────────────────────────────────────
    def _reset_islands(self):
        self.matrix = None
        self.islands = [
            (rx * CANVAS_W, ry * CANVAS_H)
            for rx, ry in [
                (0.14, 0.28), (0.38, 0.65),
                (0.55, 0.22), (0.72, 0.62),
                (0.88, 0.32),
            ]
        ]
        self.canvas.configure(cursor="crosshair")
        bg, fg = C_BADGE_BLUE
        self.mode_badge.config(text="  ручний режим  ", bg=bg, fg=fg)
        self.hint_lbl.config(
            text="Лівий клік — додати острів  •  Правий клік — видалити"
        )
        self._redraw()

    # ── Завантаження CSV (використовує оригінальну read_adjacency_matrix) ──────
    def _load_csv(self):
        path = filedialog.askopenfilename(
            title="Оберіть файл матриці суміжності",
            filetypes=[
                ("CSV / текстові файли", "*.csv *.txt"),
                ("Усі файли", "*.*"),
            ],
        )
        if not path:
            return
        try:
            matrix = read_adjacency_matrix(path)
        except Exception as exc:
            messagebox.showerror("Помилка читання", str(exc))
            return

        n = len(matrix)
        if n < 2:
            messagebox.showwarning("Мало вершин",
                                   "Матриця повинна містити хоча б 2 вузли.")
            return

        self.matrix  = matrix
        self.islands = circle_layout(n)
        self.canvas.configure(cursor="arrow")

        bg, fg = C_BADGE_WARN
        fname = path.split("/")[-1].split("\\")[-1]
        self.mode_badge.config(
            text=f"  режим матриці  •  {n} островів  •  {fname}  ",
            bg=bg, fg=fg,
        )
        self.hint_lbl.config(
            text="Натисніть «Скинути», щоб повернутися до ручного режиму"
        )
        self._redraw()

    # ── Збереження результату (використовує оригінальну write_result_to_file) ──
    def _save_result(self):
        if self._last_mst_total == 0:
            messagebox.showinfo("Немає даних",
                                "Спочатку завантажте граф або додайте острови.")
            return
        path = filedialog.asksaveasfilename(
            title="Зберегти результат",
            initialfile="result.txt",
            defaultextension=".txt",
            filetypes=[("Текстовий файл", "*.txt")],
        )
        if not path:
            return
        write_result_to_file(self._last_mst_total, path)
        messagebox.showinfo(
            "Збережено",
            f"Результат {self._last_mst_total} записано у\n{path}",
        )

    # ── Обробники кліків (тільки в ручному режимі) ─────────────────────────────
    def _on_left_click(self, event):
        if self.matrix is not None:
            return
        self.islands.append((float(event.x), float(event.y)))
        self._redraw()

    def _on_right_click(self, event):
        if self.matrix is not None:
            return
        if not self.islands:
            return
        px, py = float(event.x), float(event.y)
        idx = min(range(len(self.islands)),
                  key=lambda i: _dist(self.islands[i], (px, py)))
        if _dist(self.islands[idx], (px, py)) < DELETE_R:
            self.islands.pop(idx)
            self._redraw()

    # ── Перемальовування ───────────────────────────────────────────────────────
    def _redraw(self):
        c = self.canvas
        c.delete("all")
        self._draw_ocean()

        if not self.islands:
            c.create_text(
                CANVAS_W // 2, CANVAS_H // 2,
                text="Клікніть, щоб додати перший острів",
                fill="white", font=("Helvetica", 14),
            )
            self._update_stats(0, 0)
            return

        if self.matrix is not None:
            self._draw_matrix_mode()
        else:
            self._draw_coord_mode()

        self._draw_islands()

    # ── Ручний режим ──────────────────────────────────────────────────────────
    def _draw_coord_mode(self):
        n = len(self.islands)
        if n < 2:
            self._update_stats(0, 0)
            return

        for i in range(n):
            for j in range(i + 1, n):
                x1, y1 = self.islands[i]
                x2, y2 = self.islands[j]
                self.canvas.create_line(x1, y1, x2, y2,
                                        fill=C_ALL_EDGE, width=1, dash=(5, 7))

        edges  = prim_mst_coords(self.islands)
        mst_px = sum(d for _, _, d in edges)
        all_px = all_edges_total_coords(self.islands)

        for a, b, d in edges:
            self._draw_mst_edge(a, b, round(d * KM_SCALE), "км")

        mst_km   = round(mst_px * KM_SCALE)
        saved_km = round(max(0, all_px - mst_px) * KM_SCALE)
        self._last_mst_total = mst_km
        self._update_stats(mst_km, saved_km, unit="км")

    # ── Режим матриці ─────────────────────────────────────────────────────────
    def _draw_matrix_mode(self):
        m = self.matrix

        # Усі ребра з матриці
        for i in range(len(m)):
            for j in range(i + 1, len(m)):
                if m[i][j] > 0:
                    x1, y1 = self.islands[i]
                    x2, y2 = self.islands[j]
                    self.canvas.create_line(x1, y1, x2, y2,
                                            fill=C_ALL_EDGE, width=1, dash=(5, 7))

        # calculate_minimum_cable_length — оригінальна функція для статистики
        mst_total = calculate_minimum_cable_length(m)
        # prim_mst_matrix — для відображення конкретних ребер
        mst_edges = prim_mst_matrix(m)
        all_total = all_edges_total_matrix(m)

        for a, b, w in mst_edges:
            self._draw_mst_edge(a, b, w, "")

        self._last_mst_total = mst_total
        self._update_stats(mst_total, max(0, all_total - mst_total), unit="")

    # ── Малювання одного ребра MST ────────────────────────────────────────────
    def _draw_mst_edge(self, a: int, b: int, weight: int, unit: str):
        x1, y1 = self.islands[a]
        x2, y2 = self.islands[b]
        self.canvas.create_line(x1, y1, x2, y2, fill=C_MST, width=3)

        mx, my  = (x1 + x2) / 2, (y1 + y2) / 2
        label   = f"{weight} {unit}".strip()
        half_w  = max(18, len(label) * 4)
        self.canvas.create_rectangle(
            mx - half_w, my - 11, mx + half_w, my + 3,
            fill=C_MST_BG, outline="",
        )
        self.canvas.create_text(mx, my - 4, text=label,
                                fill=C_MST_LABEL, font=("Helvetica", 9))

    # ── Фон — океан з хвилями ─────────────────────────────────────────────────
    def _draw_ocean(self):
        for y in range(WAVE_STEP, CANVAS_H, WAVE_STEP):
            pts: List[float] = []
            for x in range(0, CANVAS_W + 4, 4):
                wy = y + math.sin(x * WAVE_FREQ + y * 0.02) * WAVE_AMP
                pts += [x, wy]
            if len(pts) >= 4:
                self.canvas.create_line(pts, fill=C_WAVE, width=1, smooth=True)

    # ── Малювання островів ────────────────────────────────────────────────────
    def _draw_islands(self):
        for i, (x, y) in enumerate(self.islands):
            self.canvas.create_oval(
                x - ISLAND_R + 2, y - ISLAND_R + 3,
                x + ISLAND_R + 2, y + ISLAND_R + 3,
                fill="#0d4f7a", outline="",
            )
            self.canvas.create_oval(
                x - ISLAND_R, y - ISLAND_R,
                x + ISLAND_R, y + ISLAND_R,
                fill=C_ISLAND, outline=C_ISLAND_STR, width=2,
            )
            self.canvas.create_oval(x - 6, y - 6, x - 1, y - 1,
                                    fill=C_PALM, outline="")
            lbl = chr(65 + i) if i < 26 else str(i + 1)
            self.canvas.create_text(x + 3, y + 4, text=lbl,
                                    fill=C_LABEL, font=("Helvetica", 10, "bold"))

    # ── Оновлення лічильників ─────────────────────────────────────────────────
    def _update_stats(self, mst: int, saved: int, unit: str = "км"):
        self.lbl_count.config(text=str(len(self.islands)))
        suffix = f" {unit}" if unit else ""
        if mst == 0 and len(self.islands) < 2:
            self.lbl_mst.config(text="—")
            self.lbl_saved.config(text="—")
        else:
            self.lbl_mst.config(text=f"{mst}{suffix}")
            self.lbl_saved.config(text=f"{saved}{suffix}", fg=C_SAVED)


# ═══════════════════════════════════════════════════════════════════════════════
#  ТОЧКА ВХОДУ — підтримує обидва режими роботи
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Консольний режим (оригінальна логіка з islands.csv):
        python islands_visualizer.py --cli
    """
    import sys
    if "--cli" in sys.argv:
        input_file  = "islands.csv"
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
    else:
        root = tk.Tk()
        IslandApp(root)
        root.mainloop()


if __name__ == "__main__":
    main()