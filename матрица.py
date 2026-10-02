# Функция для проверки совместимости матриц
def check_size(A, B):
    if len(A[0]) != len(B): # Проверка при умножении
        raise ValueError("Матрицы нельзя перемножить!")
    elif len(A) != len(B) or len(A[0]) != len(B[0]): # Проверка при сложении
        raise ValueError("Матрицы должны быть одинакового размера!")

# Сложение двух матриц
def matrix_add(A, B):
    check_size(A, B)
    
    result = []
    for i in range(len(A)):
        row = []                     # Создаем новую строку
        for j in range(len(A[i])):  
            row.append(A[i][j] + B[i][j])
        result.append(row)
    return result


# Транспонирование матрицы
def matrix_transpose(A):
    rows = len(A)
    cols = len(A[0])
    
    T = [[None]*rows for _ in range(cols)] # Готовим пустую матрицу нужного размера
    
    for i in range(rows):
        for j in range(cols):
            T[j][i] = A[i][j]
    return T


# Перемножение матриц
def matrix_multiply(A, B):
    check_size(A, B)
    
    rows_A = len(A)
    cols_B = len(B[0])
    
    M = [[0]*cols_B for _ in range(rows_A)]
    
    for i in range(rows_A):
        for k in range(cols_B):
            # Вычисляем один элемент новой матрицы как скалярное произведение строк/столбцов
            for j in range(len(B)):   
                M[i][k] += A[i][j] * B[j][k]
    return M


# Пример использования функций
if __name__ == "__main__":
    # Матрица из задания
    A = [
        [1, 2],
        [3, 0]
    ]

    B = [
        [4, 1],
        [-2, 5]
    ]

    # Вручную считаем выражение C = (A + BT) · A
    BT = matrix_transpose(B)
    summa = matrix_add(A, BT)
    C = matrix_multiply(summa, A)

    print(" Результат вычисления выражения:")
    for row in C:
        print(*row)