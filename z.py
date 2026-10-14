import math

print(" Симулятор перемещения персонажа              ")


x_a = float(input("Введите x координаты точки A: "))
y_a = float(input("Введите y координаты точки A: "))


x_u = float(input("Введите x компоненты вектора u: "))
y_u = float(input("Введите y компоненты вектора u: "))


x_v = float(input("Введите x компоненты вектора v: "))
y_v = float(input("Введите y компоненты вектора v: "))


length_u = math.sqrt(x_u**2 + y_u**2)
length_v = math.sqrt(x_v**2 + y_v**2)


x_r = x_u + x_v
y_r = y_u + y_v


x_b = x_a + x_r
y_b = y_a + y_r


total_length = length_u + length_v


print("\n=== Результаты перемещения ===")
print(f"Начальная точка A: ({x_a}, {y_a})")
print(f"Результирующий вектор r: ({x_r}, {y_r})")
print(f"Конечная точка B: ({x_b}, {y_b})")
print(f"Длина первого перемещения: {length_u:.2f}")
print(f"Длина второго перемещения: {length_v:.2f}")
print(f"Общая длина пути: {total_length:.2f}")