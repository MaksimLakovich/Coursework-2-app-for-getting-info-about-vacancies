from typing import Any


class Vacancy:
    """Класс для работы с вакансиями."""

    __slots__ = [
        "id",
        "name",
        "area_name",
        "alternate_url",
        "salary_from",
        "salary_to",
        "salary_currency",
        "published_at",
        "archived",
        "snippet_responsibility",
    ]

    def __init__(
        self,
        id: str,
        name: str,
        area_name: str,
        alternate_url: str,
        salary_from: float | None,
        salary_to: float | None,
        salary_currency: str | None,
        published_at: str,
        archived: bool,
        snippet_responsibility: str,
    ):
        """Конструктор для создания вакансии. Инициализация экземпляра класса (объекта)."""
        self.id = id
        self.name = name
        self.area_name = area_name
        self.alternate_url = alternate_url
        self.salary_from = self.__validate_salary(salary_from)
        self.salary_to = self.__validate_salary(salary_to)
        self.salary_currency = self.__validate_currency(salary_currency)
        self.published_at = published_at
        self.archived = archived
        self.snippet_responsibility = snippet_responsibility or ""

    def __validate_currency(self, currency: str | None) -> str:
        """Приватный метод валидации валюты зарплаты.
        :param currency: Значение валюты, которое поступает из запроса к API сервиса вакансий.
        :return: Возвращает строку 'RUB', если валюта отсутствует, так как:
                1) при отсутствии зарплаты на сервисе вакансий мы будем устанавливать 0;
                2) если зарплата установлена в другой валюте, то будем выполнять конвертацию в рубли."""
        return currency or "RUB"

    def __validate_salary(self, salary: float | None) -> float:
        """Приватный метод проверки значения зарплаты.
        :param salary: Значения 'from' и 'to' из 'salary', которые поступают из запроса к API сервиса вакансий.
        :return: Возвращает ноль, если зарплата не указана на сервисе вакансий."""
        return salary if salary and salary > 0 else 0.0

    def __eq__(self, other: object) -> bool:
        """Магический метод для операции сравнения 'равенство' (self = other)."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_to == other.salary_to

    def __lt__(self, other: "Vacancy") -> bool:
        """Магический метод для операции сравнения 'меньше' (self < other)."""
        return self.salary_to < other.salary_to

    def __le__(self, other: "Vacancy") -> bool:
        """Магический метод для операции сравнения 'меньше или равно' (self <= other)."""
        return self.salary_to <= other.salary_to

    def __gt__(self, other: "Vacancy") -> bool:
        """Магический метод для операции сравнения 'больше' (self > other)."""
        return self.salary_to > other.salary_to

    def __ge__(self, other: "Vacancy") -> bool:
        """Магический метод для операции сравнения 'больше или равно' (self >= other)."""
        return self.salary_to >= other.salary_to

    @staticmethod
    def cast_to_object_list(vacancies_data: list[dict[str, Any]]) -> list["Vacancy"]:
        """Преобразует список словарей в список объектов Vacancy.
        :param vacancies_data: Файл с полученными вакансиями, которые сформировались в запросе API сервиса вакансий.
        :return: Возвращает список объектов Vacancy."""
        return [
            Vacancy(
                id=data["id"],
                name=data["name"],
                area_name=data["area"]["name"],
                alternate_url=data["alternate_url"],
                # None, если salary отсутствует
                salary_from=(data.get("salary") or {}).get("from"),
                # None, если salary отсутствует
                salary_to=(data.get("salary") or {}).get("to"),
                # None, если salary отсутствует
                salary_currency=(data.get("salary") or {}).get("currency"),
                published_at=data["published_at"],
                archived=data["archived"],
                snippet_responsibility=data["snippet"].get("responsibility", ""),
            )
            for data in vacancies_data
        ]
