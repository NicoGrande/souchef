import uuid
import logging
import pydantic

import src.data_models.item as sc_item
import src.data_models.quantity as sc_quantity
import src.data_models.nutritional_facts as sc_nutritional_facts
import src.utils.types as sc_types


class RecipeIngredient(pydantic.BaseModel):
    """
    Class representing an ingredient in a recipe with its quantity.
    """

    name: str
    quantity: float
    unit: str


class Recipe(pydantic.BaseModel):
    """
    Class representing a meal recipe.

    Attributes:
        name (str): Name of the recipe.
        description (str): Description of the recipe.
        instructions (dict[int, str]): Step-by-step instructions for the recipe.
        ingredients (list[RecipeIngredient]): Ingredients and their quantities.
    """

    name: str
    description: str
    instructions: dict[int, str]
    ingredients: list[RecipeIngredient]
    nutritional_facts: sc_nutritional_facts.NutritionalFacts = pydantic.Field(
        default_factory=sc_nutritional_facts.NutritionalFacts
    )
    _recipe_id: uuid.UUID = pydantic.PrivateAttr(default_factory=uuid.uuid4)

    @pydantic.field_validator("ingredients")
    def validate_ingredients(cls, value):
        """
        Validate the ingredients of the recipe.
        """
        if not isinstance(value, list) or not value:
            raise ValueError("Ingredients cannot be empty and must be a list")
        return value

    @pydantic.field_validator("instructions")
    def validate_instructions(cls, value):
        """
        Validate the instructions of the recipe.
        """
        if not isinstance(value, dict) or not value:
            raise ValueError("Instructions cannot be empty and must be a dictionary")
        return value

    def check_feasibility(self, existing_items: list[sc_item.Item]) -> bool:
        """
        Check if the recipe is feasible based on available ingredient quantities.

        Args:
            existing_items (list[sc_item.Item]): List of available items to check against

        Returns:
            bool: True if the recipe is feasible, False otherwise
        """
        item_lookup = {item.name: item for item in existing_items}

        for recipe_ingredient in self.ingredients:
            if recipe_ingredient.name not in item_lookup:
                logging.warning(f"Missing ingredient: {recipe_ingredient.name}")
                return False

            item = item_lookup[recipe_ingredient.name]
            # Create a Quantity object from the RecipeIngredient
            recipe_quantity = sc_quantity.Quantity(
                quantity=recipe_ingredient.quantity,
                unit=sc_types.Unit(recipe_ingredient.unit),
                type=item.quantity.type,
            )
            required_quantity_converted = sc_quantity.convert_unit(
                recipe_quantity, item.quantity.unit
            )
            if item.quantity.quantity < required_quantity_converted:
                logging.warning(f"Not enough {item.name} for recipe {self.name}")
                return False

        return True

    def update_nutritional_facts(self, existing_items: list[sc_item.Item]) -> None:
        """
        Calculate and update the nutritional facts for the recipe based on its ingredients.
        """
        facts = sc_nutritional_facts.NutritionalFacts()

        # Create a lookup dictionary for items by name
        item_lookup = {item.name: item for item in existing_items}

        for recipe_ingredient in self.ingredients:
            if recipe_ingredient.name in item_lookup:
                item = item_lookup[recipe_ingredient.name]
                # Calculate the ratio of recipe quantity to serving size
                recipe_quantity = sc_quantity.Quantity(
                    quantity=recipe_ingredient.quantity,
                    unit=sc_types.Unit(recipe_ingredient.unit),
                    type=item.nutritional_facts.serving_size.type,
                )
                converted_recipe_quantity = sc_quantity.convert_unit(
                    recipe_quantity, item.nutritional_facts.serving_size.unit
                )
                ratio = (
                    converted_recipe_quantity
                    / item.nutritional_facts.serving_size.quantity
                )

                # Scale the macros by the ratio
                facts.calories.quantity += (
                    item.nutritional_facts.calories.quantity * ratio
                )
                facts.protein.quantity += (
                    item.nutritional_facts.protein.quantity * ratio
                )
                facts.fat.quantity += item.nutritional_facts.fat.quantity * ratio
                facts.carbs.quantity += item.nutritional_facts.carbs.quantity * ratio
                facts.fiber.quantity += item.nutritional_facts.fiber.quantity * ratio
                facts.sugar.quantity += item.nutritional_facts.sugar.quantity * ratio

        self.nutritional_facts = facts
