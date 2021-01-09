from database import init_db, db_session
from models import Tag, RecipesType, User, Recipe, Step, Ingredients
from flask import Flask, render_template, request, session
import credentials
import parser
import userSystem
import frontendModels

app = Flask(__name__)
app.secret_key = credentials.sessionSecretKey
init_db()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/logout')
def logout():
    userSystem.logout()
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = parser.getLogin(request.form)
        password = parser.getPassword(request.form)
        loggedIn = userSystem.tryLogin(login, password)
        if loggedIn:
            return render_template('/index.html')
        else:
            return render_template('/login/login.html', failed=True)
    else:
        return render_template('/login/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = parser.getLogin(request.form)
        password = parser.getPassword(request.form)
        registered = userSystem.tryRegister(login, password)
        if registered:
            return render_template('/index.html')
        else:
            return render_template('/login/register.html', failed=True)
    else:
        return render_template('/login/register.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    isAdmin = True
    #isAdmin = userSystem.isAdmin(login)
    if isAdmin:
        users = User.query.all()
        return render_template('/login/adminPanel.html', users=users)
    return render_template('/index.html')


@app.route('/admin/remove/<usr>')
def adminRemoveUser(usr):
    User.query.filter(User.name == usr).delete(synchronize_session=False)
    db_session.commit()
    return render_template('/index.html')


@app.route('/admin/makeAdmin/<usr>')
def adminMakeAdmin(usr):
    pass


@app.route('/admin/makeChef/<usr>')
def adminMakeChef(usr):
    pass


@app.route('/recipes/browseRecipes')
def browseRecipes():
    recipesFromDb = Recipe.query.all()
    recipes = []
    for dbRecipe in recipesFromDb:
        dbSteps = Step.query.filter(Step.recipe == dbRecipe.id).all()
        dbOwner = User.query.filter(User.id == dbRecipe.owner).first()
        dbIngredients = Ingredients.query.filter(Ingredients.recipe == dbRecipe.id).all()
        dbTags = (db_session.query(Tag)
                  .join(RecipesType, RecipesType.tag == Tag.id)) \
            .filter(RecipesType.recipe == dbRecipe.id)
        print(dbOwner)
        for tag in dbTags:
            print("tag")
            print(tag.name)
        for step in dbSteps:
            print("step")
            print(step.description)
        for ingred in dbIngredients:
            print("ingred")
            print(ingred.name)
        print("END\n\n")

    return render_template('index.html')


@app.route('/recipes/newRecipe', methods=['GET', 'POST'])
def newRecipe():
    if userSystem.isLoggedIn():
        if request.method == 'POST':
            recipe = parser.getRecipe(request.form, userSystem.getUserId())
            db_session.add(recipe)
            db_session.commit()

            ingredients = parser.getIngredients(request.form, recipe.id)
            steps = parser.getSteps(request.form, recipe.id)
            tags = parser.getTags(request.form)

            for ingredient in ingredients:
                db_session.add(ingredient)
            for step in steps:
                db_session.add(step)
            db_session.commit()

            for tag in tags:
                print(tag)
                db_session.add(tag)
                try:
                    db_session.commit()
                except Exception as err:
                    db_session.rollback()
                tag = Tag.query.filter(Tag.name == tag.name).first()
                tagConnection = RecipesType(tag.id, recipe.id)
                db_session.add(tagConnection)
                db_session.commit()
            return render_template('index.html')
        else:
            return render_template('recipes/newRecipe.html')
    else:
        return render_template('/login/login.html')





if __name__ == '__main__':
    app.run()