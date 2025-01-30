from src.get_vacancies import Vacancy


def vacancy_to_dict(vacancy: Vacancy) -> dict:
    """Функция для преобразования объекта Vacancy в словарь."""
    return {slot: getattr(vacancy, slot) for slot in Vacancy.__slots__}
