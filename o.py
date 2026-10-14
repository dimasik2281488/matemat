def input_vector():
    print ("Введите координаты вектора x:")
    x1 = float(input("x1 = "))
    x2 = float(input("x2 = "))
    return [x1, x2]

def input_matrix(name):
    print (f"\nВведите элементы матрицы {name} (2x2):")
    matrix = []

    for i in range(2):
        row = []
        for j in range(2):
            value = float(input(f"{name}[{i + 1} [{j + 1}] = "))
            row.append(value)
        matrix.append(row)

    return matrix

def multiply_matrix_vector(matrix, vector):
    result = []
    for i in range (2):
        value = 0
        for j in range (2):
            value += matrix[i][j] * vector[j]
        result.append(value)

    return result

def multiply_matrices(A, B):
    result = [[0, 0], [0, 0]]

    for i in range(2):
        for j in range(2):
            for k in range(2):
                result[i][j] += A[i][k] * B[k][j]

    return result


def print_matrix(name, matrix):
    print(name)
    for row in matrix:
        print(["{:.4f}".format(value) for value in row])


def print_vector(name, vector):
    print(name, [round(value, 4) for value in vector])



x = input_vector()
R = input_matrix("R")
S = input_matrix("S")


x1 = multiply_matrix_vector(R, x)


x2 = multiply_matrix_vector(S, x1)


T = multiply_matrices(S, R)


check = multiply_matrix_vector(T, x)


print("\n=== РЕЗУЛЬТАТЫ ===")

print_vector("Исходный вектор x:", x)
print_matrix("Матрица поворота R:", R)
print_matrix("Матрица масштабирования S:", S)

print_vector("Промежуточные координаты x1 = R*x:", x1)
print_vector("Итоговые координаты x2 = S*x1:", x2)

print_matrix("Матрица общего преобразования T = S*R:", T)
print_vector("Результат T*x:", check)


if all(abs(check[i] - x2[i]) < 1e-9 for i in range(2)):
    print("Проверка пройдена: T*x = x2")
else:
    print("Проверка не пройдена")
