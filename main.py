from database import init_db, db_session
from models import User, Recipe, Ingredients, Step, Tag, RecipesType, Vote

init_db()
#u = User('igor', 'admin@localho4st', User.Privileges.guest)
#db_session.add(u)
#db_session.commit()

rec = Recipe(2, 'KURCZAK', 'Bardzo smaczny kurczak', 500)
db_session.add(rec)
db_session.commit()

a = User.query.filter(User.name == 'igor').first()
print(a.id)
rec = Recipe(a.id, 'NOWY', 'Badsadasdsadaak', 511100)
db_session.add(rec)
db_session.commit()