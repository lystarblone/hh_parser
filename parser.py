import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from config import HEADERS
from models import VacancyCreate
import logging

logger = logging.getLogger(__name__)

def parse_vacancies(query, area=1, pages=2):
    all_vacancies = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for page in range(pages):
        url = "https://hh.ru/search/vacancy"
        params = {
            "text": query,
            "area": area,
            "page": page,
            "per_page": 20
        }

        try:
            response = requests.get(url, headers=HEADERS, params=params)
            response.raise_for_status()

            # Проверка на капчу или блокировку
            if "Доступ ограничен" in response.text or "captcha" in response.text.lower():
                logger.error("Access denied or CAPTCHA detected. Try changing headers or using proxy.")
                break

        except requests.RequestException as e:
            logger.error(f"Request failed on page {page + 1}: {e}")
            break

        soup = BeautifulSoup(response.text, 'lxml')

        # 🔥 ИСПРАВЛЕНО: Используем data-qa для поиска контейнера вакансии
        vacancy_blocks = soup.find_all(attrs={"data-qa": "vacancy-serp__vacancy"})

        if not vacancy_blocks:
            logger.warning(f"No vacancies found on page {page + 1}. Ending parsing.")
            break

        for block in vacancy_blocks:
            # Заголовок и ссылка
            title_tag = block.find('a', {'data-qa': 'serp-item__title'})
            title = title_tag.get_text(strip=True) if title_tag else "Без названия"
            link = title_tag['href'] if title_tag else ""

            # Компания
            company_tag = block.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})
            company = company_tag.get_text(strip=True) if company_tag else "Не указана"

            # Зарплата — может отсутствовать
            salary_tag = block.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            salary = salary_tag.get_text(strip=True) if salary_tag else "Не указана"

            # Город
            city_tag = block.find('span', {'data-qa': 'vacancy-serp__vacancy-address'})
            city = city_tag.get_text(strip=True).split(',')[0] if city_tag else "Не указан"

            try:
                vacancy = VacancyCreate(
                    title=title,
                    company=company,
                    salary=salary,
                    city=city,
                    link=link,
                    parsed_at=current_time
                )
                all_vacancies.append(vacancy)
            except Exception as e:
                logger.error(f"Validation error for vacancy '{title}': {e}")
                continue

        time.sleep(2)

    logger.info(f"Parsed {len(all_vacancies)} vacancies from {pages} pages.")
    return all_vacancies