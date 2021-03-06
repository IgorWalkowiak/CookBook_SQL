import enum
import credentials
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column, Integer, String, Enum, create_engine, ForeignKey

engine = create_engine('mysql://{}:{}@{}/cookbook'.format(credentials.login, credentials.password, credentials.host_address))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

meta = MetaData()


class Privileges(enum.Enum):
   chef = 1
   admin = 2

user = Table(
   'users', meta,
   Column('id', Integer, primary_key=True),
   Column('name', String(100), nullable=False),
   Column('password', String(100), nullable=False),
   Column('privileges', Enum(Privileges), nullable=False)
)

recipe = Table(
   'recipes', meta,
   Column('id', Integer, primary_key=True),
   Column('owner', Integer, ForeignKey("users.id", ondelete='CASCADE')),
   Column('title', String(100)),
   Column('description', String(1000)),
   Column('calories', Integer),
   Column('video', String(1000))
)

ingredient = Table(
   'ingredients', meta,
   Column('id', Integer, primary_key=True),
   Column('recipe', Integer, ForeignKey("recipes.id")),
   Column('name', String(100)),
   Column('unit', String(100)),
   Column('amount', Integer)
)

step = Table(
   'steps', meta,
   Column('id', Integer, primary_key=True),
   Column('recipe', Integer, ForeignKey("recipes.id"), nullable=False),
   Column('description', String(100), nullable=False),
)

tag = Table(
   'tags', meta,
   Column('id', Integer, primary_key=True),
   Column('name', String(100), unique=True, nullable=False),
)

recipes_type = Table(
   'recipes_types', meta,
   Column('id', Integer, primary_key=True),
   Column('tag', Integer, ForeignKey("tags.id"), nullable=False),
   Column('recipe', Integer, ForeignKey("recipes.id")),
)


class voteType(enum.Enum):
   up = 1
   down = 2


vote = Table(
   'votes', meta,
   Column('id', Integer, primary_key=True),
   Column('fromUser', Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False),
   Column('target', Integer, ForeignKey("recipes.id"), nullable=False),
   Column('voteType', Enum(voteType), nullable=False)
)

meta.create_all(engine)


def init_db():
    import models
    Base.metadata.create_all(bind=engine)