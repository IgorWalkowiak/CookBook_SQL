from database import init_db, db_session
from sqlalchemy import func, case
from models import Tag, RecipesType, User, Recipe, Step, Ingredients, Vote
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


@app.route('/admin')
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


@app.route('/recipes/browseRecipes', methods=['GET', 'POST'])
def browseRecipes():
    if request.method == 'GET':
        recipesFromDb = Recipe.query.all()
        recipes = []
        for dbRecipe in recipesFromDb:
            dbSteps = Step.query.filter(Step.recipe == dbRecipe.id).all()
            dbOwner = User.query.filter(User.id == dbRecipe.owner).first()
            dbIngredients = Ingredients.query.filter(Ingredients.recipe == dbRecipe.id).all()
            dbVotesUp = Vote.query.filter(Vote.voteType == Vote.VoteType.up).filter(Vote.target == dbRecipe.id).count()
            dbVotesDown = Vote.query.filter(Vote.voteType == Vote.VoteType.down).filter(Vote.target == dbRecipe.id).count()
            dbTags = (db_session.query(Tag)
                      .join(RecipesType, RecipesType.tag == Tag.id)) \
                .filter(RecipesType.recipe == dbRecipe.id)
            recipe = frontendModels.Recipe(dbRecipe.id, dbOwner.name, dbRecipe.title, dbRecipe.description, dbRecipe.calories, dbSteps,
                                           dbIngredients, dbTags, dbVotesUp, dbVotesDown)
            recipes.append(recipe)
        return render_template('recipes/browseRecipes.html', recipes=recipes)
    elif request.method == 'POST':
        sortMethod = parser.getSortMethod(request.form)
        tagToSearch = parser.getTagSearch(request.form)
        textToSearch = parser.getTextSearch(request.form)
        mainQuery = Recipe.query
        if textToSearch != '':
            mainQuery = mainQuery.filter(Recipe.description.contains('ryba'))
        if sortMethod == 'fromWorst':
            my_case = case(
                [
                    (Vote.voteType == Vote.VoteType.up, 1),
                    (Vote.voteType == Vote.VoteType.down, -1)
                ]
            )
            sumOfVotes = db_session.query(
                Recipe.id.label('recipe_id'), Vote.voteType, func.sum(my_case).label('voteTypeCount')
            ).group_by(Recipe.id, Vote.voteType).filter(Recipe.id == Vote.target).subquery()
            mainQuery = mainQuery.join(
                sumOfVotes, Recipe.id == sumOfVotes.c.recipe_id).order_by(sumOfVotes.c.voteTypeCount.asc())
        elif sortMethod == 'fromBest':
            my_case = case(
                [
                    (Vote.voteType == Vote.VoteType.up, 1),
                    (Vote.voteType == Vote.VoteType.down, -1)
                ]
            )
            sumOfVotes = db_session.query(
                Recipe.id.label('recipe_id'), Vote.voteType, func.sum(my_case).label('voteTypeCount')
            ).group_by(Recipe.id, Vote.voteType).filter(Recipe.id == Vote.target).subquery()
            mainQuery = mainQuery.join(
                sumOfVotes, Recipe.id == sumOfVotes.c.recipe_id).order_by(sumOfVotes.c.voteTypeCount.desc())
        else:
            pass

        if tagToSearch != '':
            tag = Tag.query.filter(Tag.name == tagToSearch).first()
            if tag is not None:
                tagConnections = RecipesType.query.filter(RecipesType.tag == tag.id).all()
                ids = [x.recipe for x in tagConnections]
                mainQuery = mainQuery.filter(Recipe.id.in_(ids))
            else:
                mainQuery = mainQuery.filter(Recipe.id.in_((-1,-1)))
        recipesFromDb = mainQuery.all()
        recipes = []
        for dbRecipe in recipesFromDb:
            dbSteps = Step.query.filter(Step.recipe == dbRecipe.id).all()
            dbOwner = User.query.filter(User.id == dbRecipe.owner).first()
            dbIngredients = Ingredients.query.filter(Ingredients.recipe == dbRecipe.id).all()
            dbVotesUp = Vote.query.filter(Vote.voteType == Vote.VoteType.up).filter(Vote.target == dbRecipe.id).count()
            dbVotesDown = Vote.query.filter(Vote.voteType == Vote.VoteType.down).filter(Vote.target == dbRecipe.id).count()
            dbTags = (db_session.query(Tag)
                      .join(RecipesType, RecipesType.tag == Tag.id)) \
                .filter(RecipesType.recipe == dbRecipe.id)
            recipe = frontendModels.Recipe(dbRecipe.id, dbOwner.name, dbRecipe.title, dbRecipe.description, dbRecipe.calories, dbSteps,
                                           dbIngredients, dbTags, dbVotesUp, dbVotesDown)
            recipes.append(recipe)
        print(sortMethod)
        print(tagToSearch)
        print(textToSearch)
        return render_template('recipes/browseRecipes.html', recipes=recipes)



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


@app.route('/recipes/recipe/<recipeId>')
def recipe(recipeId):
    dbRecipe = Recipe.query.filter(Recipe.id == recipeId).first()
    dbSteps = Step.query.filter(Step.recipe == dbRecipe.id).all()
    dbOwner = User.query.filter(User.id == dbRecipe.owner).first()
    dbIngredients = Ingredients.query.filter(Ingredients.recipe == dbRecipe.id).all()
    dbVotesUp = Vote.query.filter(Vote.voteType == Vote.VoteType.up).filter(Vote.target == dbRecipe.id).count()
    dbVotesDown = Vote.query.filter(Vote.voteType == Vote.VoteType.down).filter(Vote.target == dbRecipe.id).count()
    dbTags = (db_session.query(Tag)
              .join(RecipesType, RecipesType.tag == Tag.id)) \
        .filter(RecipesType.recipe == dbRecipe.id)
    recipe = frontendModels.Recipe(dbRecipe.id, dbOwner.name, dbRecipe.title, dbRecipe.description, dbRecipe.calories, dbSteps,
                                   dbIngredients, dbTags, dbVotesUp, dbVotesDown)
    return render_template('recipes/recipe.html', recipe=recipe)



@app.route('/recipes/voteUp/<recipeId>')
def voteUp(recipeId):
    if userSystem.isLoggedIn():
        dbVote = Vote.query.filter(Vote.fromUser == userSystem.getUserId()).filter(Vote.target == recipeId).delete(synchronize_session=False)
        db_session.commit()

        vote = Vote(userSystem.getUserId(), recipeId, Vote.VoteType.up)
        db_session.add(vote)
        db_session.commit()
    return recipe(recipeId)


@app.route('/recipes/voteDown/<recipeId>')
def voteDown(recipeId):
    if userSystem.isLoggedIn():
        dbVote = Vote.query.filter(Vote.fromUser == userSystem.getUserId()).filter(Vote.target == recipeId).delete(synchronize_session=False)
        db_session.commit()

        vote = Vote(userSystem.getUserId(), recipeId, Vote.VoteType.down)
        db_session.add(vote)
        db_session.commit()
    return recipe(recipeId)


if __name__ == '__main__':
    app.run()