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
        self.nutritional_facts = {
            sc_types.Macros.CARBS: sc_quantity.Quantity(0, sc_types.Units.GRAMS),
            sc_types.Macros.FAT: sc_quantity.Quantity(0, sc_types.Units.GRAMS),
            sc_types.Macros.PROTEIN: sc_quantity.Quantity(0, sc_types.Units.GRAMS),
        }
        for item, required_quantity in self.recipe_ingredients.items():
            for macro, macro_quantity in item.macros.items():
                required_quantity_grams = sc_math.convert_unit(
                    required_quantity, sc_types.Units.GRAMS
                )
                macro_multiplier = item.quantity / required_quantity_grams
                self.nutritional_facts[macro] += macro_quantity * macro_multiplier
