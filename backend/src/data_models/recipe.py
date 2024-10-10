from dataclasses import dataclass
import uuid
import logging

import backend.src.data_models.item as sc_item
import backend.src.data_models.quantity as sc_quantity
import backend.src.utils.types as sc_types


@dataclass
class Recipe:
    """Class representing meal recipe"""

    recipe_id: uuid.UUID
    recipe_name: str
    recipe_description: str
    recipe_instructions: dict[int, str]
    recipe_ingredients: dict[sc_item.Item, sc_quantity.Quantity]

    def __post_init__(self):
        self._compute_recipe_macros()

    def _is_recipe_feasible(self) -> bool:
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
        self._nutritional_facts = sc_quantity.macrosDefaultDict()
        for macro in sc_types.Macro:
            total = 0
            for ingredient, quantity in self.recipe_ingredients.items():
                serving_size = ingredient.serving_size
                recipe_quantity = sc_quantity.convert_unit(quantity, serving_size.unit)
                servings = recipe_quantity / serving_size.quantity
                total += ingredient.per_serving_macros[macro].quantity * servings
            
            if macro == sc_types.Macro.CALORIES:
                self._nutritional_facts[macro] = sc_quantity.Quantity(total, sc_types.Unit.KCAL, sc_types.UnitType.ENERGY)
            else:
                self._nutritional_facts[macro] = sc_quantity.Quantity(total, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT)

    @property
    def is_feasible(self) -> bool:
        return self._is_recipe_feasible()

    @property
    def nutritional_facts(self) -> dict[sc_types.Macro, sc_quantity.Quantity]:
        return self._nutritional_facts
