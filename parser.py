from models import User, Recipe, Ingredients, Step, Tag, RecipesType, Vote

TITLE_ID = 'title'
DESCRIPTION_ID = 'description'
CALORIES_ID = 'calories'
INGREDIENT_NAME_ID = 'ingredientName'
INGREDIENT_UNIT_ID = 'ingredientUnit'
INGREDIENT_AMOUNT_ID = 'ingredientAmount'
STEP_ID = 'step'
TAG_ID = 'tags'
TAG_SEPARATOR = ", "

def getRecipe(data, ownerId):
    title = data[TITLE_ID]
    desc = data[DESCRIPTION_ID]
    calories = data[CALORIES_ID]
    recipe = Recipe(ownerId, title, desc, calories)
    return recipe


def getIngredients(data, recipeId):
    ingredients = []
    for i in range(1,20,1):
        try:
            name = data[INGREDIENT_NAME_ID+str(i)]
            unit = data[INGREDIENT_UNIT_ID+str(i)]
            amount = data[INGREDIENT_AMOUNT_ID+str(i)]
            ingredients.append(Ingredients(recipeId, name, unit, amount))
        except:
            break
    return ingredients


def getSteps(data, recipeId):
    steps = []
    for i in range(1,20,1):
        try:
            desc = data[STEP_ID+str(i)]
            steps.append(Step(recipeId, desc))
        except:
            break
    return steps


def getTags(data, recipeId):
    rawData = data[TAG_ID]
    tagNames = rawData.split(TAG_SEPARATOR)
    tags = []
    tagConnections = []
    for tag in tagNames:
        tempTag = Tag(tag)
        tags.append(tempTag)
        tagConnections.append(RecipesType(tempTag.id, recipeId))

    return tags, tagConnections