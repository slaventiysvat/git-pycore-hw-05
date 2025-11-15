#!/usr/bin/env python3
"""
Завдання 1: Реалізація функції caching_fibonacci з використанням замикань

Функція створює та використовує кеш для зберігання й повторного використання
вже обчислених значень чисел Фібоначчі.

Ряд Фібоначчі: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
Формула: F(n) = F(n-1) + F(n-2), де F(0) = 0, F(1) = 1
"""


def caching_fibonacci():
    """
    Створює функцію fibonacci з кешуванням результатів.
    
    Використовує замикання для збереження кешу між викликами.
    
    Returns:
        function: Внутрішня функція fibonacci(n) з кешуванням
    """
    # Словник для кешування вже обчислених значень
    cache = {}
    
    def fibonacci(n):
        """
        Обчислює n-е число Фібоначчі з використанням кешування.
        
        Args:
            n (int): Номер елементу в послідовності Фібоначчі (n >= 0)
            
        Returns:
            int: n-е число Фібоначчі
            
        Raises:
            ValueError: Якщо n < 0
        """
        # Перевірка на коректність вхідного параметра
        if n < 0:
            raise ValueError("Номер елементу послідовності не може бути від'ємним")
        
        # Перевіряємо, чи є значення в кеші
        if n in cache:
            return cache[n]
        
        # Базові випадки послідовності Фібоначчі
        if n == 0:
            result = 0
        elif n == 1:
            result = 1
        else:
            # Рекурсивне обчислення з використанням кешу
            result = fibonacci(n - 1) + fibonacci(n - 2)
        
        # Зберігаємо результат в кеш
        cache[n] = result
        return result
    
    # Повертаємо внутрішню функцію (замикання)
    return fibonacci


# Демонстрація роботи функції
if __name__ == "__main__":
    # Створюємо функцію fibonacci з кешуванням
    fib = caching_fibonacci()
    
    # Тестуємо на декількох значеннях
    test_values = [0, 1, 5, 10, 15, 20]
    
    print("Демонстрація роботи caching_fibonacci:")
    print("=" * 40)
    
    for n in test_values:
        result = fib(n)
        print(f"F({n}) = {result}")
    
    print("\nПерші 21 число Фібоначчі:")
    print("=" * 40)
    fibonacci_sequence = [fib(i) for i in range(21)]
    print(fibonacci_sequence)
