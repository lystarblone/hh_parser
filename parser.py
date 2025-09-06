import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from config import HEADERS
from models import VacancyCreate

def parse_vacancies(query, area=1, pages=2):
    all_vacancies = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for page in range(pages):
        print(f"📄 Парсим страницу {page + 1} из {pages}...")

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
        except requests.RequestException as e:
            print(f"❌ Ошибка при запросе: {e}")
            break

        soup = BeautifulSoup(response.text, 'lxml')
        vacancy_blocks = soup.find_all('div', class_='vacancy-serp-item__layout')

        if not vacancy_blocks:
            print("⚠️ Вакансии не найдены — возможно, конец списка или изменилась верстка")
            break

        for block in vacancy_blocks:
            title_tag = block.find('a', class_='serp-item__title')
            title = title_tag.get_text(strip=True) if title_tag else "Без названия"
            link = title_tag['href'] if title_tag else ""

            company_tag = block.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})
            company = company_tag.get_text(strip=True) if company_tag else "Не указана"

            salary_tag = block.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            salary = salary_tag.get_text(strip=True) if salary_tag else "Не указана"

            city_tag = block.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})
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
                print(f"❌ Ошибка валидации вакансии: {e}")
                continue

        time.sleep(1.5)

    print(f"✅ Спарсено {len(all_vacancies)} вакансий")
    return all_vacancies