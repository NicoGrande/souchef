from dataclasses import dataclass
from uuid import UUID
from item import Item
from enum import Enum

@dataclass
class recipe:
    """Class representing meal recipe"""
    
    recipe_id: UUID
    recipe_name: str
    recipe_style: Enum # appetizer, entree, dessert, etc.
    recipe_cuisine: Enum
    recipe_description: str
    recipe_instructions: dict[int, str]
    recipe_ingredients: dict[Item, float]
    
    # Ideas: add/remove instructions, add/remove ingredients, update recipe name, style, etc., 
    
    
    