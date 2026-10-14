def dense_layer(x, W, b):
    """
    Полносвязный слой:
    y = W * x + b
    """


    if len(W) != len(b):
        raise ValueError(
            "Количество строк матрицы W должно совпадать "
            "с количеством элементов вектора b."
        )


    for row in W:
        if len(row) != len(x):
            raise ValueError(
                "Количество столбцов матрицы W должно "
                "совпадать с размером входного вектора x."
            )


    y = []

    for i in range(len(W)):
        total = 0

        for j in range(len(x)):
            total += W[i][j] * x[j]

        total += b[i]
        y.append(total)

    return y


def main():
    try:
        print("=== Симулятор полносвязного слоя ===")

        M = int(input("Введите размер входного вектора M: "))
        N = int(input("Введите размер выходного слоя N: "))

        if M <= 0 or N <= 0:
            raise ValueError(
                "Размерности M и N должны быть положительными."
            )


        x = []
        print("\nВведите элементы входного вектора x:")

        for i in range(M):
            value = float(input(f"x[{i}] = "))
            x.append(value)


        W = []
        print(f"\nВведите матрицу весов W ({N} x {M}):")

        for i in range(N):
            row = []

            for j in range(M):
                value = float(input(f"W[{i}][{j}] = "))
                row.append(value)

            W.append(row)


        b = []
        print(f"\nВведите вектор смещений b ({N} элементов):")

        for i in range(N):
            value = float(input(f"b[{i}] = "))
            b.append(value)


        if len(x) != M:
            raise ValueError("Неверный размер входного вектора.")

        if len(W) != N:
            raise ValueError("Неверное количество строк матрицы W.")

        if any(len(row) != M for row in W):
            raise ValueError(
                "Каждая строка W должна содержать M элементов."
            )

        if len(b) != N:
            raise ValueError(
                "Размер вектора b должен совпадать с N."
            )


        y = dense_layer(x, W, b)

        
        print("\n=== Результат ===")
        print("Входной вектор x:", x)
        print("Матрица весов W:", W)
        print("Вектор смещений b:", b)
        print("Выходной вектор y:", y)

    except ValueError as error:
        print("\nОшибка ввода или размерностей:", error)

    except Exception as error:
        print("\nНепредвиденная ошибка:", error)


if __name__ == "__main__":
    main()