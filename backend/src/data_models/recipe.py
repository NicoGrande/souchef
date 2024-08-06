from dataclasses import dataclass
import uuid
import logging

import backend.src.data_models.item as sc_item
import backend.src.data_models.quantity as sc_quantity
import backend.src.utils.math as sc_math
import backend.src.utils.types as sc_types


@dataclass
class recipe:
    """Class representing meal recipe"""

    recipe_sid: uuid.UUID
    recipe_name: str
    recipe_description: str
    recipe_instructions: dict[int, str]
    recipe_ingredients: dict[sc_item.Item, sc_quantity.Quantity]

    def __post_init__(self):
        self._compute_recipe_macros()

    def _is_recipe_feasible(self) -> bool:
        is_feasible = True
        for item, required_quantity in self.recipe_ingredients.items():
            required_quantity_converted = sc_math.convert_unit(
                required_quantity, item.quantity.unit
            )
            if item.quantity.quantity > required_quantity_converted:
                logging.warning(f"Not enough {item.name} for recipe {self.recipe_name}")
                is_feasible = False
        return is_feasible

    def _compute_recipe_macros(self):
        self._nutritional_facts = sc_quantity.macrosDefaultDict()
        for item, required_quantity in self.recipe_ingredients.items():
            for macro, serving_quantity in item.per_serving_macros.items():
                macro_multiplier = required_quantity / item.serving_size
                self._nutritional_facts[macro] += serving_quantity * macro_multiplier

    @property
    def is_feasible(self) -> bool:
        return self._is_recipe_feasible()

    @property
    def nutritional_facts(self) -> dict[sc_types.Macro, sc_quantity.Quantity]:
        return self._nutritional_facts
