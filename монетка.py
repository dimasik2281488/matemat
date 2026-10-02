def find_fake(coin_weights):
    # Первое взвешивание: [0] vs [1]
    balance_1 = coin_weights[0] - coin_weights[1]
    
    # Второе взвешивание сравниваем с эталонной монетой 2
    # Если баланс был равен нулю — подозреваемые монеты 3 и 4
    # Иначе — подозреваемая монета это первая из первой пары
    suspect_index = int(balance_1 == 0) * 2 + int(balance_1 != 0)

    # Проверяем подозреваемого против эталона
    balance_2 = coin_weights[suspect_index] - coin_weights[2]

    # Определяем дефектную монету
    #   - если баланс изменился на ноль  вторая в паре
    #   - иначе та, что проверили
    fake_index = suspect_index if bool(balance_2) else suspect_index ^ 1
    
    # Тип дефекта определяется знаком первого баланса
    defect_type = 'тяжелее' * (balance_1 > 0) or 'легче'

    return f'Фальшивая {fake_index + 1}, {defect_type}'