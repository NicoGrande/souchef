import uuid
import logging
import pydantic
import typing

import backend.src.data_models.item as sc_item
import backend.src.data_models.quantity as sc_quantity
import backend.src.utils.types as sc_types


class Recipe(pydantic.BaseModel):
    """
    Class representing a meal recipe.

    Attributes:
        recipe_id (uuid.UUID): Unique identifier for the recipe.
        recipe_name (str): Name of the recipe.
        recipe_description (str): Description of the recipe.
        recipe_instructions (dict[int, str]): Step-by-step instructions for the recipe.
        recipe_ingredients (dict[sc_item.Item, sc_quantity.Quantity]): Ingredients and their quantities.
    """

    recipe_id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)
    recipe_name: str
    recipe_description: str
    recipe_instructions: dict[int, str]
    recipe_ingredients: dict[sc_item.Item, sc_quantity.Quantity]

    def model_post_init(self, __context: typing.Any):
        """
        Post-initialization method to compute recipe macros.

        Args:
            __context (typing.Any): Context information (not used).
        """
        self._compute_recipe_macros()

    def _is_recipe_feasible(self) -> bool:
        """
        Check if the recipe is feasible based on available ingredient quantities.

        Returns:
            bool: True if the recipe is feasible, False otherwise.
        """
        is_feasible = True
        for item, required_quantity in self.recipe_ingredients.items():
            required_quantity_converted = sc_quantity.convert_unit(
                required_quantity, item.quantity.unit
            )
            if item.quantity.quantity < required_quantity_converted:
                logging.warning(f"Not enough {item.name} for recipe {self.recipe_name}")
                is_feasible = False
        return is_feasible

    def _compute_recipe_macros(self):
        """
        Compute the nutritional facts (macros) for the recipe.
        """
        self._nutritional_facts = sc_quantity.macrosDefaultDict()
        for macro in sc_types.Macro:
            total = 0
            for ingredient, quantity in self.recipe_ingredients.items():
                serving_size = ingredient.serving_size
                recipe_quantity = sc_quantity.convert_unit(quantity, serving_size.unit)
                servings = recipe_quantity / serving_size.quantity
                total += ingredient.per_serving_macros[macro].quantity * servings

            if macro == sc_types.Macro.CALORIES:
                self._nutritional_facts[macro] = sc_quantity.Quantity(
                    quantity=total,
                    unit=sc_types.Unit.KCAL,
                    type=sc_types.UnitType.ENERGY,
                )
            else:
                self._nutritional_facts[macro] = sc_quantity.Quantity(
                    quantity=total,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                )

    @property
    def is_feasible(self) -> bool:
        """
        Check if the recipe is feasible based on available ingredient quantities.

        Returns:
            bool: True if the recipe is feasible, False otherwise.
        """
        return self._is_recipe_feasible()

    @property
    def nutritional_facts(self) -> dict[sc_types.Macro, sc_quantity.Quantity]:
        """
        Get the nutritional facts (macros) for the recipe.

        Returns:
            dict[sc_types.Macro, sc_quantity.Quantity]: A dictionary of macros and their quantities.
        """
        return self._nutritional_facts
