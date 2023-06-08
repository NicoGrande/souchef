from dataclasses import dataclass
from uuid import UUID
from item import Item
from enum import Enum
from quantity import Quantity

class Style(Enum):
    APPETIZER = "appetizer"
    ENTREE = "entree"
    DESSERT = "dessert"
    SNACK = "snack"
    NONE = ""
    
class Cuisine(Enum):
    ITALIAN = "italian"
    FRENCH = "french"
    SPANISH = "spanish"
    BRITISH = "british"
    GERMAN = "german"
    SCANDINAVIAN = "scandinavian"
    RUSSIAN = "russian"
    SLAVIC = "slavic"
    MEDITERRANEAN = "mediterranean"
    TURKISH = "turkish"
    EGYPTIAN = "egyptian"
    GHANAIAN = "ghanaian"
    ETHIOPIAN = "ethiopian"
    ARABIC = "arabic"
    INDIAN = "indian"
    CHINESE = "chinese"
    VIETNAMESE = "vietnamese"
    MALAYSIAN = "malaysian"
    FILIPINO = "filipino"
    JAPANESE = "japanese"
    KOREAN = "korean"
    AUSTRALIAN = "australian"
    CANADIAN = "canadian"
    AMERICAN = "american"
    NORTHEASTERN = "northeastern"
    MIDWESTERN = "midwestern"
    SOUTHWESTERN = "southwestern"
    SOUTHERN = "southern"
    HAWAIIAN = "hawaiian"
    JAMAICAN = "jamaican"
    MEXICAN = "mexican"
    VENEZUELAN = "venezuelan"
    COLOMBIAN = "colombian"
    PERUVIAN = "peruvian"
    BRAZILIAN = "brazilian"
    ARGENTINIAN = "argentinian"
    LATIN = "latin"
    NORTHAMERICAN = "north american"
    SOUTHAMERICAN = "south american"
    EUROPEAN = "european"
    AFRICAN = "african"
    ASIAN = "asian"
    OCEANIC = "oceanic"
    NONE = ""


@dataclass
class recipe:
    """Class representing meal recipe"""
    
    recipe_id: UUID
    recipe_name: str
    recipe_style: Style 
    recipe_cuisine: Cuisine
    recipe_description: str
    recipe_instructions: dict[int, str]
    recipe_ingredients: dict[Item, Quantity]
    
    # Ideas: add/remove instructions, add/remove ingredients, update recipe name, style, etc., 
    
    
    