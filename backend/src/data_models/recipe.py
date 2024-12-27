import uuid
import logging
import pydantic

import src.data_models.item as sc_item
import src.data_models.quantity as sc_quantity
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
        ingredients (dict[str, RecipeIngredient]): Ingredients and their quantities.
    """

    name: str
    description: str
    instructions: dict[int, str]
    ingredients: dict[str, RecipeIngredient]
    nutritional_facts: dict[sc_types.Macro, sc_quantity.Quantity] = pydantic.Field(
        default_factory=sc_quantity.macrosDefaultDict
    )
    _recipe_id: uuid.UUID = pydantic.PrivateAttr(default_factory=uuid.uuid4)

    @pydantic.field_validator("nutritional_facts", mode="before")
    def validate_nutritional_facts(cls, value):
        """
        Validate the nutritional facts.
        """
        if isinstance(value, dict):
            if value == {}:
                return sc_quantity.macrosDefaultDict()

            validated_macros = {}
            for key, quantity in value.items():
                if isinstance(key, str):
                    try:
                        macro_key = sc_types.MACRO_MAPPINGS[key.lower()]
                    except KeyError:
                        raise ValueError(f"Invalid macro type: {key}")
                    else:
                        validated_macros[macro_key] = (
                            sc_quantity.Quantity.model_validate(quantity)
                        )

                elif isinstance(key, sc_types.Macro) and isinstance(quantity, dict):
                    validated_macros[key] = sc_quantity.Quantity.model_validate(
                        quantity
                    )

                elif isinstance(key, sc_types.Macro) and isinstance(
                    quantity, sc_quantity.Quantity
                ):
                    validated_macros[key] = quantity

                else:
                    raise ValueError(f"Invalid macro type: {key}")
            return validated_macros
        return value

    def _is_recipe_feasible(self, existing_items: list[sc_item.Item]) -> bool:
        """
        Check if the recipe is feasible based on available ingredient quantities.

        Returns:
            bool: True if the recipe is feasible, False otherwise.
        """
        is_feasible = True
        for item in existing_items:
            if item.name in self.ingredients:
                recipe_ingredient = self.ingredients[item.name]
                # Create a Quantity object from the RecipeIngredient
                required_quantity = sc_quantity.Quantity(
                    quantity=recipe_ingredient.quantity,
                    unit=sc_types.Unit(recipe_ingredient.unit),
                    type=item.quantity.type,  # Use the same type as the item's quantity
                )
                required_quantity_converted = sc_quantity.convert_unit(
                    required_quantity, item.quantity.unit
                )
                if item.quantity.quantity < required_quantity_converted:
                    logging.warning(f"Not enough {item.name} for recipe {self.name}")
                    is_feasible = False
        return is_feasible

    @property
    def is_feasible(self) -> bool:
        """
        Check if the recipe is feasible based on available ingredient quantities.

        Returns:
            bool: True if the recipe is feasible, False otherwise.
        """
        return self._is_recipe_feasible()

    def calculate_nutritional_facts(self, items: list[sc_item.Item]) -> None:
        """
        Calculate and update the nutritional facts for the recipe based on its ingredients.
        """
        facts = sc_quantity.macrosDefaultDict()

        for item in items:
            if item.name in self.ingredients:
                recipe_ingredient = self.ingredients[item.name]
                # Calculate the ratio of recipe quantity to serving size
                recipe_quantity = sc_quantity.Quantity(
                    quantity=recipe_ingredient.quantity,
                    unit=sc_types.Unit(recipe_ingredient.unit),
                    type=item.serving_size.type,
                )
                converted_recipe_quantity = sc_quantity.convert_unit(
                    recipe_quantity, item.serving_size.unit
                )
                ratio = converted_recipe_quantity / item.serving_size.quantity

                # Scale the macros by the ratio
                for macro, quantity in item.per_serving_macros.items():
                    facts[macro].quantity += quantity.quantity * ratio

        self.nutritional_facts = facts
