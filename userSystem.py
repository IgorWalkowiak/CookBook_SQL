from models import User
from database import db_session
from flask import session


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

    user = User(login, password, User.Privileges.guest)
    db_session.add(user)
    db_session.commit()
    session['loggedIn'] = login
    return True


def isAdmin(login):
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