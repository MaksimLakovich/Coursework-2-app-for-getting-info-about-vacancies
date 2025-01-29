from abc import ABC, abstractmethod

from src.get_vacancies import Vacancy


class BaseFileWork(ABC):
    """Абстрактный класс BaseFileWork для работы с файлом, который будет содержать экземпляры класса Vacancy."""

    @abstractmethod
    def __init__(self, file_with_vacancies: str) -> None:
        """Конструктор для инициализации пути к JSON-файлу, который хранит данные по вакансиям.
        :param file_with_vacancies: ?????????????????????????????"""
        pass

    @abstractmethod
    def add_vacancy(self, vacancy: "Vacancy") -> None:
        """Метод для добавления вакансий в JSON-файл.
        :param vacancy: Экземпляр класса Vacancy.
        ?????????????????????????????"""
        pass

    @abstractmethod
    def get_vacancy(self, vacancy: "Vacancy") -> None:
        """Метод получения вакансий из JSON-файла.
        ВАЖНО:
            Метод get_vacancy будет принимать параметры для фильтрации (например, по id или salary или описанию).
        ?????????????????????????????"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: "Vacancy") -> None:
        """Метод удаления вакансий из JSON-файла.
        Работает с id.
        ?????????????????????????????"""
        pass
