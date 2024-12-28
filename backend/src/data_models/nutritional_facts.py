import pydantic

from src.data_models import quantity as sc_quantity
from src.utils import types as sc_types


class NutritionalFacts(pydantic.BaseModel):
    """
    Data class representing nutritional facts for a food item.

    Attributes:
        serving_size: The size of the serving of the item.
        calories: The calories per serving of the item.
        protein: The protein per serving of the item.
        fat: The fat per serving of the item.
        carbs: The carbs per serving of the item.
        fiber: The fiber per serving of the item.
        sugar: The sugar per serving of the item.
    """

    serving_size: sc_quantity.Quantity = pydantic.Field(
        default_factory=lambda: sc_quantity.Quantity(
            quantity=1, unit=sc_types.Unit.NONE, type=sc_types.UnitType.NONE
        )
    )
    calories: sc_quantity.Quantity = pydantic.Field(
        default_factory=lambda: sc_quantity.Quantity(
            quantity=0, unit=sc_types.Unit.KCAL, type=sc_types.UnitType.ENERGY
        )
    )
    protein: sc_quantity.Quantity = pydantic.Field(
        default_factory=lambda: sc_quantity.Quantity(
            quantity=0, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        )
    )
    fat: sc_quantity.Quantity = pydantic.Field(
        default_factory=lambda: sc_quantity.Quantity(
            quantity=0, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        )
    )
    carbs: sc_quantity.Quantity = pydantic.Field(
        default_factory=lambda: sc_quantity.Quantity(
            quantity=0, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        )
    )
    fiber: sc_quantity.Quantity = pydantic.Field(
        default_factory=lambda: sc_quantity.Quantity(
            quantity=0, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        )
    )
    sugar: sc_quantity.Quantity = pydantic.Field(
        default_factory=lambda: sc_quantity.Quantity(
            quantity=0, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        )
    )
