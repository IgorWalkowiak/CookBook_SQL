from __future__ import annotations
import OBS_interface
import parser
from database import db_session
from models import Tag, RecipesType


class TagCreator(OBS_interface.Observer):
    def update(self, recipeId, network_data) -> None:
        tags = parser.getTags(network_data)
        for tag in tags:
            db_session.add(tag)
            try:
                db_session.commit()
            except Exception as err:
                db_session.rollback()
            tag = Tag.query.filter(Tag.name == tag.name).first()
            tagConnection = RecipesType(tag.id, recipeId)
            db_session.add(tagConnection)
            db_session.commit()


class IngredientCreator(OBS_interface.Observer):
    def update(self, recipeId, network_data) -> None:
        ingredients = parser.getIngredients(network_data, recipeId)
        for ingredient in ingredients:
            db_session.add(ingredient)
            db_session.commit()


class StepCreator(OBS_interface.Observer):
    def update(self, recipeId, network_data) -> None:
        steps = parser.getSteps(network_data, recipeId)
        for step in steps:
            db_session.add(step)
        db_session.commit()





