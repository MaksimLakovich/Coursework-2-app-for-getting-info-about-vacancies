from typing import Any

from src.exchange_rates import get_exchange_rates


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
        self.salary_from = self.__validate_salary(salary=salary_from, currency=salary_currency)
        self.salary_to = self.__validate_salary(salary=salary_to, currency=salary_currency)
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

    def __validate_salary(self, salary: float | None, currency: str | None) -> float:
        """Приватный метод проверки значения зарплаты (валидация пустых значений),
        если валюта != RUB, то выполнение конвертации валюты в RUB.
        :param salary: Значения 'from' и 'to' из 'salary', которые поступают из запроса к API сервиса вакансий.
        :param currency: Значение валюты, которое поступает из запроса к API сервиса вакансий.
        :return: Возвращает дробное число:
                1) ноль, если зарплата не указана на сервисе вакансий;
                2) конвертируемое значение по текущему курсу валют, если зарплата в отличной от RUB валюте.
                3) текущее значение без изменения, если зарплата на сервисе вакансий указана в RUB."""
        if not salary or salary <= 0:
            return 0.0
        if currency and currency != "RUR":
            return salary * get_exchange_rates(currency_name=currency)
        # Возвращаем исходное значение зарплаты, так как оно в RUB и не требует конвертации
        return salary

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
