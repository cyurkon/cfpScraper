import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
env = os.getenv("ENV_TYPE")
if env == "dev":
    engine = create_engine("sqlite:///timeslots.db")
elif env == "prod":
    engine = create_engine("")
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Timeslots(Base):
    __tablename__ = "Timeslots"

    id = Column(Integer, primary_key=True)
    timeslots = Column(JSON)


Base.metadata.create_all(engine)

