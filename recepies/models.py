import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

recepie_ingredients = Table('recepie_ingredients', Base.metadata,
                                Column('recepie_id', Integer, ForeignKey('recepie.id')),
                                Column('variation_id', Integer, ForeignKey('ingredient_variation.id'))
                            )

ingredient_variation = Table('ingredient_variation', Base.metadata,
                                Column('id', Integer, primary_key=True),
                                Column('ingredient_id', Integer, ForeignKey('ingredient.id'))
                             )

class Ingredient(Base):

    __tablename__ = 'ingredient'

    def __init__(self, display_name):
        self.display_name = display_name

    id = Column(Integer, primary_key=True)

    display_name = Column(String, unique=True)

    recepies = relationship(
        'Recepie',
        secondary = ingredient_variation,
        secondaryjoin = sqlalchemy.and_(id == ingredient_variation.c.ingredient_id, recepie_ingredients.c.variation_id == ingredient_variation.c.id, sqlalchemy.text('recepie.id = recepie_ingredients.recepie_id'))
    )

    def toJSON(self):
        return {
            "id": self.id,
            "displayName": self.display_name
        }

class Recepie(Base):

    __tablename__ = 'recepie'

    def __init__(self, display_name):
        self.display_name = display_name

    id = Column(Integer, primary_key=True)

    display_name = Column(String, unique=True)

    ingredients = relationship(
        'Ingredient',
        secondary = recepie_ingredients,
        secondaryjoin = sqlalchemy.and_(id == recepie_ingredients.c.recepie_id, recepie_ingredients.c.variation_id == ingredient_variation.c.id, ingredient_variation.c.ingredient_id == Ingredient.id)
    )

    def toJSON(self):
        return {
            "displayName": self.display_name,
            "ingredients": [x.toJSON() for x in self.ingredients]
        }
