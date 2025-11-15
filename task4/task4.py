#!/usr/bin/env python3
"""
Завдання 4: Консольний бот-помічник з обробкою помилок через декоратори

Удосконалена версія бота з попереднього завдання, що включає:
- Декоратор input_error для обробки помилок введення користувача
- Обробку винятків KeyError, ValueError, IndexError
- Зрозумілі повідомлення про помилки без завершення програми
"""

from __future__ import annotations
from typing import Dict, Tuple, Callable, Any
import functools


def input_error(func: Callable) -> Callable:
    """
    Декоратор для обробки помилок введення користувача.
    
    Обробляє винятки:
    - KeyError: коли ім'я контакту не знайдено
    - ValueError: коли недостатньо аргументів або неправильний формат
    - IndexError: коли недостатньо аргументів у списку
    
    Args:
        func (Callable): Функція-обробник команди
        
    Returns:
        Callable: Обгорнута функція з обробкою помилок
    """
    @functools.wraps(func)
    def inner(*args, **kwargs) -> str:
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            # Обробка випадку, коли контакт не знайдено
            contact_name = str(e).strip("'\"")
            return f"Contact '{contact_name}' not found."
        except ValueError as e:
            # Обробка різних випадків ValueError
            error_msg = str(e).lower()
            
            if "not enough values to unpack" in error_msg:
                return "Enter the argument for the command"
            elif "phone" in error_msg:
                return "Give me name and phone please."
            elif "name" in error_msg:
                return "Enter user name"
            else:
                return "Invalid format. Please check your input."
        except IndexError as e:
            # Обробка випадку недостатньої кількості аргументів
            error_msg = str(e).lower()
            if "search query" in error_msg:
                return "Enter search query"
            return "Enter the argument for the command"
        except Exception as e:
            # Загальна обробка інших помилок
            return f"An error occurred: {str(e)}"
    
    return inner


# -------------------- Парсер команд --------------------

def parse_input(user_input: str) -> Tuple[str, ...]:
    """
    Парсить введення користувача на команду та аргументи.
    
    Args:
        user_input (str): Рядок введення користувача
        
    Returns:
        Tuple[str, ...]: Кортеж з командою та аргументами
    """
    if not isinstance(user_input, str):
        return ("",)
    
    parts = user_input.strip().split()
    if not parts:
        return ("",)
    
    cmd, *args = parts
    cmd = cmd.strip().lower()
    return (cmd, *args)


# -------------------- Обробники команд --------------------

@input_error
def add_contact(args: Tuple[str, ...], contacts: Dict[str, str]) -> str:
    """
    Додає новий контакт до адресної книги.
    
    Args:
        args: Кортеж з іменем та телефоном
        contacts: Словник контактів
        
    Returns:
        str: Повідомлення про результат операції
        
    Raises:
        ValueError: Якщо недостатньо аргументів
    """
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    
    name, phone = args[0], args[1]
    
    # Перевіряємо, чи не порожні значення
    if not name.strip() or not phone.strip():
        raise ValueError("Give me name and phone please.")
    
    # Перевіряємо, чи контакт уже існує
    if name in contacts:
        return f"Contact '{name}' already exists. Use 'change' to update."
    
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: Tuple[str, ...], contacts: Dict[str, str]) -> str:
    """
    Змінює телефон існуючого контакту.
    
    Args:
        args: Кортеж з іменем та новим телефоном
        contacts: Словник контактів
        
    Returns:
        str: Повідомлення про результат операції
        
    Raises:
        ValueError: Якщо недостатньо аргументів
        KeyError: Якщо контакт не знайдено
    """
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    
    name, phone = args[0], args[1]
    
    # Перевіряємо, чи не порожні значення
    if not name.strip() or not phone.strip():
        raise ValueError("Give me name and phone please.")
    
    # Якщо контакт не існує, викидаємо KeyError
    if name not in contacts:
        raise KeyError(name)
    
    old_phone = contacts[name]
    contacts[name] = phone
    return f"Contact '{name}' updated from {old_phone} to {phone}."


@input_error
def show_phone(args: Tuple[str, ...], contacts: Dict[str, str]) -> str:
    """
    Показує телефон конкретного контакту.
    
    Args:
        args: Кортеж з іменем контакту
        contacts: Словник контактів
        
    Returns:
        str: Телефон контакту
        
    Raises:
        ValueError: Якщо не вказано ім'я
        KeyError: Якщо контакт не знайдено
    """
    if len(args) < 1:
        raise ValueError("Enter user name")
    
    name = args[0]
    
    if not name:
        raise ValueError("Enter user name")
    
    # Якщо контакт не існує, викидаємо KeyError
    if name not in contacts:
        raise KeyError(name)
    
    return f"{name}: {contacts[name]}"


