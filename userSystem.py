from database import db_session
from flask import session
from models import User, Recipe, Vote
import recipeSystem


def isLoggedIn():
    try:
        if session['loggedIn'] != None:
            return True
    except KeyError:
        session['loggedIn'] = None

    return False


def logout():
    session['loggedIn'] = None


def tryLogin(login, password):
    user = User.query.filter(User.name == login).first()
    if user is None:
        return False

    if user.password == password:
        session['loggedIn'] = login
        return True
    else:
        return False


def tryRegister(login, password):
    user = User.query.filter(User.name == login).first()
    if user is not None:
        return False

    user = User(login, password, User.Privileges.chef)
    db_session.add(user)
    db_session.commit()
    session['loggedIn'] = login
    return True


def isAdmin():
    login = session['loggedIn']
    user = User.query.filter(User.name == login).first()
    if user is None:
        return False

    if user.privileges == User.Privileges.admin:
        return True
    return False


def getUserId():
    try:
        if session['loggedIn'] != None:
            user = User.query.filter(User.name == session['loggedIn']).first()
            return user.id
    except KeyError:
        session['loggedIn'] = None
    return -1


def removeUser(userId):
    ownedRecipes = Recipe.query.filter(Recipe.owner == userId)
    for recipe in ownedRecipes:
        recipeSystem.recipe_system.removeRecipe(recipe.id, userId)
    Vote.query.filter(Vote.fromUser == userId).delete(synchronize_session=False)
    User.query.filter(User.id == userId).delete(synchronize_session=False)
    db_session.commit()
