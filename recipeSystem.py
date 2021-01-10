from database import init_db, db_session
from models import Tag, RecipesType, User, Recipe, Step, Ingredients, Vote
import frontendModels

def removeRecipe(recipeId):
    Vote.query.filter(Vote.target == recipeId).delete(synchronize_session=False)
    Step.query.filter(Step.recipe == recipeId).delete(synchronize_session=False)
    RecipesType.query.filter(RecipesType.recipe == recipeId).delete(synchronize_session=False)
    Ingredients.query.filter(Ingredients.recipe == recipeId).delete(synchronize_session=False)
    Recipe.query.filter(Recipe.id == recipeId).delete(synchronize_session=False)
    db_session.commit()

def getRecipe(recipeId):
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
    return recipe