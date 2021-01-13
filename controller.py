from flask import render_template, request
from models import Tag, RecipesType, User, Vote
from database import db_session
import userSystem
import parser
import recipeSystem


def homePage():
    return render_template('index.html')


def logoutPage():
    userSystem.logout()
    return render_template('index.html')


def loginPage():
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

def registerPage():
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

def adminPage():
    if userSystem.isLoggedIn():
        if userSystem.isAdmin():
            users = User.query.all()
            return render_template('/login/adminPanel.html', users=users)
    return render_template('/index.html')


def adminRemoveUserPage(usr):
    if userSystem.isLoggedIn():
        if userSystem.isAdmin():
            userSystem.removeUser(usr)
    return adminPage()


def makeAdminPage(usr):
    if userSystem.isLoggedIn():
        if userSystem.isAdmin():
            user = User.query.filter(User.id == usr).first()
            user.privileges = User.Privileges.admin
            db_session.add(user)
            db_session.commit()
    return adminPage()


def makeChefPage(usr):
    if userSystem.isLoggedIn():
        if userSystem.isAdmin():
            user = User.query.filter(User.id == usr).first()
            user.privileges = User.Privileges.chef
            db_session.add(user)
            db_session.commit()
    return adminPage()


def browseRecipesPage():
    if request.method == 'GET':
        front_recipes = recipeSystem.getAllRecipes()
        return render_template('recipes/browseRecipes.html', recipes=front_recipes)
    elif request.method == 'POST':
        sortMethod = parser.getSortMethod(request.form)
        tagToSearch = parser.getTagSearch(request.form)
        textToSearch = parser.getTextSearch(request.form)
        front_recipes = recipeSystem.getSpecificRecipe(sortMethod, tagToSearch, textToSearch)
        return render_template('recipes/browseRecipes.html', recipes=front_recipes)

def newRecipePage():
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

def removeRecipePage(recipeId):
    recipeSystem.removeRecipe(recipeId, userSystem.getUserId())
    return browseRecipesPage()

def recipePage(recipeId):
    print('recipePage')
    front_recipe = recipeSystem.getRecipe(recipeId)
    return render_template('recipes/recipe.html', recipe=front_recipe)

def voteUpPage(recipeId):
    if userSystem.isLoggedIn():
        Vote.query.filter(Vote.fromUser == userSystem.getUserId()).filter(Vote.target == recipeId).delete(synchronize_session=False)
        db_session.commit()

        vote = Vote(userSystem.getUserId(), recipeId, Vote.VoteType.up)
        db_session.add(vote)
        db_session.commit()
    return recipePage(recipeId)

def voteDownPage(recipeId):
    if userSystem.isLoggedIn():
        Vote.query.filter(Vote.fromUser == userSystem.getUserId()).filter(Vote.target == recipeId).delete(synchronize_session=False)
        db_session.commit()

        vote = Vote(userSystem.getUserId(), recipeId, Vote.VoteType.down)
        db_session.add(vote)
        db_session.commit()
    return recipePage(recipeId)
