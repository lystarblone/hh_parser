import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
}

DATABASE_URL = "sqlite:///./hh_vacancies.db"
JSON_FILE = "vacancies.json"
DEFAULT_PAGES = 3
DEFAULT_AREA = 2
DEFAULT_QUERY = "python"