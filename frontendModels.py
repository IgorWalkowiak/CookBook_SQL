
class Recipe:
    def __init__(self, id, owner, title, description, calories, steps, ingredients, tags, votesUp, votesDown):
        self.id = id
        self.owner = owner
        self.title = title
        self.description = description
        self.calories = calories
        self.steps = steps
        self.ingredients = ingredients
        self.tags = tags
        self.votesUp = votesUp
        self.votesDown = votesDown