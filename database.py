# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "mysql+pymysql://tasksuser:taskspass@localhost:3306/tasksdb"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine)
# Base = declarative_base()

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "tasksuser")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "taskspass")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/tasksdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
