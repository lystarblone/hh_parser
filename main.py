import json
import logging
from parser import parse_vacancies
from database import init_db, save_vacancies_to_db, get_sample_from_db
from config import DEFAULT_QUERY, DEFAULT_AREA, DEFAULT_PAGES, JSON_FILE

LOG_FILE = "app.log"

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)

def save_to_json(vacancies, filename=JSON_FILE):
    try:
        data = [v.model_dump() for v in vacancies]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved {len(vacancies)} vacancies to {filename}")
    except Exception as e:
        logger.error(f"Failed to save to JSON: {e}")

def main():
    logger.info("Parser started")

    query = DEFAULT_QUERY
    area = DEFAULT_AREA
    pages = DEFAULT_PAGES

    try:
        init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Database init failed: {e}")
        return

    logger.info(f"Parsing with: query='{query}', area={area}, pages={pages}")

    try:
        vacancies = parse_vacancies(query, area=area, pages=pages)
    except Exception as e:
        logger.error(f"Parsing failed: {e}")
        return

    if not vacancies:
        logger.warning("No vacancies found")
        return

    try:
        saved_count = save_vacancies_to_db(vacancies)
        save_to_json(vacancies)
    except Exception as e:
        logger.error(f"Failed to save data: {e}")
        return

    logger.info(f"Total parsed: {len(vacancies)}")
    logger.info(f"Saved to DB: {saved_count}")
    logger.info(f"Skipped duplicates: {len(vacancies) - saved_count}")

    try:
        sample = get_sample_from_db(3)
        logger.info("Sample from database:")
        for title, company, salary in sample:
            logger.info(f"Title: {title} | Company: {company} | Salary: {salary}")
    except Exception as e:
        logger.error(f"Failed to fetch sample from DB: {e}")

    logger.info("Parsing completed successfully")

if __name__ == "__main__":
    main()