@input_error
def show_all(contacts: Dict[str, str]) -> str:
    """
    Показує всі контакти в адресній книзі.
    
    Args:
        contacts: Словник контактів
        
    Returns:
        str: Відформатований список всіх контактів
    """
    if not contacts:
        return "No contacts found."
    
    # Сортуємо контакти за іменем (без урахування регістру)
    sorted_contacts = sorted(contacts.items(), key=lambda x: x[0].lower())
    lines = [f"{name}: {phone}" for name, phone in sorted_contacts]
    
    return "\n".join(lines)


@input_error
def delete_contact(args: Tuple[str, ...], contacts: Dict[str, str]) -> str:
    """
    Видаляє контакт з адресної книги.
    
    Args:
        args: Кортеж з іменем контакту
        contacts: Словник контактів
        
    Returns:
        str: Повідомлення про результат операції
        
    Raises:
        ValueError: Якщо не вказано ім'я
        KeyError: Якщо контакт не знайдено
    """
    if len(args) < 1:
        raise ValueError("Enter user name")
    
    name = args[0]
    
    if not name:
        raise ValueError("Enter user name")
    
    # Якщо контакт не існує, викидаємо KeyError
    if name not in contacts:
        raise KeyError(name)
    
    deleted_phone = contacts.pop(name)
    return f"Contact '{name}' ({deleted_phone}) deleted."


@input_error
def search_contacts(args: Tuple[str, ...], contacts: Dict[str, str]) -> str:
    """
    Шукає контакти за частиною імені або телефону.
    
    Args:
        args: Кортеж з пошуковим запитом
        contacts: Словник контактів
        
    Returns:
        str: Результати пошуку
        
    Raises:
        IndexError: Якщо не вказано пошуковий запит
    """
    if len(args) < 1:
        raise IndexError("search query required")
    
    query = args[0].lower()
    
    if not query.strip():
        raise IndexError("search query required")
    
    # Шукаємо в іменах та телефонах
    matches = []
    for name, phone in contacts.items():
        if query in name.lower() or query in phone:
            matches.append(f"{name}: {phone}")
    
    if not matches:
        return f"No contacts found matching '{query}'"
    
    return f"Found {len(matches)} contact(s):\n" + "\n".join(matches)


# -------------------- Допоміжні функції --------------------

def show_help() -> str:
    """
    Показує довідку по доступних командах.
    
    Returns:
        str: Текст довідки
    """
    help_text = """
Available commands:
  hello                     - Greeting
  add <name> <phone>        - Add new contact
  change <name> <phone>     - Change existing contact
  phone <name>              - Show phone for contact
  delete <name>             - Delete contact
  search <query>            - Search contacts by name or phone
  all                       - Show all contacts
  help                      - Show this help
  close, exit               - Exit the program

Examples:
  add John 0501234567
  change John 0509876543
  phone John
  delete John
  search 050
  all
"""
    return help_text.strip()


# -------------------- Головний цикл програми --------------------

def main() -> None:
    """
    Головна функція бота - запускає інтерактивний цикл.
    """
    contacts: Dict[str, str] = {}
    print("Welcome to the assistant bot!")
    print("Type 'help' to see available commands.")
    
    # Командна мапа для легкого розширення
    command_handlers = {
        "add": lambda args: add_contact(args, contacts),
        "change": lambda args: change_contact(args, contacts),
        "phone": lambda args: show_phone(args, contacts),
        "delete": lambda args: delete_contact(args, contacts),
        "search": lambda args: search_contacts(args, contacts),
        "all": lambda: show_all(contacts),
        "help": lambda: show_help()
    }
    
    while True:
        try:
            user_input = input("Enter a command: ").strip()
            
            if not user_input:
                continue
            
            command, *args = parse_input(user_input)
            
            # Команди виходу
            if command in ("close", "exit", "quit", "bye"):
                print("Good bye!")
                break
            
            # Привітання
            elif command == "hello":
                print("How can I help you?")
            
            # Обробляємо команди через мапу
            elif command in command_handlers:
                handler = command_handlers[command]
                # Перевіряємо, чи функція потребує аргументів
                if command in ("all", "help"):
                    result = handler()
                else:
                    result = handler(tuple(args))
                print(result)
            
            # Невідома команда
            else:
                print(f"Invalid command: '{command}'. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\nProgram interrupted by user. Good bye!")
            break
        except EOFError:
            print("\nEnd of input. Good bye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
