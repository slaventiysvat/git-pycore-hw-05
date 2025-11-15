#!/usr/bin/env python3
"""
Завдання 2: Генератор чисел та обчислення прибутку

Реалізація функцій:
1. generator_numbers - генератор для пошуку дійсних чисел у тексті
2. sum_profit - функція для підсумовування чисел за допомогою генератора

Використовує регулярні вирази та yield для ефективної обробки текстових даних.
"""

import re
from typing import Iterator, Callable


def generator_numbers(text: str) -> Iterator[float]:
    """
    Генератор, що аналізує текст і повертає всі дійсні числа.
    
    Функція використовує регулярні вирази для пошуку чисел у тексті.
    Числа можуть бути цілими або з плаваючою комою, відокремлені пробілами.
    
    Args:
        text (str): Вхідний текст для аналізу
        
    Yields:
        float: Дійсні числа, знайдені в тексті
        
    Examples:
        >>> list(generator_numbers("Дохід: 1000.50 та 250"))
        [1000.5, 250.0]
        
        >>> list(generator_numbers("Немає чисел тут"))
        []
    """
    # Регулярний вираз для пошуку дійсних чисел
    # \b - межа слова, щоб число було відокремлене
    # \d+ - одна або більше цифр
    # (?:\.\d+)? - необов'язкова десяткова частина
    pattern = r'\b\d+(?:\.\d+)?\b'
    
    # Знаходимо всі співпадіння в тексті
    matches = re.finditer(pattern, text)
    
    # Повертаємо кожне знайдене число як float
    for match in matches:
        yield float(match.group())


def sum_profit(text: str, func: Callable[[str], Iterator[float]]) -> float:
    """
    Обчислює загальну суму чисел у тексті, використовуючи передану функцію-генератор.
    
    Args:
        text (str): Вхідний текст для аналізу
        func (Callable): Функція-генератор для отримання чисел з тексту
        
    Returns:
        float: Загальна сума всіх чисел у тексті
        
    Examples:
        >>> sum_profit("Дохід 100.5 і 200", generator_numbers)
        300.5
        
        >>> sum_profit("Немає чисел", generator_numbers)
        0.0
    """
    # Використовуємо генератор для отримання всіх чисел і підсумовуємо їх
    return sum(func(text))


def format_currency(amount: float, currency: str = "₴") -> str:
    """
    Допоміжна функція для форматування суми як валюти.
    
    Args:
        amount (float): Сума для форматування
        currency (str): Символ валюти (за замовчуванням гривня)
        
    Returns:
        str: Відформатована сума
    """
    return f"{amount:.2f} {currency}"


# Демонстрація роботи функцій
if __name__ == "__main__":
    # Тестові дані згідно з прикладом
    text = ("Загальний дохід працівника складається з декількох частин: "
            "1000.01 як основний дохід, доповнений додатковими надходженнями "
            "27.45 і 324.00 доларів.")
    
    print("=== Демонстрація роботи generator_numbers та sum_profit ===")
    print("=" * 60)
    print()
    
    print("Вхідний текст:")
    print(f'"{text}"')
    print()
    
    # Демонстрація роботи генератора
    print("Знайдені числа:")
    numbers_found = list(generator_numbers(text))
    for i, number in enumerate(numbers_found, 1):
        print(f"  {i}. {number}")
    
    print()
    
    # Обчислення загального прибутку
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")
    print(f"Загальний дохід (форматований): {format_currency(total_income, '$')}")
    
    print()
    print("=== Додаткові тести ===")
    print("=" * 30)
    
    # Тести з різними форматами чисел
    test_cases = [
        "Прибуток за місяць: 15000 гривень",
        "Витрати склали 250.75 та 1340.50",
        "Інвестиції: 50000.00, дивіденди: 2500.25, бонуси: 750",
        "Немає жодних чисел у цьому реченні",
        "Змішані дані: abc123.45def 678.90 xyz",
        "Негативні не підтримуються: -100.50, але 200.25 підтримується"
    ]
    
    for i, test_text in enumerate(test_cases, 1):
        numbers = list(generator_numbers(test_text))
        total = sum_profit(test_text, generator_numbers)
        
        print(f"Тест {i}:")
        print(f"  Текст: \"{test_text}\"")
        print(f"  Числа: {numbers}")
        print(f"  Сума: {total}")
        print()
    
    # Демонстрація використання з іншим генератором
    def generator_integers_only(text: str) -> Iterator[float]:
        """Генератор, що повертає тільки цілі числа"""
        pattern = r'\b\d+\b'
        for match in re.finditer(pattern, text):
            # Перевіряємо, що це не частина десяткового числа
            if (match.start() == 0 or text[match.start()-1] != '.') and \
               (match.end() == len(text) or text[match.end()] != '.'):
                yield float(match.group())
    
    print("=== Тест з альтернативним генератором (тільки цілі числа) ===")
    test_text = "Доходи: 1000.50 основний, 250 бонус, 75.25 премія"
    
    print(f"Текст: \"{test_text}\"")
    print(f"Всі числа: {list(generator_numbers(test_text))}")
    print(f"Тільки цілі: {list(generator_integers_only(test_text))}")
    print(f"Сума всіх: {sum_profit(test_text, generator_numbers)}")
    print(f"Сума цілих: {sum_profit(test_text, generator_integers_only)}")
