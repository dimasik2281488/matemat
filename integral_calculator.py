"""Калькулятор"""
import csv
import math
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


SAFE_NAMES = {k: v for k, v in vars(math).items() if not k.startswith("_")}
SAFE_NAMES["abs"] = abs

PRESETS = {
    "x**2 + 2*x + 1": "x**2 + 2*x + 1",
    "sin(x) + exp(-x)": "sin(x) + exp(-x)",
    "1/x": "1/x",
    "sqrt(x)": "sqrt(x)",
    "cos(x)": "cos(x)",
}

METHODS = [
    "Прямоугольники (левые)",
    "Прямоугольники (правые)",
    "Прямоугольники (средние)",
    "Трапеций",
    "Симпсона",
]


def make_function(expr):
    expr = expr.strip().replace("^", "**")
    if not expr:
        raise ValueError("Введите функцию f(x).")
    try:
        code = compile(expr, "<f>", "eval")
    except SyntaxError:
        raise ValueError("Синтаксическая ошибка в выражении функции.")
    for name in code.co_names:
        if name != "x" and name not in SAFE_NAMES:
            raise ValueError(f"Неизвестное имя в выражении: «{name}».")

    def f(x):
        return eval(code, {"__builtins__": {}}, {**SAFE_NAMES, "x": x})

    return f


def build_table(f, a, b, n):
    h = (b - a) / n
    rows = []
    for i in range(n + 1):
        x = a + i * h
        try:
            y = float(f(x))
            if math.isnan(y) or math.isinf(y):
                raise ValueError
            rows.append((x, y, ""))
        except ZeroDivisionError:
            rows.append((x, None, "деление на ноль"))
        except Exception:
            rows.append((x, None, "ошибка вычисления"))
    return rows


def integrate(f, a, b, n, method):
    h = (b - a) / n
    if method == "Прямоугольники (левые)":
        return h * sum(f(a + i * h) for i in range(n))
    if method == "Прямоугольники (правые)":
        return h * sum(f(a + i * h) for i in range(1, n + 1))
    if method == "Прямоугольники (средние)":
        return h * sum(f(a + (i + 0.5) * h) for i in range(n))
    if method == "Трапеций":
        return h * (f(a) / 2 + sum(f(a + i * h) for i in range(1, n)) + f(b) / 2)
    if method == "Симпсона":
        if n % 2:
            raise ValueError("Для метода Симпсона число шагов N должно быть чётным.")
        s = f(a) + f(b)
        s += 4 * sum(f(a + i * h) for i in range(1, n, 2))
        s += 2 * sum(f(a + i * h) for i in range(2, n, 2))
        return s * h / 3
    raise ValueError("Неизвестный метод.")


