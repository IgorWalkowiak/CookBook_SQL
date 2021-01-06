import enum
import credentials
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column, Integer, String, Enum, create_engine, ForeignKey

engine = create_engine('mysql://{}:{}@localhost/CookBook'.format(credentials.login,credentials.password))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

meta = MetaData()


class MyEnum(enum.Enum):
   guest = 1
   chef = 2
   admin = 3


user = Table(
   'users', meta,
   Column('id', Integer, primary_key=True),
   Column('name', String(100)),
   Column('password', String(100)),
   Column('privileges', Enum(MyEnum)),
)

recipe = Table(
   'recipes', meta,
   Column('id', Integer, primary_key=True),
   Column('owner', Integer, ForeignKey("users.id")),
   Column('title', String(100)),
   Column('description', String(1000)),
   Column('calories', Integer)
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
   Column('recipe', Integer, ForeignKey("recipes.id")),
   Column('description', String(100)),
)

tag = Table(
   'tags', meta,
   Column('id', Integer, primary_key=True),
   Column('name', String(100)),
)

recipes_type = Table(
   'recipes_types', meta,
   Column('id', Integer, primary_key=True),
   Column('tag', Integer, ForeignKey("tags.id"), nullable=False),
   Column('recipe', Integer, ForeignKey("recipes.id")),
)

vote = Table(
   'votes', meta,
   Column('id', Integer, primary_key=True),
   Column('from', Integer, ForeignKey("users.id"), nullable=False),
   Column('target', Integer, ForeignKey("recipes.id")),
)

meta.create_all(engine)


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)