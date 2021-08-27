import pytest

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, create_engine,insert
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgres+psycopg2://postgres:postgres@localhost/sqlalchemy_practice")
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column('first_name',String)
    last_name = Column('last_name', String)
    birthday = Column('birthday', Date)


Base.metadata.create_all(bind=engine)


Session = sessionmaker(bind=engine)
session = Session()
session.add(User(first_name='farzaneh', last_name='kamaloo'))
session.commit()


def test_get_user():
    assert session.query(User).get(1).first_name == 'farzaneh'

