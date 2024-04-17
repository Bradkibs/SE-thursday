from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import PostgresDsn

POSTGRES_URL = PostgresDsn("postgresql://ethnpwjw:Yu-wFVfQG5ERNe8M6wAz6E4cDg4nljxF@kala.db.elephantsql.com/ethnpwjw")
DB_URL = POSTGRES_URL.unicode_string()

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()