#!/usr/bin/env python3
"""
Завдання 3: Скрипт для аналізу файлів логів

Скрипт читає лог-файли, аналізує їх та виводить статистику за рівнями логування.
Підтримує фільтрацію записів за конкретним рівнем.

Використання:
    python task3.py /path/to/logfile.log
    python task3.py /path/to/logfile.log ERROR

Функціональне програмування:
    - Використання lambda-функцій
    - Списковий вираз (list comprehension)
    - Функції filter, map
    - Функції вищого порядку
"""

import sys
import re
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Callable
from collections import defaultdict


def parse_log_line(line: str) -> Optional[Dict[str, str]]:
    """
    Парсить рядок логу та повертає словник з компонентами.
    
    Формат логу: YYYY-MM-DD HH:MM:SS LEVEL Message
    
    Args:
        line (str): Рядок з логу для парсингу
        
    Returns:
        Optional[Dict[str, str]]: Словник з компонентами або None при помилці
        
    Example:
        >>> parse_log_line("2024-01-22 08:30:01 INFO User logged in successfully.")
        {
            'date': '2024-01-22',
            'time': '08:30:01',
            'level': 'INFO',
            'message': 'User logged in successfully.'
        }
    """
    # Регулярний вираз для парсингу логів
    # Групи: (дата) (час) (рівень) (повідомлення)
    pattern = r'^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+(\w+)\s+(.+)$'
    
    match = re.match(pattern, line.strip())
    if match:
        return {
            'date': match.group(1),
            'time': match.group(2),
            'level': match.group(3).upper(),
            'message': match.group(4)
        }
    return None


def load_logs(file_path: str) -> List[Dict[str, str]]:
    """
    Завантажує та парсить лог-файл.
    
    Args:
        file_path (str): Шлях до лог-файлу
        
    Returns:
        List[Dict[str, str]]: Список розпарсених записів логу
        
    Raises:
        FileNotFoundError: Якщо файл не знайдено
        PermissionError: Якщо немає доступу до файлу
        UnicodeDecodeError: Якщо проблеми з кодуванням
    """
    logs = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Використовуємо list comprehension та filter для функціонального стилю
            # Спочатку парсимо всі рядки, потім фільтруємо None значення
            parsed_lines = [parse_log_line(line) for line in file]
            logs = list(filter(lambda x: x is not None, parsed_lines))
            
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{file_path}' не знайдено")
    except PermissionError:
        raise PermissionError(f"Немає доступу до файлу '{file_path}'")
    except UnicodeDecodeError:
        raise UnicodeDecodeError("Помилка декодування файлу. Перевірте кодування")
    
    return logs


def filter_logs_by_level(logs: List[Dict[str, str]], level: str) -> List[Dict[str, str]]:
    """
    Фільтрує записи логу за рівнем логування.
    
    Args:
        logs (List[Dict[str, str]]): Список записів логу
        level (str): Рівень логування для фільтрації
        
    Returns:
        List[Dict[str, str]]: Відфільтровані записи логу
        
    Example:
        >>> logs = [{'level': 'INFO', 'message': 'test'}, {'level': 'ERROR', 'message': 'fail'}]
        >>> filter_logs_by_level(logs, 'ERROR')
        [{'level': 'ERROR', 'message': 'fail'}]
    """
    # Використовуємо lambda-функцію з filter для функціонального програмування
    return list(filter(lambda log: log['level'].upper() == level.upper(), logs))


def count_logs_by_level(logs: List[Dict[str, str]]) -> Dict[str, int]:
    """
    Підраховує кількість записів за кожним рівнем логування.
    
    Args:
        logs (List[Dict[str, str]]): Список записів логу
        
    Returns:
        Dict[str, int]: Словник з підрахунком за рівнями
        
    Example:
        >>> logs = [{'level': 'INFO'}, {'level': 'ERROR'}, {'level': 'INFO'}]
        >>> count_logs_by_level(logs)
        {'INFO': 2, 'ERROR': 1}
    """
    counts = defaultdict(int)
    
    # Використовуємо функціональний підхід з map
    levels = map(lambda log: log['level'], logs)
    
    # Підраховуємо кожен рівень
    for level in levels:
        counts[level] += 1
    
    return dict(counts)


