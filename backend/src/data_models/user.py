import pydantic


class UserPreferences(pydantic.BaseModel):
    """
    Data class representing a user's preferences.
    """

    dietary_restrictions: list[str]
    favorite_cuisines: list[str]
    favorite_recipes: list[str]
    kitchen_appliances: list[str]
    number_of_people: int
