
class Recipe:
    def __init__(self, owner, title, description, calories, steps, ingredients, tags, votesUp, votesDown):
        self.owner = owner
        self.title = title
        self.description = description
        self.calories = calories
        self.steps = steps
        self.ingredients = ingredients
        self.tags = tags
        self.votesUp = votesUp
        self.votesDown = votesDown
