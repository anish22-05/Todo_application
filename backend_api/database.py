from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Setting up database  
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR,'todo.db')}"

engine = create_engine( DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# Whenever this function will be called a session will be created for db operations.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
