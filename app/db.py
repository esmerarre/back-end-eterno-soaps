from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

if not DATABASE_URI:
    raise RuntimeError("No DATABASE_URI set or loaded")

#for fastAPI we need:
# 1) create engine
# 2) create session uses engine in 1)
# 3) create base class -- used by models
# 4) get_db function -- used by routes to get a session


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from .models.base import Base

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
