import json
from pathlib import Path
from typing import Union, Any, Optional

from config import file_with_vacancies, initialize_directories
from src.abs_base_file_work import BaseFileWork
from src.get_vacancies import Vacancy
from src.vacancy_to_dict import vacancy_to_dict


class JSONSaver(BaseFileWork):
    """Класс-наследник от абстрактного класса (BaseFileWork) для работы с JSON-файлами (работа с вакансиями)."""

    def __init__(self, path_to_file_with_vacancies: Path = file_with_vacancies) -> None:
        """Конструктор для инициализации пути к JSON-файлу, который хранит данные по вакансиям.
        :param path_to_file_with_vacancies: Путь к JSON-файлу, в котором будут храниться вакансии."""
        initialize_directories()  # Создаю директорию и файл доп функцией initialize_directories(), если этого еще нет.
        self.__file_with_vacancies = file_with_vacancies

    def add_vacancy(self, vacancy: Union["Vacancy", list["Vacancy"]]) -> None:
        """Метод для добавления вакансий в JSON-файл.
        :param vacancy: Экземпляр класса Vacancy (OBJECT) или список объектов Vacancy (LIST OF OBJECTS)."""
        # ШАГ 1: Открываю JSON-файл с существующими вакансиями.
        try:
            with open(self.__file_with_vacancies, "r", encoding="utf-8") as file:  # Сразу читаю все вакансии в файле.
                vacancies_data: list[dict[str, Any]] = json.load(file)
        except json.JSONDecodeError:  # Эта ошибка возникает, когда невозможно декодировать(преобразовать) JSON-данные.
            vacancies_data = []

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
        for vac in vacancies_data:
            existing_vacancies[vac["id"]] = vac

        # ШАГ 4: Проверяю дубли вакансий и статус архивации. А потом удаляю, обновляю или добавляю вакансию.
        for new_vacancy in new_vacancies:
            if new_vacancy["id"] in existing_vacancies:  # True - если вакансия уже есть в существующих вакансиях.
                old_vacancy: dict[str, Any] = existing_vacancies[new_vacancy["id"]]

                if new_vacancy["archived"]:  # Удаляю вакансию, если archived == True.
                    print(f"❌Удаляем архивную вакансию {new_vacancy["id"]}")
                    del existing_vacancies[new_vacancy["id"]]
                    continue

                if old_vacancy != new_vacancy:  # Проверяю, изменились ли данные (кроме ID) и обновляем их, если True.
                    print(f"🔄Обновляем вакансию {new_vacancy["id"]}")
                    existing_vacancies[new_vacancy["id"]] = new_vacancy

            else:
                print(f"✅Добавляем новую вакансию {new_vacancy["id"]}")
                existing_vacancies[new_vacancy["id"]] = new_vacancy  # Если новая вакансия, то просто добавляю её.

        # ШАГ 5: Перезаписываю JSON-файл с обновленными данными по вакансиям.
        # Преобразовываю обратно словарь словарей "existing_vacancies" в список "list(existing_vacancies.values()".
        with open(self.__file_with_vacancies, "w", encoding="utf-8") as file:
            json.dump(list(existing_vacancies.values()), file, indent=4, ensure_ascii=False)

    def get_vacancy(self, user_keywords: str = "") -> list[dict[str, Any]]:
        """Метод получения вакансий из JSON-файла.
        :param user_keywords: Ключевые слова через запятую для фильтрации вакансий.
        :return: Список найденных вакансий по заданным ключевым словам."""
        # ШАГ 1: Открываю JSON-файл с существующими вакансиями.
        try:
            with open(self.__file_with_vacancies, "r", encoding="utf-8") as file:
                vacancies_data: list[dict[str, Any]] = json.load(file)
        except json.JSONDecodeError:  # Эта ошибка возникает, когда невозможно декодировать(преобразовать) JSON-данные.
            vacancies_data = []

        # ШАГ 2: Если ключевые слова не заданы, то тогда возвращаю все вакансии.
        if not user_keywords:
            return vacancies_data

        # ШАГ 3: Разбиваю строку на список ключевых слов.
        input_user_key_words: list = [word.lower().strip() for word in user_keywords.split(",")]

        # ШАГ 4: Ищу вакансии по ключевым словам.
        found_vacancies = []
        for vacancy in vacancies_data:
            found = False  # Флаг по умолчанию в начале цикла перебора слов в описании, что ничего не найдено.
            for word in input_user_key_words:  # Перебираю ключевые слова и проверяю его наличие в описании вакансии.
                if word in vacancy["snippet_responsibility"].lower():
                    found = True  # Меняю флаг, если нашли совпадение в описании вакансии.
                    # Прерываю цикл перебора ключевых слов, так как уже по одному из них нашли совпадение и нет смысла
                    # искать другие ключевые слова и делать лишние проверки.
                    break
            if found:  # Если хотя бы одно ключевое слово найдено в описании.
                found_vacancies.append(vacancy)  # Добавляю эту вакансию в список найденных вакансий.
        return found_vacancies  # Возвращаю список найденных вакансий.

    def delete_vacancy(self, vacancy_to_delete: Optional["Vacancy"] = None) -> None:
        """Метод удаления вакансий из JSON-файла.
        :param vacancy_to_delete: Экземпляр класса Vacancy (OBJECT), который будем удалять из файла с вакансиями."""
        # ШАГ 1: Открываю JSON-файл с существующими вакансиями.
        try:
            with open(self.__file_with_vacancies, "r", encoding="utf-8") as file:
                vacancies_data: list[dict[str, Any]] = json.load(file)
        except json.JSONDecodeError:  # Эта ошибка возникает, когда невозможно декодировать(преобразовать) JSON-данные.
            vacancies_data = []

        # ШАГ 2: Если ничего не передали на удаление, просто выходим.
        if not vacancy_to_delete:
            return

        # ШАГ 3: Удаляю вакансию из JSON-файла с существующими вакансиями.
        vacancies_data_after_deletion = []
        for vacancy in vacancies_data:
            if vacancy["id"] != vacancy_to_delete.id:
                vacancies_data_after_deletion.append(vacancy)

        # ШАГ 4: Перезаписываю JSON-файл с обновленными данными по вакансиям.
        with open(self.__file_with_vacancies, "w", encoding="utf-8") as file:
            json.dump(vacancies_data_after_deletion, file, indent=4, ensure_ascii=False)

        print(f"❌Вакансия {vacancy_to_delete.id} удалена из JSON-файла.")
