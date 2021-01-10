from database import db_session
from models import Tag, RecipesType, User, Recipe, Step, Ingredients, Vote
import frontendModels
from sqlalchemy import func, case


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


def getAllRecipes():
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
        recipe = frontendModels.Recipe(dbRecipe.id, dbOwner.name, dbRecipe.title, dbRecipe.description,
                                       dbRecipe.calories, dbSteps,
                                       dbIngredients, dbTags, dbVotesUp, dbVotesDown)
        recipes.append(recipe)
    return recipes


def getSpecificRecipe(sortMethod, tagToSearch, textToSearch):
    mainQuery = Recipe.query
    if textToSearch != '':
        mainQuery = mainQuery.filter(Recipe.description.contains(textToSearch))

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
            mainQuery = mainQuery.filter(Recipe.id.in_((-1, -1)))
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
        recipe = frontendModels.Recipe(dbRecipe.id, dbOwner.name, dbRecipe.title, dbRecipe.description,
                                       dbRecipe.calories, dbSteps,
                                       dbIngredients, dbTags, dbVotesUp, dbVotesDown)
        recipes.append(recipe)
    return recipes