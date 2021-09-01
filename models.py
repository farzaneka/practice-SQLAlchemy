import unittest

import pytest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, create_engine, \
    ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship


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
    projects = relationship('Project', back_populates='manager_id')


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    title = Column('title', String)
    primary_manager_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column('created_at', DateTime)
    modified_at = Column('modified_at', DateTime)
    manager_id = relationship('User', back_populates='projects')


Base.metadata.create_all(bind=engine)


class TestUser(unittest.TestCase):

    def setUp(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.session.query(User).delete()

        self.user_1 = User(
            first_name='first_user_name',
            last_name='first_user_last_name'
        )
        self.session.add(self.user_1)

        self.user_2 = User(
            first_name='second_user_name',
            last_name='second_user_last_name'
        )
        self.session.add(self.user_2)

        self.user_3 = User(
            first_name='third_user_name',
            last_name='third_user_last_name'
        )
        self.session.add(self.user_3)
        self.session.commit()

    def test_get_user(self):
        first_user = self.session.query(User) \
            .filter(User.first_name == 'first_user_name')
        first_user_exists = self.session.query(first_user.exists()).first()
        assert first_user_exists[0] == True

        user_order_by_id = self.session.query(User) \
            .order_by(User.id) \
            .all()
        assert len(user_order_by_id) == 3
        assert user_order_by_id[0].id < user_order_by_id[1].id < \
            user_order_by_id[2].id

        unique_user =  self.session.query(User) \
            .filter(User.first_name == 'second_user_name') \
            .one()
        assert unique_user.last_name == 'second_user_last_name'

        user_count = self.session.query(User) \
            .filter(User.first_name == 'first_user_name') \
            .count()
        assert user_count == 1

        user_filter_by_first_name =  self.session.query(User) \
            .filter(User.first_name == 'foo') \
            .one_or_none()
        assert user_filter_by_first_name == None

        total_users = self.session.query(User).all()
        assert total_users[0].first_name == 'first_user_name'

        user_get_by_id =  self.session.query(User) \
            .get(self.user_1.id)
        assert user_get_by_id.first_name == 'first_user_name'

        user_get_by_two_limit = self.session.query(User) \
            .limit(2) \
            .all()
        assert len(user_get_by_two_limit) == 2

