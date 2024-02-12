from utils import *


if __name__ == "__main__":
    # загрузка данных из файла
    load_data(phone_book, filename)

    # главное меню
    while True:
        clear_screen()
        action: str = input(
            'Выберите действие: (1) смотреть данные, (2) добавить запись, (3) редактировать запись, (4) найти запись, '
            '(0) выйти: ')
        if action not in ['0', '1', '2', '3', '4']:
            print('Incorrect input. Try again.')
            print()

        # выход из приложения
        if action == '0':
            clear_screen()
            print("Сеанс завершён.")
            break

        # просмотр данных
        if action == '1':
            display_data(5)

        # добавление новой записи
        if action == '2':

            # формируем новую запись и добавляем в словарь
            new_entry: Dict[int, Dict[str, str]] = {int(max(phone_book.keys()) + 1): {}}
            for field in data_fields:
                value: str = input(f'Введите {field}: ')
                if field in ["Телефон (раб.)", "Телефон (сот.)"]:
                    while not value.isdigit():
                        print('Неверный ввод. Только числовые значения в 10-значном формате (например, 79253749850).')
                        value = input(f'Введите {field}: ')
                new_entry[list(new_entry.keys())[0]][field] = value
            phone_book.update(new_entry)

            # сохраняем данные в файл
            clear_screen()
            result: bool = save_data()

            # при успешном сохранении выводим данные пользователю
            if result:
                print(f'Добавлена запись:\n')
                display_specific_data(new_entry)

            # в случае сбоя удаляем запись из словаря
            else:
                phone_book.popitem()

            print('\n')
            input('Нажмите любую клавишу, чтобы продолжить. ')

        # редактирование данных
        if action == '3':

            while True:
                # запрос записи для редактирования
                entry_id: str = input('Введите номер записи ("q" чтобы выйти): ')
                if (not entry_id.isdigit() and entry_id != 'q') or (entry_id.isdigit() and int(entry_id)
                                                                    not in phone_book.keys()):
                    print('Запись не найдена. Попробуйте заново.')
                    print()

                # выход из данного меню
                elif entry_id == 'q':
                    break

                else:
                    # вывод запрошенной записи на экран пользователю
                    while True:
                        clear_screen()
                        display_specific_data(phone_book, iteration=False, key=entry_id)
                        print()

                        # запрос поля для редактирования
                        update: str = input(f'Какое поле вы хотите обновить?\n'
                                            f'{", ".join(str(field) for field in data_fields)}\n'
                                            f'(введите "a", чтобы обновить все поля, "q" - чтобы выйти): ')

                        if update not in phone_book[int(entry_id)] and update not in ['q', 'a']:
                            print('Запись не найдена. Попробуйте заново.', '', sep='\n')
                            input('Нажимте любую клавишу, чтобы продолжить.')

                        # возврат в предыдущее меню
                        elif update == 'q':
                            break

                        # обновление всех полей записи
                        elif update == 'a':
                            for key in phone_book[int(entry_id)]:
                                new_value: str = input(f'Введите новое значение для поля "{key}" '
                                                       f'(пустой ввод, чтобы оставить без изменений): ')
                                if key in ["Телефон (раб.)", "Телефон (сот.)"]:
                                    while not new_value.isdigit() and not new_value == "":
                                        print('Неверный ввод. Только числовые значения в 10-значном формате '
                                              '(например, 79253749850).')
                                        new_value = input(f'Введите новое значение для поля "{key}" '
                                                          f'(пустой ввод, чтобы оставить без изменений): ')

                                    if new_value == "":
                                        pass
                                    else:
                                        phone_book[int(entry_id)][key] = new_value
                                elif new_value == "":
                                    pass
                                else:
                                    phone_book[int(entry_id)][key] = new_value

                            # сохраняем данные в файл
                            clear_screen()
                            result: bool = save_data()

                            # при успешном сохранении выводим данные пользователю
                            if result:
                                print(f'Запись #{int(entry_id)} обновлена успешно:\n')
                                display_specific_data(phone_book, iteration=False, key=entry_id)

                            # в случае сбоя перезагружаем данные из рабочего файла
                            else:
                                load_data(phone_book, filename)

                            print('\n')
                            input('Нажмите любую клавишу, чтобы продолжить. ')
                            break

                        # обновление выбранного поля
                        else:
                            # запрашиваем новое значение у пользователя и сохраняем в словарь
                            new_value: str = input('Введите новое значение: ')
                            if update in ["Телефон (раб.)", "Телефон (сот.)"]:
                                while not new_value.isdigit():
                                    print('Неверный ввод. Только числовые значения в 10-значном формате '
                                          '(например, 79253749850).')
                                    new_value = input(f'Введите {update}: ')
                            phone_book[int(entry_id)][update] = new_value

                            # сохраняем данные в файл
                            clear_screen()
                            result: bool = save_data()

                            # при успешном сохранении выводим данные пользователю
                            if result:
                                print(f'Поле "{update}" успешно обновлено:\n')
                                display_specific_data(phone_book, iteration=False, key=entry_id)

                            # в случае сбоя перезагружаем данные из рабочего файла
                            else:
                                load_data(phone_book, filename)

                            print('\n')
                            input('Нажмите любую клавишу, чтобы продолжить. ')
                            break
                    break

        # поиск данных
        if action == '4':

            while True:
                # запрашиваем тип поиска
                search_type = input("Выберите тип поиска: (1) по ключевым словам, (2) по конкретному параметру: ")

                # поиск по ключевым словам
                if search_type == '1':

                    # запрашиваем ключевые слова у пользователя
                    search_input: str = input("Введите ключевые слова через запятую: ")
                    search_keywords: List[str] = [keyword.strip() for keyword in search_input.split(",")]

                    # фильтрация записей по ключевым словам
                    search_results: Dict[int, Dict[str, str]] = {}
                    for entry_id, entry_data in phone_book.items():
                        for keyword in search_keywords:
                            for field, value in entry_data.items():
                                if keyword.lower() in str(value).lower():
                                    search_results[int(entry_id)] = entry_data
                                    break
                            else:
                                continue
                            break

                    # отображение результатов поиска
                    clear_screen()
                    print(f'Результаты поиска по ключевым словам: {", ".join(word for word in search_keywords)}', sep="\n")
                    display_specific_data(search_results, iteration=True, two_iterables=True)
                    input('Нажмите любую клавишу, чтобы продолжить. ')
                    break

                # поиск по конкретному параметру
                elif search_type == '2':
                    while True:
                        # запрашиваем поле и поисковой запрос у пользователя
                        search_field = input(
                            f'Введите поле для поиска: {", ".join(str(field) for field in data_fields)}: ')
                        if search_field.lower() not in [field.lower() for field in data_fields]:
                            print("Некорректное поле для поиска. Попробуйте снова.")
                        else:
                            break

                    search_value = input(f'Введите значение для поля "{search_field}": ')

                    # фильтрация записей по конкретному параметру
                    search_results: Dict[int, Dict[str, str]] = {}
                    for entry_id, entry_data in phone_book.items():
                        if search_value.lower() == entry_data.get(search_field, "").lower():
                            search_results[int(entry_id)] = entry_data

                    # отображение результатов поиска
                    clear_screen()
                    print(f'Результаты поиска по параметру: {search_field} = {search_value}')
                    display_specific_data(search_results, iteration=True, two_iterables=True)
                    input('Нажмите любую клавишу, чтобы продолжить. ')
                    break

                else:
                    print("Некорректный выбор. Попробуйте снова.")