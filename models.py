import unittest

import pytest
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
        self.user_2 = User(
            first_name='second_user_name',
            last_name='second_user_last_name'
        )

        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.session.add(self.user_1)
        self.session.add(self.user_2)
        self.session.commit()

    def test_get_user(self):
        first_user = self.session.query(User) \
            .filter(User.first_name == 'first_user_name')
        first_user_exists = self.session.query(first_user.exists()).first()
        assert first_user_exists[0] == True

        user_order_by_last_name = self.session.query(User) \
            .order_by(User.last_name) \
            .all()
        assert user_order_by_last_name != None

        unique_user =  self.session.query(User) \
            .filter(User.first_name == 'second_user_name') \
            .limit(1) \
            .one()
        assert unique_user != None

        user_count = self.session.query(User) \
            .filter(User.first_name == 'first_user_name') \
            .limit(1) \
            .count()
        assert user_count == 1

        user_filter_by_first_name =  self.session.query(User) \
            .filter(User.first_name == 'foo') \
            .one_or_none()
        assert user_filter_by_first_name == None

        total_users = self.session.query(User).all()
        assert total_users[0].first_name == 'first_user_name'

        user_get_by_id =  self.session.query(User) \
            .get(self.user_1.id) \
            .first_name
        assert user_get_by_id == 'first_user_name'

