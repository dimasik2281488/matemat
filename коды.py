import random

def generate_safe_pin():
    # Генерируем случайные цифры от 0 до 9
    digits = [random.randint(0, 9) for _ in range(4)]
    
    # Проверка запрета №1: все цифры одинаковые
    if len(set(digits)) == 1:
        return False
    
    # Проверка запрета №2: цифры идут строго по порядку
    sorted_digits = sorted(digits)
    is_ordered = all(sorted_digits[i] + 1 == sorted_digits[i+1] 
                     for i in range(len(sorted_digits)-1))
    
    # Если хотя бы одно из условий не выполнено — генерируем новый PIN-код
    if is_ordered:
        return False
    
    # Преобразуем список цифр в строку и возвращаем результат
    return ''.join(map(str, digits))

# Пример использования функции
while True:
    pin_code = generate_safe_pin()
    if pin_code:
        print(f" Сгенерирован безопасный PIN-код: {pin_code}")
        break