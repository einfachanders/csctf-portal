from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

engine = create_engine("sqlite+pysqlite:///data/csctf-portal.sqlite")

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()