import json
from pathlib import Path
from typing import Union, Any

from config import initialize_directories
from src.abs_base_file_work import BaseFileWork
from src.get_vacancies import Vacancy
from src.vacancy_to_dict import vacancy_to_dict


class JSONSaver(BaseFileWork):
    """Класс-наследник от абстрактного класса (BaseFileWork) для работы с JSON-файлами (работа с вакансиями)."""

    def __init__(self, file_with_vacancies: Path) -> None:
        """Конструктор для инициализации пути к JSON-файлу, который хранит данные по вакансиям.
        :param file_with_vacancies: Путь к JSON-файлу, в котором будут храниться вакансии."""
        initialize_directories()  # Создаю директорию и файл доп функцией initialize_directories(), если этого еще нет.
        self.__file_with_vacancies = file_with_vacancies

    def add_vacancy(self, vacancy: Union["Vacancy", list["Vacancy"]]) -> None:
        """Метод для добавления вакансий в JSON-файл.
        :param vacancy: Экземпляр класса Vacancy (OBJECT) или список объектов Vacancy (LIST OF OBJECTS)."""
        # ШАГ 1: Открываю JSON-файл с существующими вакансиями.
        try:
            with open(self.__file_with_vacancies, "r", encoding="utf-8") as file:  # Сразу читаю все вакансии в файле.
                vacancies: list[dict[str, Any]] = json.load(file)
        except json.JSONDecodeError:  # Эта ошибка возникает, когда невозможно декодировать(преобразовать) JSON-данные.
            vacancies = []

        # ШАГ 2: Преобразовываю OBJECT/LIST_OF_OBJ в словари при помощи функции в "vacancy_to_dict.py".
        new_vacancies: list[dict[str, Any]] = []
        if isinstance(vacancy, list):
            new_vacancies.extend([vacancy_to_dict(v) for v in vacancy])  # extend - добавляем множество вакансий.
        else:
            new_vacancies.append(vacancy_to_dict(vacancy))  # append - добавляем 1 вакансию.

        # ШАГ 3: Создаю словарь словарей "existing_vacancies" с данными {id: {вакансии}} для последующего
        # выполнения быстрого поиска. Тут мы влияем на быстродействие программы. Теперь можно будет быстро проверять,
        # есть ли вакансия с таким id, а потом обновлять её или удалять при необходимости в ШАГЕ 4.
        existing_vacancies: dict[str, dict[str, Any]] = {}
        for vac in vacancies:
            existing_vacancies[vac["id"]] = vac

        # ШАГ 4: Проверяю дубли вакансий и статус архивации. А потом удаляю, обновляю или добавляю вакансию.
        for new_vacancy in new_vacancies:
            if new_vacancy["id"] in existing_vacancies:  # True - если вакансия уже есть в существующих вакансиях.
                old_vacancy: dict[str, Any] = existing_vacancies[new_vacancy["id"]]

                if new_vacancy["archived"]:  # Удаляю вакансию, если archived == True.
                    print(f"Удаляем архивную вакансию {new_vacancy["id"]}")
                    del existing_vacancies[new_vacancy["id"]]
                    continue

                if old_vacancy != new_vacancy:  # Проверяю, изменились ли данные (кроме ID) и обновляем их, если True.
                    print(f"Обновляем вакансию {new_vacancy["id"]}")
                    # existing_vacancies[new_vacancy["id"]] = new_vacancy
                    existing_vacancies[new_vacancy["id"]] = new_vacancy

            else:
                print(f"Добавляем новую вакансию {new_vacancy["id"]}")
                existing_vacancies[new_vacancy["id"]] = new_vacancy  # Если новая вакансия, то просто добавляю её.

        # ШАГ 5: Перезаписываю JSON-файл с обновленными данными по вакансиям.
        # Преобразовываю обратно словарь словарей "existing_vacancies" в список "list(existing_vacancies.values()".
        with open(self.__file_with_vacancies, "w", encoding="utf-8") as file:
            json.dump(list(existing_vacancies.values()), file, indent=4, ensure_ascii=False)

    def get_vacancy(self, vacancy: "Vacancy") -> None:
        """Метод получения вакансий из JSON-файла."""
        pass

    # def get_vacancy(self) -> list[Vacancy]:
    #     """Метод получения всех вакансий из JSON-файла, с пересозданием объектов `Vacancy`."""
    #     try:
    #         with open(self.__file_with_vacancies, "r", encoding="utf-8") as file:
    #             vacancies_data = json.load(file)
    #         return [Vacancy(**data) for data in vacancies_data]  # ⬅ Пересоздаём объекты Vacancy
    #     except json.JSONDecodeError:
    #         return []

    def delete_vacancy(self, vacancy: "Vacancy") -> None:
        """Метод удаления вакансий из JSON-файла."""
        pass
