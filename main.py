from src.get_vacancies import Vacancy
from src.hh_api import HeadHunterAPI
from src.json_file_work import JSONSaver
from src.vacancy_to_dict import vacancy_to_dict


def user_interaction() -> None:
    """Функция для взаимодействия пользователя с программой."""

    platforms = ["HeadHunter"]  # В будущем можно расширить и добавить другие платформы поиска вакансий.

    while True:
        select_platform = input(f"Выберите платформу для поиска вакансий ({', '.join(platforms)}): ").strip()
        if select_platform in platforms:
            print(f"✅ Выбрана платформа: {select_platform}")
            break
        else:
            print(f"❌ Ошибка: Платформа '{select_platform}' не поддерживается. Введите платформу из списка.")

    # ШАГ 1: Подключаемся к HeadHunter и получаем все вакансии по указанному поисковому запросу.
    if select_platform == "HeadHunter":
        search_query = input("Введите поисковый запрос: ").strip()
        hh_api = HeadHunterAPI()  # Создание экземпляра класса для работы с API HeadHunter (сайта с вакансиями).
        hh_vacancies_data = hh_api.load_vacancies(search_query)  # Получение вакансий с hh.ru.
        vacancies_list = Vacancy.cast_to_object_list(hh_vacancies_data)  # Изменение данных в список объектов Vacancy.

        # ШАГ 2: Сохранение собранных данных о вакансиях в JSON-файл.
        json_saver = JSONSaver()
        json_saver.add_vacancy(vacancies_list)

        # ШАГ 3: Создаю копию списка вакансий, которая будет меняться при дальнейшей пользовательской фильтрации,
        # чтоб у пользователя была возможность отменить фильтрацию и вернуться к первоначальному полному списку.
        current_vacancies = vacancies_list.copy()

        # ШАГ 4: Даю пользователю выбрать, что делать дальше.
        while True:
            print("\nДополнительные действия:")
            print("1 - Получить вакансии в заданном городе")
            print("2 - Получить топ N вакансий по зарплате")
            print("3 - Найти вакансии по ключевым словам")
            print("4 - Фильтр по зарплате")
            print("5 - Сбросить фильтры (вернуть полный список вакансий)")
            print("6 - Выход")
            choice = input("Выберите действие (1-6): ").strip()

            if choice == "1":
                filter_city = input("Введите город (или набор городов через запятую): ").strip().title()
                found_vacancies = json_saver.get_vacancy(filter_city)
                if found_vacancies:
                    # Обновляю current_vacancies, оставляя только те вакансии, у которых ID совпадает.
                    current_vacancies = [
                        vac for vac in current_vacancies if vac.id in {v["id"] for v in found_vacancies}
                    ]
                    count = len(current_vacancies)
                    print(f"\nНайденные вакансии в {filter_city} ({count}):")
                    for vacancy in current_vacancies:
                        # Использую функцию vacancy_to_dict() для преобразования объектов Vacancy в словари для печати.
                        vacancy_dict = vacancy_to_dict(vacancy)
                        print(vacancy_dict)
                else:
                    print("⚠️По вашему запросу ничего не найдено.")

            elif choice == "2":
                try:
                    top_n = int(input("Введите количество вакансий для вывода в топ N по зарплате: "))
                    sorted_vacancies = sorted(current_vacancies, reverse=True)  # Работают магические методы Vacancy.
                    current_vacancies = sorted_vacancies[:top_n]  # Обновляем список после сортировки.
                    print(f"\nТоп-{top_n} вакансий:")
                    for vacancy in current_vacancies:
                        # Использую функцию vacancy_to_dict() для преобразования объектов Vacancy в словари для печати.
                        vacancy_dict = vacancy_to_dict(vacancy)
                        print(vacancy_dict)
                except ValueError:
                    print("❌Ошибка: Введите корректное число.")

            elif choice == "3":
                filter_words = input("Введите ключевые слова для поиска (через запятую): ")
                found_vacancies = json_saver.get_vacancy(filter_words)
                if found_vacancies:
                    # Обновляю current_vacancies, оставляя только те вакансии, у которых ID совпадает.
                    current_vacancies = [
                        vac for vac in current_vacancies if vac.id in {v["id"] for v in found_vacancies}
                    ]
                    count = len(current_vacancies)
                    print(f"\nНайденные вакансии ({count}):")
                    for vacancy in current_vacancies:
                        # Использую функцию vacancy_to_dict() для преобразования объектов Vacancy в словари для печати.
                        print(vacancy_to_dict(vacancy))
                else:
                    print("⚠️По вашему запросу ничего не найдено.")

            elif choice == "4":
                try:
                    salary_min = input("Введите минимальную зарплату (или нажмите Enter, чтобы пропустить): ").strip()
                    salary_max = input("Введите максимальную зарплату (или нажмите Enter, чтобы пропустить): ").strip()

                    salary_min = float(salary_min) if salary_min else 0  # Если не указали, то 0 по умолчанию.
                    salary_max = float(salary_max) if salary_max else float('inf')  # Если не указали, то до ...
                    # Обновляю current_vacancies, оставляя те вакансии, которые в диапазоне salary_min и salary_max.
                    current_vacancies = [
                        vac for vac in current_vacancies if salary_min <= vac.salary_to <= salary_max
                    ]
                    print(f"\nВакансии с зарплатой от {salary_min} до {salary_max}:")
                    for vacancy in current_vacancies:
                        # Использую функцию vacancy_to_dict() для преобразования объектов Vacancy в словари для печати.
                        print(vacancy_to_dict(vacancy))
                except ValueError:
                    print("❌Ошибка: Введите корректные числа.")

            elif choice == "5":
                current_vacancies = vacancies_list.copy()
                print("✅Фильтры сброшены. Отображается полный список вакансий.")

            elif choice == "6":
                print("✅Завершение работы.")
                break

            else:
                print("❌Ошибка: Некорректный ввод. Попробуйте снова.")


if __name__ == "__main__":
    user_interaction()
