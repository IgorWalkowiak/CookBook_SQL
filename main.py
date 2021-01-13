from database import init_db
from flask import Flask
import credentials
import controller


app = Flask(__name__)
app.secret_key = credentials.sessionSecretKey
init_db()

@app.route('/')
def home():
    return controller.homePage()


@app.route('/logout')
def logout():
    return controller.logoutPage()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return controller.loginPage()


@app.route('/register', methods=['GET', 'POST'])
def register():
    return controller.registerPage()


@app.route('/admin')
def admin():
    return controller.adminPage()


@app.route('/admin/remove/<usr>')
def adminRemoveUser(usr):
    return controller.adminRemoveUserPage(usr)


@app.route('/admin/makeAdmin/<usr>')
def adminMakeAdmin(usr):
    return controller.makeAdminPage(usr)


@app.route('/admin/makeChef/<usr>')
def adminMakeChef(usr):
    return controller.makeChefPage(usr)


@app.route('/recipes/browseRecipes', methods=['GET', 'POST'])
def browseRecipes():
    return controller.browseRecipesPage()


@app.route('/recipes/newRecipe', methods=['GET', 'POST'])
def newRecipe():
    return controller.newRecipePage()


@app.route('/recipes/removeRecipe/<recipeId>')
def removeRecipe(recipeId):
    return controller.removeRecipePage(recipeId)


@app.route('/recipes/recipe/<recipeId>')
def recipe(recipeId):
    print('route')
    return controller.recipePage(recipeId)


@app.route('/recipes/voteUp/<recipeId>')
def voteUp(recipeId):
    return controller.voteUpPage(recipeId)


@app.route('/recipes/voteDown/<recipeId>')
def voteDown(recipeId):
    return controller.voteDownPage(recipeId)


if __name__ == '__main__':
    app.run(host='192.168.0.109')