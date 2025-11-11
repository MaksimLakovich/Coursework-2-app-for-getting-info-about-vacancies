from pathlib import Path

# Определение пути к корневой директории проекта, это будет использоваться далее в определении необходимых путей
BASE_DIR = Path(__file__).resolve().parent


# Определение пути к директории где будет размещаться JSON-файл с вакансиями (../data/)
DATA_DIR = BASE_DIR / "data"


# 1) Чтобы автоматически создать необходимую директорию (../data/), если ее еще не существует, я использую эту функцию.
# Будем вызывать ее при работе с классом-наследником JSONSaver в "src/json_file_work.py", что логично на мой взгляд,
# так как конструктор класса (__iint__) инициализирует путь к JSON-файлу с вакансиями для дальнейшего взаимодействия.
# 2) Также проверяю существование "json_data_with_vacancies.json" и если его не существует, то создаю пустой.
def initialize_directories() -> None:
    """Функция создает необходимые директории и файлы, если они еще не существуют."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not file_with_vacancies.exists():
        file_with_vacancies.write_text("[]", encoding="utf-8")


# Определение пути к JSON-файлу с вакансиями, который размещается в проекте в директории (../data/)
file_with_vacancies = DATA_DIR / "json_data_with_vacancies.json"
