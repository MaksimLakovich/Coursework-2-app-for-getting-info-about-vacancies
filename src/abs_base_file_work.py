from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, Any

from src.get_vacancies import Vacancy


class BaseFileWork(ABC):
    """Абстрактный класс BaseFileWork для работы с файлом, который будет содержать экземпляры класса Vacancy."""

    @abstractmethod
    def __init__(self, file_with_vacancies: Path) -> None:
        """Конструктор для инициализации пути к файлу, который хранит данные по вакансиям.
        :param file_with_vacancies: Путь к файлу (JSON, CSV и т.д.), в котором будут храниться вакансии."""
        pass

    @abstractmethod
    def add_vacancy(self, vacancy: Union["Vacancy", list["Vacancy"]]) -> None:
        """Метод для добавления вакансий в файл.
        :param vacancy: Экземпляр класса Vacancy (OBJECT) или список объектов Vacancy (LIST OF OBJECTS)."""
        pass

    @abstractmethod
    def get_vacancy(self, user_keywords: str = "") -> list[dict[str, Any]]:
        """Метод получения вакансий из файла.
        :param user_keywords: Ключевые слова через запятую для фильтрации вакансий.
        :return: Список найденных вакансий по заданным ключевым словам."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_to_delete: "Vacancy") -> None:
        """Метод удаления вакансий из файла.
        :param vacancy_to_delete: Экземпляр класса Vacancy (OBJECT), который будем удалять из файла с вакансиями."""
        pass
