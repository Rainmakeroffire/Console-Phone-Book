import os
import shutil
from typing import Dict, Optional, Tuple, List
from colorama import Fore, Style


# ПЕРЕМЕННЫЕ

# словарь для хранения данных
phone_book: Dict[int, Dict[str, str]] = {}

# переменная для хранения имени рабочего файла
filename: str = 'db.txt'

# поля таблицы
data_fields: List[str] = ["Имя", "Фамилия", "Отчество", "Организация", "Телефон (раб.)", "Телефон (сот.)"]

# сообщение об ошибке
error_message: str = ''


# ФУНКЦИИ

def load_data(dictionary, filename) -> None:
    """Открывает файл с данными в режиме чтения, итерирует его построчно и сохраняет данные в словарь, где ключами
    являются целые числа (номера строк), а значениями - вложенные словари с парами поле: значение."""

    try:
        # чтение файла, итерация и сохранение значений в словарь
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line_id, line_data = line.split("#", 1)
                entry_data = {}
                for data_pair in line_data.strip().split(","):
                    key, value = data_pair.split(": ")
                    entry_data[key.strip()] = value.strip()
                dictionary[int(line_id)] = entry_data

    # вылавливаем исключение на случай, если рабочий файл был переименован, удалён или перемещён
    except FileNotFoundError:
        print(f'Не удалось загрузить файл "{filename}"')

    # игнорируем пустые строки
    except ValueError:
        pass


def save_data():
    """Сохраняет данные из словаря в файл в случае добавления или редактирования записей пользователем."""
    try:
        # создаётся резервная копия рабочего файла и устанавливается флаг успеха/сбоя сохранения данных
        has_succeeded = False
        backup_filename = filename + '.bak'
        shutil.copyfile(filename, backup_filename)

        #открывается файл, итерируется словарь, данные построчно переносятся в файл
        with open(filename, 'w', encoding='utf-8') as file:
            for k, v in phone_book.items():
                file.writelines(f'{str(k)}# ')
                for k1, v1 in v.items():
                    file.writelines(f'{k1}: ')
                    if v1 == list(v.values())[-1]:
                        file.writelines(f'{v1}')
                    else:
                        file.writelines(f'{v1}, ')
                file.writelines('\n')

            # флаг меняется на успешный
            has_succeeded = True
            return has_succeeded

    # сообщение пользователю в случае сбоя сохранения данных
    except Exception:
        print(f'Не удалось сохранить изменения.')

    # если произошёл сбой, данные восстанавливаются из резервной копии
    # если сохранение прошло успшено - резервная копия удаляется
    finally:
        if os.path.exists(backup_filename):
            if has_succeeded is False:
                shutil.move(backup_filename, filename)
            else:
                os.remove(backup_filename)


def go_to_page(page_number: int, page_size: int, total_pages: int) -> Tuple[Optional[int], Optional[int]]:
    """Обеспечивает пагинацию данных"""
    if page_number < 1 or page_number > total_pages:
        global error_message
        error_message = f'Неверный номер страницы. Введите значение от 1 до {total_pages}.'
        return None, None

    start_index: int = (page_number - 1) * page_size
    end_index: int = min(start_index + page_size, len(phone_book))
    return start_index, end_index


# функция отображения всех данных в виде таблицы
def display_data(page_size: int) -> None:
    """Отображает общий массив данных в виде таблицы с разбивкой на страницы."""

    # параметры пагинации
    total_entries: int = len(phone_book)
    total_pages: int = (total_entries + page_size - 1) // page_size

    current_page: int = 1

    while True:
        # очистка экрана и отображение таблицы с данными, а также нумерации страниц
        clear_screen()

        print(Fore.YELLOW + Style.BRIGHT + "\n{:<5} {:<15} {:<15} {:<15} {:<25} {:<15} {:<10}".format(
            "ID", *data_fields))
        print(Style.RESET_ALL)

        start_index, end_index = go_to_page(current_page, page_size, total_pages)
        if start_index is None:
            return

        for key in sorted(list(phone_book.keys())[start_index:end_index]):
            data: Dict[str, str] = phone_book[key]
            print("{:<5} {:<15} {:<15} {:<15} {:<25} {:<15} {:<10}".format(
                key, *(data.get(field, '') for field in data_fields)))

        print(Fore.GREEN + Style.BRIGHT + f"\nPage {current_page}/{total_pages}\n")
        print(Style.RESET_ALL)

        # настройка внешнего вида сообщений об ошибке
        global error_message

        if error_message:
            print(Fore.RED + Style.BRIGHT + error_message)
            print(Style.RESET_ALL)
            error_message = ''

        # панель пользовательской навигации по страницам таблицы
        action: str = input(f'Для перехода на следующую страницу нажимите Enter, "b" - на предыдущую страницу, '
                            f'или введите номер страницы в диапазоне от (1 до {total_pages}), "q" чтобы выйти: ')

        if action == "":
            if current_page < total_pages:
                current_page += 1

        elif action == "b":
            if current_page > 1:
                current_page -= 1

        elif action.isdigit():
            page_number: int = int(action)
            start_index, end_index = go_to_page(page_number, page_size, total_pages)
            if start_index is not None:
                current_page = page_number
        elif action == "q":
            break
        else:
            error_message = "Некорректный ввод. Попробуйте заново."


# функция отображения отдельной выборки данных в виде таблицы
def display_specific_data(dictionary: Dict[int, Dict[str, str]], iteration: bool = True, key: Optional[str] = None,
                          two_iterables: bool = False) -> None:
    """Отображает отдельные выборки данных (результаты поиска, внесённые изменения и т.п.) в виде таблицы

    Всегда принимает словарь в качестве позиционного арумента, также содержит ключевые аргументы, которые могут
    передаваться в зависимости от контекста использования функции.
    """


    print(Fore.YELLOW + Style.BRIGHT + "\n{:<5} {:<15} {:<15} {:<15} {:<25} {:<15} {:<10}".format(
        "ID", *data_fields))
    print(Style.RESET_ALL)

    if iteration:
        if two_iterables:
            # отображение результатов поиска
            for entry_id, entry_data in dictionary.items():
                print("{:<5} {:<15} {:<15} {:<15} {:<25} {:<15} {:<10}".format(
                    entry_id, *(entry_data.get(field, '') for field in data_fields)))
            print(Fore.GREEN + Style.BRIGHT + f"\nНайдено записей: {len(dictionary)}\n")
            print(Style.RESET_ALL)
        else:
            # отображение данных о новой записи
            for key in dictionary:
                data: Dict[str, str] = dictionary[key]
                print("{:<5} {:<15} {:<15} {:<15} {:<25} {:<15} {:<10}".format(
                    key, *(data.get(field, '') for field in data_fields)))

    else:
        # отображение данных для редактирования или отредактированных данных
        data: Dict[str, str] = dictionary[int(key)]
        print("{:<5} {:<15} {:<15} {:<15} {:<25} {:<15} {:<10}".format(
            key, *(data.get(field, '') for field in data_fields)))


def clear_screen():
    """Очищает экран"""
    os.system('cls' if os.name == 'nt' else 'clear')
