import pytest

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, create_engine
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


def test_get_user():
    user_1 = User(first_name='user_1', last_name='user_1')

    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(user_1)
    session.commit()

    assert session.query(User).filter(User.first_name == 'foo').count() == 0
    #assert session.query(User).order_by(User.first_name)
    #assert session.query(User).filter(User.first_name == 'user_1').one()
    assert session.query(User).filter(User.first_name == 'foo').one_or_none() == None
    #assert session.query(User).all()
    query = session.query(User).filter(User.first_name == 'user_1')
    assert session.query(query.exists())
    assert session.query(User).get(1).first_name == 'farzaneh'
    #assert session.query(User).limit(5)

