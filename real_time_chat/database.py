from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from real_time_chat.config import settings


DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
