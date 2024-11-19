# Тестовая программа: применение popcnt поэлементно

import json
import struct

def apply_popcnt_to_vector():
    # Исходный вектор
    vector = [15, 3, 8, 7, 31, 5, 2, 10]
    
    # Массив для хранения результата
    results = []

    # Этап 1: Применение popcnt к каждому элементу
    for i in range(8):
        # Применение popcnt
        count = bin(vector[i]).count('1')
        results.append(count)
        
        # Запись результата в регистр (эмулируем запись)
        vector[i] = count

    # Этап 2: Печать результатов
    print("Исходный вектор после применения popcnt: ")
    print(vector)

    return vector

# Запуск функции
apply_popcnt_to_vector()
