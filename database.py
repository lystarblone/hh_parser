from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, VacancyORM
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_vacancies_to_db(vacancies: list):
    db = SessionLocal()
    saved_count = 0

    for vac_data in vacancies:
        if hasattr(vac_data, "model_dump"):
            vac_data = vac_data.model_dump()

        db_vacancy = VacancyORM(**vac_data)

        db.add(db_vacancy)
        try:
            db.commit()
            saved_count += 1
        except IntegrityError:
            db.rollback()
            continue

    db.close()
    return saved_count

def get_sample_from_db(limit=5):
    db = SessionLocal()
    vacancies = db.query(VacancyORM).limit(limit).all()
    db.close()
    return [(v.title, v.company, v.salary) for v in vacancies]