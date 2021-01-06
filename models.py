import enum
from sqlalchemy import Column, Integer, String, Enum
from database import Base



class User(Base):
    __tablename__ = 'users'
    class Privileges(enum.Enum):
        guest = 1
        chef = 2
        admin = 3
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    password = Column(String(100))
    privileges = Column(Enum(Privileges))

    def __init__(self, name=None, password=None, privileges=None):
        self.name = name
        self.password = password
        self.privileges = privileges

    def __repr__(self):
        return '<User %r>' % (self.name)


class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    owner = Column(Integer)
    title = Column(String(100))
    description = Column(String(1000))
    calories = Column(Integer)

    def __init__(self, owner=None, title=None, description=None, calories=None):
        self.owner = owner
        self.title = title
        self.description = description
        self.calories = calories

    def __repr__(self):
        return '<title %r>' % (self.title)


class Ingredients(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    recipe = Column(Integer)
    name = Column(String(100))
    unit = Column(String(100))
    amount = Column(Integer)

    def __init__(self, recipe=None, name=None, unit=None, amount=None):
        self.recipe = recipe
        self.name = name
        self.unit = unit
        self.amount = amount

    def __repr__(self):
        return '<name %r>' % (self.name)


class Step(Base):
    __tablename__ = 'steps'
    id = Column(Integer, primary_key=True)
    recipe = Column(Integer)
    description = Column(String(1000))

    def __init__(self, recipe=None, description=None):
        self.recipe = recipe
        self.description = description

    def __repr__(self):
        return '<name %r>' % (self.name)


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<name %r>' % (self.name)


class RecipesType(Base):
    __tablename__ = 'recipes_types'
    id = Column(Integer, primary_key=True)
    tag = Column(Integer)
    recipe = Column(Integer)

    def __init__(self, tag=None, recipe=None):
        self.tag = tag
        self.recipe = recipe

    def __repr__(self):
        return '<tag %r>' % (self.tag)


class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    fromUser = Column(Integer)
    target = Column(Integer)

    def __init__(self, fromUser=None, target=None):
        self.fromUser = fromUser
        self.target = target

    def __repr__(self):
        return '<target %r>' % (self.target)