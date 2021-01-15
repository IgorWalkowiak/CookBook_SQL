from flask import render_template
from models import User, Vote
from database import db_session
import userSystem
import parser
from recipeSystem import recipe_system


def homePage():
    return render_template('index.html')


def logoutPage():
    userSystem.logout()
    return render_template('index.html')


def loginPage(network_data=None):
    if userSystem.isLoggedIn():
        return render_template('/index.html')
    if network_data is None:
        return render_template('/login/login.html')
    else:
        login = parser.getLogin(network_data)
        password = parser.getPassword(network_data)
        loggedIn = userSystem.tryLogin(login, password)
        if loggedIn:
            return render_template('/index.html')
        else:
            return render_template('/login/login.html', failed=True)


def registerPage(network_data=None):
    if userSystem.isLoggedIn():
        return render_template('/index.html')
    if network_data is None:
        return render_template('/login/register.html')
    else:
        login = parser.getLogin(network_data)
        password = parser.getPassword(network_data)
        registered = userSystem.tryRegister(login, password)
        if registered:
            return render_template('/index.html')
        else:
            return render_template('/login/register.html', failed=True)


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


def browseRecipesPage(network_data=None):
    if network_data is None:
        front_recipes = recipe_system.getAllRecipes()
        return render_template('recipes/browseRecipes.html', recipes=front_recipes)
    else:
        sortMethod = parser.getSortMethod(network_data)
        tagToSearch = parser.getTagSearch(network_data)
        textToSearch = parser.getTextSearch(network_data)
        front_recipes = recipe_system.getSpecificRecipe(sortMethod, tagToSearch, textToSearch)
        return render_template('recipes/browseRecipes.html', recipes=front_recipes)

def newRecipePage(network_data=None):
    if userSystem.isLoggedIn():
        if network_data is None:
            return render_template('recipes/newRecipe.html')
        else:
            recipe_system.addRecipe(network_data)
            return render_template('index.html')
    else:
        return render_template('/login/login.html')


def removeRecipePage(recipeId):
    recipe_system.removeRecipe(recipeId, userSystem.getUserId())
    return browseRecipesPage()


def recipePage(recipeId):
    front_recipe = recipe_system.getRecipe(recipeId)
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