# ---------- ИНТЕРФЕЙС ----------

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Калькулятор интегралов")
        self.report = None  # данные последнего расчёта
        self.build()

    def build(self):
        form = ttk.Frame(self, padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="f(x) =").grid(row=0, column=0, sticky="e")
        self.func = ttk.Combobox(form, values=list(PRESETS), width=30)
        self.func.set("x**2 + 2*x + 1")
        self.func.grid(row=0, column=1, columnspan=3, sticky="we", pady=2)

        self.a = self.field(form, "a (нижняя):", 1, 0, "0")
        self.b = self.field(form, "b (верхняя):", 1, 2, "1")

        ttk.Label(form, text="Шаги:").grid(row=2, column=0, sticky="e")
        self.mode = tk.StringVar(value="N")
        ttk.Radiobutton(form, text="число шагов N", variable=self.mode, value="N").grid(row=2, column=1, sticky="w")
        ttk.Radiobutton(form, text="шаг h", variable=self.mode, value="h").grid(row=2, column=2, sticky="w")
        self.step = ttk.Entry(form, width=10)
        self.step.insert(0, "10")
        self.step.grid(row=2, column=3, sticky="w")

        ttk.Label(form, text="Метод:").grid(row=3, column=0, sticky="e")
        self.method = ttk.Combobox(form, values=METHODS, state="readonly", width=30)
        self.method.current(3)
        self.method.grid(row=3, column=1, columnspan=3, sticky="we", pady=2)

        self.exact = self.field(form, "Эталон (опц.):", 4, 0, "")

        btns = ttk.Frame(self, padding=(10, 0))
        btns.pack(fill="x")
        ttk.Button(btns, text="Рассчитать", command=self.calculate).pack(side="left", padx=2)
        ttk.Button(btns, text="Сохранить в CSV", command=lambda: self.save("csv")).pack(side="left", padx=2)
        ttk.Button(btns, text="Сохранить в TXT", command=lambda: self.save("txt")).pack(side="left", padx=2)

        self.result = ttk.Label(self, text="", padding=10, font=("Arial", 10, "bold"))
        self.result.pack(fill="x")

        self.tree = ttk.Treeview(self, columns=("i", "x", "fx", "note"), show="headings", height=12)
        for col, title, w in (("i", "i", 40), ("x", "x", 120), ("fx", "f(x)", 140), ("note", "Примечание", 140)):
            self.tree.heading(col, text=title)
            self.tree.column(col, width=w)
        self.tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def field(self, parent, text, row, col, default):
        ttk.Label(parent, text=text).grid(row=row, column=col, sticky="e")
        entry = ttk.Entry(parent, width=12)
        entry.insert(0, default)
        entry.grid(row=row, column=col + 1, sticky="w", pady=2)
        return entry

    def number(self, entry, name):
        try:
            return float(entry.get().replace(",", "."))
        except ValueError:
            raise ValueError(f"Поле «{name}» должно быть числом.")

    def calculate(self):
        try:
            f = make_function(self.func.get())
            a = self.number(self.a, "a")
            b = self.number(self.b, "b")
            if not a < b:
                raise ValueError("Должно выполняться a < b.")
            value = self.number(self.step, "Шаги")
            if self.mode.get() == "N":
                n = int(value)
                if n != value:
                    raise ValueError("N должно быть целым числом.")
            else:
                if value <= 0:
                    raise ValueError("Шаг h должен быть больше 0.")
                n = max(1, round((b - a) / value))
            if n <= 0:
                raise ValueError("Число шагов N должно быть больше 0.")
            method = self.method.get()
            rows = build_table(f, a, b, n)
            try:
                integral = integrate(f, a, b, n, method)
            except ZeroDivisionError:
                raise ValueError("Деление на ноль в точках интегрирования.")
            except OverflowError:
                raise ValueError("Слишком большие значения при вычислении.")
            except ValueError as e:
                raise ValueError(str(e) or "Функция не определена на отрезке.")
            exact_text = self.exact.get().strip()
            error = None
            if exact_text:
                error = abs(integral - self.number(self.exact, "Эталон"))
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
            return
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось вычислить: {e}")
            return

        self.tree.delete(*self.tree.get_children())
        bad = 0
        for i, (x, y, note) in enumerate(rows):
            if y is None:
                bad += 1
            self.tree.insert("", "end", values=(i, f"{x:.6g}", "—" if y is None else f"{y:.8g}", note))
        text = f"Интеграл ≈ {integral:.10g}"
        if error is not None:
            text += f"   |   погрешность: {error:.3g}"
        if bad:
            text += f"   |   пропущено точек: {bad}"
        self.result.config(text=text)
        self.report = {
            "func": self.func.get(), "a": a, "b": b, "n": n, "h": (b - a) / n,
            "method": method, "integral": integral, "error": error, "rows": rows,
        }

    def save(self, kind):
        if not self.report:
            messagebox.showinfo("Нет данных", "Сначала нажмите «Рассчитать».")
            return
        r = self.report
        path = filedialog.asksaveasfilename(defaultextension=f".{kind}", filetypes=[(kind.upper(), f"*.{kind}")])
        if not path:
            return
        try:
            if kind == "csv":
                with open(path, "w", newline="", encoding="utf-8-sig") as f:
                    w = csv.writer(f, delimiter=";")
                    w.writerow(["i", "x", "f(x)", "примечание"])
                    for i, (x, y, note) in enumerate(r["rows"]):
                        w.writerow([i, x, "" if y is None else y, note])
            else:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(f"Функция: {r['func']}\n")
                    f.write(f"Границы: a = {r['a']}, b = {r['b']}\n")
                    f.write(f"Число шагов: {r['n']} (h = {r['h']:.6g})\n")
                    f.write(f"Метод: {r['method']}\n")
                    f.write(f"Значение интеграла: {r['integral']:.10g}\n")
                    if r["error"] is not None:
                        f.write(f"Погрешность: {r['error']:.3g}\n")
                    f.write("\n   i |            x |         f(x) | примечание\n")
                    for i, (x, y, note) in enumerate(r["rows"]):
                        fx = "—" if y is None else f"{y:.8g}"
                        f.write(f"{i:4} | {x:12.6g} | {fx:>12} | {note}\n")
            messagebox.showinfo("Готово", f"Сохранено: {path}")
        except OSError as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")


if __name__ == "__main__":
    App().mainloop()
