import os
from typing import Any

import requests
from dotenv import load_dotenv

# Кеш для сохранения курсов валют
EXCHANGE_RATES_CACHE: dict[str, float] = {}


def get_exchange_rates(currency_name: str) -> float:
    """Функция для получения текущего курса валюты по отношению к RUB.
    :param currency_name: Название валюты, для которой будет выполняться запрос курса по отношению к RUB.
    :return: Курс по интересующей валюте (пример для "USD": функция вернет 101.21)."""

    # Загружаю ключ-api из ".env" через dotenv
    load_dotenv()
    api_key = os.getenv("API_KEY_EXCHANGE_RATES")

    # Возбуждаю ошибку, если в окружении env нет ключа или он некорректный
    if not api_key:
        raise ValueError("API_KEY_EXCHANGE_RATES не найден в переменных окружения.env")

    if currency_name in EXCHANGE_RATES_CACHE:
        return EXCHANGE_RATES_CACHE[currency_name]
    else:
        try:
            url = "https://api.apilayer.com/exchangerates_data/convert"
            payload: dict[str, str | int] = {
                "amount": 1,
                "from": currency_name,
                "to": "RUB",
            }
            headers = {"apikey": api_key}
            response = requests.request("GET", url, headers=headers, params=payload)
            if response.status_code != 200:
                raise ValueError(f"Не удалось получить курс валюты {currency_name}: {response.text}")
            currency_rate: Any = response.json().get("result")
            if not isinstance(currency_rate, (int, float)):
                raise ValueError(f"Ответ API не содержит курс для валюты {currency_name}")
            EXCHANGE_RATES_CACHE[currency_name] = currency_rate
            return currency_rate
        except requests.RequestException as info_e:
            print(f"Ошибка при запросе API для валюты {currency_name}: {info_e}")
            return 0.0
