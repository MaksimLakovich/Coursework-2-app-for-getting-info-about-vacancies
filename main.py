from src.hh_api import HeadHunterAPI
from src.get_vacancies import Vacancy


# Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HeadHunterAPI()

# Получение вакансий с hh.ru в формате JSON
hh_vacancies_data = hh_api.load_vacancies("Python")

# Преобразование набора данных из hh_vacancies_data в список объектов Vacancy
vacancies_list = Vacancy.cast_to_object_list(hh_vacancies_data)

# Пример работы контструктора класса с одной вакансией
vacancy = Vacancy(
    "93353083",
    "Тестировщик комфорта квартир",
    "Воронеж",
    "https://hh.ru/vacancy/93353083",
    1000,
    1501,
    "USD",
    "2024-02-16T14:58:28+0300",
    False,
    "Оценивать вид из окна: встречать рассветы на кухне, провожать алые закаты",
)


if __name__ == "__main__":
    print(type(hh_vacancies_data))
    print(type(vacancies_list))
    print(vacancy.id, vacancy.name , vacancy.area_name , vacancy.alternate_url , vacancy.salary_from ,
          vacancy.salary_to , vacancy.salary_currency , vacancy.published_at , vacancy.archived ,
          vacancy.snippet_responsibility,)
