from database import init_db, db_session
from models import User, Recipe, Ingredients, Step, Tag, RecipesType, Vote

init_db()
u = User('admi321nfas4', 'admin@localho4st', User.Privileges.guest)
db_session.add(u)
db_session.commit()
a = User.query.all()
for user in a:
    print("AHOJ")
    print(user.privileges)
    print('\n')