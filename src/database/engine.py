from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase


engine = create_engine('sqlite:///database.db')

class Base(DeclarativeBase):
    pass




