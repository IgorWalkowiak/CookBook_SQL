from database import init_db, db_session
from models import Tag, RecipesType, User, Recipe, Step, Ingredients, Vote


def removeRecipe(recipeId):
    Vote.query.filter(Vote.target == recipeId).delete(synchronize_session=False)
    Step.query.filter(Step.recipe == recipeId).delete(synchronize_session=False)
    RecipesType.query.filter(RecipesType.recipe == recipeId).delete(synchronize_session=False)
    Ingredients.query.filter(Ingredients.recipe == recipeId).delete(synchronize_session=False)
    Recipe.query.filter(Recipe.id == recipeId).delete(synchronize_session=False)
    db_session.commit()