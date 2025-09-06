import json
import logging
from parser import parse_vacancies
from database import init_db, save_vacancies_to_db, get_sample_from_db
from config import DEFAULT_QUERY, DEFAULT_AREA, DEFAULT_PAGES, JSON_FILE

LOG_FILE = "app.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def save_to_json(vacancies, filename=JSON_FILE):
    try:
        data = [v.model_dump() for v in vacancies]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ Сохранено {len(vacancies)} вакансий в {filename}")
    except Exception as e:
        logger.error(f"❌ Ошибка при сохранении в JSON: {e}")

def main():
    logger.info("🚀 Запуск парсера hh.ru с ORM и логированием")

    try:
        init_db()
        logger.info("✅ База данных инициализирована")
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации БД: {e}")
        return

    query = input("🔍 Введите поисковый запрос (Enter для 'python'): ").strip() or DEFAULT_QUERY
    area = input("🌍 Регион (1 — Москва, 2 — СПб, Enter для 1): ").strip() or str(DEFAULT_AREA)
    pages = input("📄 Сколько страниц парсить? (Enter для 3): ").strip() or str(DEFAULT_PAGES)

    try:
        area = int(area)
        pages = int(pages)
        logger.info(f"🔎 Параметры: запрос='{query}', регион={area}, страниц={pages}")
    except ValueError:
        logger.warning("⚠️ Некорректные параметры, используем значения по умолчанию.")
        area = DEFAULT_AREA
        pages = DEFAULT_PAGES

    try:
        vacancies = parse_vacancies(query, area=area, pages=pages)
    except Exception as e:
        logger.error(f"❌ Ошибка при парсинге: {e}")
        return

    if not vacancies:
        logger.warning("😔 Ничего не удалось спарсить.")
        return

    try:
        saved_count = save_vacancies_to_db(vacancies)
        save_to_json(vacancies)
    except Exception as e:
        logger.error(f"❌ Ошибка при сохранении данных: {e}")
        return

    logger.info(f"📊 Итоги:")
    logger.info(f"   Всего найдено: {len(vacancies)}")
    logger.info(f"   Уникальных (сохранено в БД): {saved_count}")
    logger.info(f"   Дубликатов пропущено: {len(vacancies) - saved_count}")
    try:
        sample = get_sample_from_db(3)
        logger.info("📋 Примеры из базы данных:")
        for title, company, salary in sample:
            logger.info(f"   💼 {title} | 🏢 {company} | 💰 {salary}")
    except Exception as e:
        logger.error(f"❌ Ошибка при получении образца из БД: {e}")

    logger.info("🏁 Парсинг завершён успешно")

if __name__ == "__main__":
    main()