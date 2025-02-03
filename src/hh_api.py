from typing import Any

import requests

from src.abs_base_api import BaseAPI


class HeadHunterAPI(BaseAPI):
    """Класс-наследник от абстрактного класса (BaseAPI) для работы с платформой hh.ru."""

    def __init__(self) -> None:
        """Конструктор для инициализации подключения к API сервису."""
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params: dict[str, str | int] = {"text": "", "page": 0, "per_page": 100}
        # Итоговый список в который складываются вакансии list[dict[str, Any]]
        self.__vacancies: list[dict[str, Any]] = []

    def load_vacancies(self, keyword: str) -> list[dict[str, Any]]:
        """Метод для получения вакансии с API сервиса HeadHunter.ru по ключевому слову.
        :param keyword: Ключевое слово для получения данных о вакансиях.
        :return: Файл с полученными вакансиями."""
        # Устанавливаю в self.params['text'] конструктора класса значение =keyword (ключевое слово или фраза), которое
        # будет искаться в специальных полях вакансии
        self.__params["text"] = keyword
        # При указании параметров пагинации (page, per_page) работает ограничение: глубина возвращаемых результатов
        # не может быть больше 2000, поэтому прохожу циклом по 20 страницам (от 0 до 19)
        while self.__params.get("page") != 20:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            if response.status_code == 200:
                try:
                    # Сохраняю в переменную vacancies список вакансий из items
                    vacancies = response.json()["items"]
                    # С каждой страницы (page) добавляю список вакансий в общий список
                    self.__vacancies.extend(vacancies)
                    self.__params["page"] += 1
                except requests.exceptions.RequestException as info:
                    print(f"❌Ошибка при обращении к API hh.ru: {info}")
                    return []
                except KeyError:
                    print("❌Некорректный формат ответа API hh.ru.")
                    return []
            else:
                print(f"❌Ошибка: {response.status_code}, текст: {response.text}")
                return []
        return self.__vacancies
