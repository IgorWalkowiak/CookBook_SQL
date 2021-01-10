from database import init_db, db_session
from models import Tag, RecipesType, User, Vote, Recipe
from flask import Flask, render_template, request
import credentials
import parser
import userSystem
import recipeSystem

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
    if userSystem.isLoggedIn():
        return render_template('/index.html')
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
    if userSystem.isLoggedIn():
        return render_template('/index.html')
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


@app.route('/admin')
def admin():
    if userSystem.isLoggedIn():
        if userSystem.isAdmin():
            users = User.query.all()
            return render_template('/login/adminPanel.html', users=users)
    return render_template('/index.html')

@app.route('/admin/remove/<usr>')
def adminRemoveUser(usr):
    if userSystem.isLoggedIn():
        if userSystem.isAdmin():
            userSystem.removeUser(usr)
    return admin()


@app.route('/admin/makeAdmin/<usr>')
def adminMakeAdmin(usr):
    if userSystem.isLoggedIn():
        if userSystem.isAdmin():
            user = User.query.filter(User.id == usr).first()
            user.privileges = User.Privileges.admin
            db_session.add(user)
            db_session.commit()
    return admin()



@app.route('/admin/makeChef/<usr>')
def adminMakeChef(usr):
    if userSystem.isLoggedIn():
        if userSystem.isAdmin():
            user = User.query.filter(User.id == usr).first()
            user.privileges = User.Privileges.chef
            db_session.add(user)
            db_session.commit()
    return admin()


@app.route('/recipes/browseRecipes', methods=['GET', 'POST'])
def browseRecipes():
    if request.method == 'GET':
        front_recipes = recipeSystem.getAllRecipes()
        return render_template('recipes/browseRecipes.html', recipes=front_recipes)
    elif request.method == 'POST':
        sortMethod = parser.getSortMethod(request.form)
        tagToSearch = parser.getTagSearch(request.form)
        textToSearch = parser.getTextSearch(request.form)
        front_recipes = recipeSystem.getSpecificRecipe(sortMethod, tagToSearch, textToSearch)
        return render_template('recipes/browseRecipes.html', recipes=front_recipes)


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


@app.route('/recipes/removeRecipe/<recipeId>')
def removeRecipe(recipeId):
    recipeSystem.removeRecipe(recipeId)
    return render_template('/index.html')


@app.route('/recipes/recipe/<recipeId>')
def recipe(recipeId):
    front_recipe = recipeSystem.getRecipe(recipeId)
    return render_template('recipes/recipe.html', recipe=front_recipe)


@app.route('/recipes/voteUp/<recipeId>')
def voteUp(recipeId):
    if userSystem.isLoggedIn():
        Vote.query.filter(Vote.fromUser == userSystem.getUserId()).filter(Vote.target == recipeId).delete(synchronize_session=False)
        db_session.commit()

        vote = Vote(userSystem.getUserId(), recipeId, Vote.VoteType.up)
        db_session.add(vote)
        db_session.commit()
    return recipe(recipeId)


@app.route('/recipes/voteDown/<recipeId>')
def voteDown(recipeId):
    if userSystem.isLoggedIn():
        Vote.query.filter(Vote.fromUser == userSystem.getUserId()).filter(Vote.target == recipeId).delete(synchronize_session=False)
        db_session.commit()

        vote = Vote(userSystem.getUserId(), recipeId, Vote.VoteType.down)
        db_session.add(vote)
        db_session.commit()
    return recipe(recipeId)


if __name__ == '__main__':
    app.run()