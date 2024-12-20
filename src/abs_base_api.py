from abc import ABC, abstractmethod
from typing import Any


class BaseAPI(ABC):
    """Абстрактный класс BaseAPI для работы с API сервиса с вакансиями."""

    @abstractmethod
    def __init__(self) -> None:
        """Конструктор для инициализации подключения к API сервису."""
        pass

    @abstractmethod
    def load_vacancies(self, keyword: str) -> list[dict[str, Any]]:
        """Метод для получения вакансии с API сервиса по ключевому слову.
        :param keyword: Ключевое слово для получения данных о вакансиях.
        :return: Файл с полученными вакансиями."""
        pass
