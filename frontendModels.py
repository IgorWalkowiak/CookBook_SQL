
class Recipe:
    def __init__(self, id, owner, title, description, calories, steps, ingredients, video, tags, votesUp, votesDown):
        self.id = id
        self.owner = owner
        self.title = title
        self.description = description
        self.calories = calories
        self.steps = steps
        self.ingredients = ingredients
        self.video = Recipe.parseYTlink(video)
        self.tags = tags
        self.votesUp = votesUp
        self.votesDown = votesDown

    def parseYTlink(link):
        if link is None:
            return None
        lastSlash = link.rfind('/')
        yt_link = 'https://youtube.com/embed'+link[lastSlash:]
        print(yt_link)
        return yt_link
