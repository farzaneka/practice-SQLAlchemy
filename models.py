import unittest
import datetime

import pytest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, create_engine, \
    ForeignKey, DateTime, event
from sqlalchemy.orm import sessionmaker, relationship, column_property


engine = create_engine(
    "postgres+psycopg2://postgres:postgres@localhost/sqlalchemy_practice"
)
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column('first_name', String)
    last_name = Column('last_name', String)
    full_name = column_property(first_name + ' ' + last_name)
    birthday = Column('birthday', Date, nullable=False)
    age = column_property(datetime.date.today() - birthday)
    projects = relationship(
        'Project',
        primaryjoin='Project.primary_manager_id == User.id',
        back_populates='manager'
    )
    secondary_projects = relationship(
        'Project',
        primaryjoin='Project.secondary_manager_id == User.id',
        back_populates='secondary_manager'
    )


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    title = Column('title', String)
    primary_manager_id = Column(Integer, ForeignKey('user.id'))
    secondary_manager_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column('created_at', DateTime, default=datetime.datetime.now())
    modified_at = Column('modified_at', DateTime)
    manager = relationship(
        'User',
        foreign_keys=[primary_manager_id],
        back_populates='projects'
    )
    secondary_manager = relationship(
        'User',
        foreign_keys=[secondary_manager_id],
        back_populates='secondary_projects'
    )


@event.listens_for(Project, 'after_update')
def receive_after_update(mapper, connection, target):
    traget.modified_at = datetime.datetime.now()


Base.metadata.create_all(bind=engine)


class TestUser(unittest.TestCase):

    def setUp(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.session.query(User).delete()
        self.session.query(Project).delete()

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

        self.project_1 = Project(
            title='first_project'
        )
        self.session.add(self.project_1)
        self.session.commit()

    def test_get_project(self):
        first_project = self.session.query(Project) \
            .get(self.project_1.id)
        assert first_project.title == 'first_project'

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
        assert unique_user.full_name == 'second_user_name second_user_last_name'

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

