from abc import ABC, abstractmethod


class BaseAPI(ABC):
    """Абстрактный класс BaseAPI для работы с API сервиса с вакансиями."""

    @abstractmethod
    def __init__(self) -> None:
        """Конструктор для инициализации подключения к API сервису."""
        pass

    @abstractmethod
    def load_vacancies(self, keyword: str) -> list:
        """Метод для получения вакансии с API сервиса по ключевому слову.
        :param keyword: Ключевое слово для получения данных о вакансиях.
        :return: Файл-json"""
        pass