def display_log_counts(counts: Dict[str, int]) -> None:
    """
    Виводить статистику підрахунку рівнів логування у вигляді таблиці.
    
    Args:
        counts (Dict[str, int]): Словник з підрахунком за рівнями
    """
    if not counts:
        print("Не знайдено жодних записів логу")
        return
    
    print("\n" + "="*50)
    print("Статистика рівнів логування:")
    print("="*50)
    print(f"{'Рівень логування':<20} | {'Кількість':<10}")
    print("-" * 50)
    
    # Сортуємо рівні за алфавітом для консистентного виводу
    sorted_levels = sorted(counts.items(), key=lambda x: x[0])
    
    for level, count in sorted_levels:
        print(f"{level:<20} | {count:<10}")
    
    print("-" * 50)
    total = sum(counts.values())
    print(f"{'Загалом':<20} | {total:<10}")
    print("="*50)


def display_filtered_logs(logs: List[Dict[str, str]], level: str) -> None:
    """
    Виводить відфільтровані записи логу для конкретного рівня.
    
    Args:
        logs (List[Dict[str, str]]): Відфільтровані записи логу
        level (str): Рівень логування
    """
    if not logs:
        print(f"\nНе знайдено записів рівня '{level.upper()}'")
        return
    
    print(f"\n{'='*80}")
    print(f"Записи рівня '{level.upper()}' (знайдено {len(logs)}):")
    print("="*80)
    
    # Використовуємо lambda для форматування виводу
    format_log = lambda log: f"{log['date']} {log['time']} {log['level']} {log['message']}"
    
    for log in logs:
        print(format_log(log))
    
    print("="*80)


def create_log_analyzer() -> Callable[[str, Optional[str]], None]:
    """
    Створює функцію-аналізатор логів (приклад функції вищого порядку).
    
    Returns:
        Callable: Функція для аналізу логів
    """
    def analyze_logs(file_path: str, filter_level: Optional[str] = None) -> None:
        """Аналізує лог-файл та виводить результати"""
        try:
            # Завантажуємо логи
            logs = load_logs(file_path)
            
            if not logs:
                print("Файл логів порожній або не містить коректних записів")
                return
            
            # Якщо вказано рівень для фільтрації
            if filter_level:
                filtered_logs = filter_logs_by_level(logs, filter_level)
                display_filtered_logs(filtered_logs, filter_level)
            else:
                # Виводимо загальну статистику
                counts = count_logs_by_level(logs)
                display_log_counts(counts)
                
                # Додаткова інформація
                print(f"\nЗагальна кількість записів: {len(logs)}")
                
                # Знаходимо найчастіший рівень за допомогою функціонального програмування
                if counts:
                    most_common_level = max(counts.items(), key=lambda x: x[1])
                    print(f"Найчастіший рівень: {most_common_level[0]} ({most_common_level[1]} разів)")
        
        except Exception as e:
            print(f"Помилка при обробці файлу: {e}")
    
    return analyze_logs


def main() -> None:
    """
    Головна функція скрипту.
    Обробляє аргументи командного рядка та запускає аналіз.
    """
    parser = argparse.ArgumentParser(
        description="Аналізатор файлів логів",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Приклади використання:
  %(prog)s /path/to/logfile.log
  %(prog)s /path/to/logfile.log ERROR
  %(prog)s /path/to/logfile.log info
        """
    )
    
    parser.add_argument(
        'file_path',
        help='Шлях до лог-файлу'
    )
    
    parser.add_argument(
        'level',
        nargs='?',
        help='Рівень логування для фільтрації (INFO, ERROR, DEBUG, WARNING)'
    )
    
    args = parser.parse_args()
    
    # Перевіряємо існування файлу
    if not Path(args.file_path).exists():
        print(f"Помилка: Файл '{args.file_path}' не існує")
        sys.exit(1)
    
    # Створюємо та використовуємо аналізатор
    analyzer = create_log_analyzer()
    analyzer(args.file_path, args.level)


if __name__ == "__main__":
    main()
