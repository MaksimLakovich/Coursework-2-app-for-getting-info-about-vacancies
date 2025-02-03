from src.get_vacancies import Vacancy
from src.hh_api import HeadHunterAPI
from src.json_file_work import JSONSaver


def user_interaction():
    """Функция для взаимодействия с пользователем."""

    platforms = ["HeadHunter"]  # В будущем можно расширить и добавить другие платформы поиска вакансий.

    while True:
        select_platform = input(f"Выберите платформу для поиска вакансий ({', '.join(platforms)}): ").strip()
        if select_platform in platforms:
            print(f"✅ Выбрана платформа: {select_platform}")
            break
        else:
            print(f"❌ Ошибка: Платформа '{select_platform}' не поддерживается. Введите платформу из списка.")

    if select_platform == "HeadHunter":
        search_query = input("Введите поисковый запрос: ").strip()
        # ШАГ 1
        hh_api = HeadHunterAPI()  # Создание экземпляра класса для работы с API HeadHunter (сайта с вакансиями).
        hh_vacancies_data = hh_api.load_vacancies(search_query)  # Получение вакансий с hh.ru в формате JSON.
        vacancies_list = Vacancy.cast_to_object_list(hh_vacancies_data)  # Преобраз-е данных в список объектов Vacancy.

        # ШАГ 2: Сохранение собранных данных о вакансиях в файл.
        json_saver = JSONSaver()
        json_saver.add_vacancy(vacancies_list)



# Функции для взаимодействия с пользователем, которые необходимо реализовать:
#     top_n = int(input("Введите количество вакансий для вывода в топ N: "))
#     filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
#     salary_range = input("Введите диапазон зарплат: ") # Пример: 100000 - 150000
#
#     filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
#
#     ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
#
#     sorted_vacancies = sort_vacancies(ranged_vacancies)
#     top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
#     print_vacancies(top_vacancies)

if __name__ == "__main__":
    user_interaction()
