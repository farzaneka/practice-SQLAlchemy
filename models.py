import inspect

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, create_engine

engine = create_engine("postgres+psycopg2://postgres:postgres@localhost/sqlalchemy_test")

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column('first_name',String)
    last_name = Column('last_name', String)
    birthday = Column('birthday', Date)

Base.metadata.create_all(bind=engine)

