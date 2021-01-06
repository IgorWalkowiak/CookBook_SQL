from database import init_db, db_session
from models import User, Recipe, Ingredients, Step, Tag, RecipesType, Vote
from flask import Flask, redirect, url_for, render_template, request
import parser


app = Flask(__name__)
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recipes/newRecipe.html', methods=['GET','POST'])
def newRecipe():
    if request.method == 'POST':
        recipe = parser.getRecipe(request.form, 1)
        db_session.add(recipe)
        db_session.commit()

        ingredients = parser.getIngredients(request.form, recipe.id)
        steps = parser.getSteps(request.form, recipe.id)
        tags, tagsConnections = parser.getTags(request.form, recipe.id)

        for ingredient in ingredients:
            db_session.add(ingredient)
        for step in steps:
            db_session.add(step)
        for tag in tags:
            db_session.add(tag)
        #for tagConnections in tagsConnections:
        #    db_session.add(tagConnections)
        db_session.commit()
        return render_template('index.html')
    else:
        return render_template('recipes/newRecipe.html')

if __name__ == '__main__':
    app.run()