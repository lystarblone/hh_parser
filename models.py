from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Mapped
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from config import DATABASE_URL

Base = declarative_base()

class VacancyORM(Base):
    __tablename__ = 'vacancies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String)
    salary = Column(String)
    city = Column(String)
    link = Column(String, unique=True, index=True)
    parsed_at = Column(String)
    description: Mapped[str] = Column(String)

    def __repr__(self):
        return f"<VacancyORM(title='{self.title}', company='{self.company}')>"

class VacancyBase(BaseModel):
    title: str
    company: str
    salary: str
    city: str
    link: str
    parsed_at: str
    description: str

    class Config:
        from_attributes = True

class VacancyCreate(VacancyBase):
    pass

class Vacancy(VacancyBase):
    id: int

    class Config:
        from_attributes = True