import pytest
import unittest

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    "postgres+psycopg2://postgres:postgres@localhost/sqlalchemy_practice"
)
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column('first_name',String)
    last_name = Column('last_name', String)
    birthday = Column('birthday', Date)


Base.metadata.create_all(bind=engine)


class TestUser(unittest.TestCase):

    def setUp(self):
        self.user_1 = User(
            first_name='first_user_name',
            last_name='first_user_last_name'
        )

        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.session.add(self.user_1)

    def test_get_user(self):
        query = self.session.query(User).filter(
            User.first_name == self.user_1.first_name
        )
        
        user_count = self.session.query(User) \
            .filter(User.first_name == self.user_1.first_name) \
            .count()
        assert user_count == 1
        
        assert self.session.query(User).order_by(User.last_name) != None
        assert self.session.query(User).filter(
            User.first_name == self.user_1.first_name).one() == self.user_1
        assert self.session.query(User).filter(
            User.first_name == 'foo').one_or_none() == None
        assert self.session.query(User).all()[0].first_name == \
            self.user_1.first_name
        assert self.session.query(query.exists())
        assert self.session.query(User).get(1) == None
        assert self.session.query(User).first() == self.user_1

