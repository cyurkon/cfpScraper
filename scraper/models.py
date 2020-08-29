import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()
env = os.getenv("ENV_TYPE")
if env == "prod":
    engine = create_engine(os.getenv("DATABASE_URL"))
else:
    engine = create_engine("sqlite:///cfpScraper.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Companies(Base):
    __tablename__ = "Companies"

    name = Column(String(100), primary_key=True)
    num_slots = Column(Integer)


Base.metadata.create_all(engine)

