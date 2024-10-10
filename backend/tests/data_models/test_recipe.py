import datetime
import pytest
import sys
import uuid

from backend.src.data_models import quantity as sc_quantity
from backend.src.utils import types as sc_types
from backend.src.data_models.recipe import Recipe
from backend.src.data_models.item import Item


@pytest.mark.parametrize(
    "quantity, unit, type",
    [
        (5.43, sc_types.Unit.KILOS, sc_types.UnitType.WEIGHT),
        (23.4, sc_types.Unit.KCAL, sc_types.UnitType.ENERGY),
        (7, sc_types.Unit.LITER, sc_types.UnitType.VOLUME),
    ],
)
def test_recipe_init(
    quantity,
    unit,
    type,
):
    test_quantity = sc_quantity.Quantity(
        quantity,
        unit,
        type,
    )

    if unit == sc_types.Unit.KILOS:
        assert test_quantity.type == sc_types.UnitType.WEIGHT
    elif unit == sc_types.Unit.KCAL:
        assert test_quantity.type == sc_types.UnitType.ENERGY
    elif unit == sc_types.Unit.LITER:
        assert test_quantity.type == sc_types.UnitType.VOLUME


def test_recipe_macro_aggregation():
    # Create ingredients with macros
    ingredient1 = Item(
        name="Chicken Breast",
        item_id=uuid.uuid4(),
        quantity=sc_quantity.Quantity(1.60, sc_types.Unit.POUNDS, sc_types.UnitType.WEIGHT),
        price=11.80,
        merchant="Trader Joes",
        per_serving_macros={
            sc_types.Macro.PROTEIN: sc_quantity.Quantity(31, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT),
            sc_types.Macro.CARB: sc_quantity.Quantity(0, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT),
            sc_types.Macro.FAT: sc_quantity.Quantity(3.6, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT),
            sc_types.Macro.SUGAR: sc_quantity.Quantity(0, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT),
            sc_types.Macro.FIBER: sc_quantity.Quantity(0, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT),
            sc_types.Macro.CALORIES: sc_quantity.Quantity(120, sc_types.Unit.KCAL, sc_types.UnitType.ENERGY),
        },
        serving_size=sc_quantity.Quantity(4, sc_types.Unit.OUNCES, sc_types.UnitType.WEIGHT),
        expiration_date=None,
        shelf_life=datetime.timedelta(days=7),
        storage=sc_types.StorageType.FRIDGE,
    )
    ingredient2 = Item(
        name="Brown Rice",
        item_id=uuid.uuid4(),
        price=3.99,
        quantity=sc_quantity.Quantity(3, sc_types.Unit.POUNDS, sc_types.UnitType.WEIGHT),
        merchant="Trader Joes",
        per_serving_macros={
            sc_types.Macro.PROTEIN: sc_quantity.Quantity(2.6, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT),
            sc_types.Macro.CARB: sc_quantity.Quantity(23, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT),
            sc_types.Macro.FAT: sc_quantity.Quantity(0.9, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT),
            sc_types.Macro.SUGAR: sc_quantity.Quantity(0.1, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT),
            sc_types.Macro.FIBER: sc_quantity.Quantity(2.1, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT),
            sc_types.Macro.CALORIES: sc_quantity.Quantity(120, sc_types.Unit.KCAL, sc_types.UnitType.ENERGY),
        },
        serving_size=sc_quantity.Quantity(195, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT),
        expiration_date=None,
        shelf_life=datetime.timedelta(days=365),
        storage=sc_types.StorageType.PANTRY,
    )

    # Create a recipe with these ingredients
    recipe = Recipe(
        recipe_id=uuid.uuid4(),
        recipe_name="Chicken and Rice",
        recipe_description="A simple recipe to cook chicken and rice.",
        recipe_instructions={
            1: "Cook the chicken in a pan.",
            2: "Cook the rice in a pot.",
            3: "Mix the chicken and rice together.",
            4: "Serve.",
        },
        recipe_ingredients={
            ingredient1: sc_quantity.Quantity(4, sc_types.Unit.OUNCES, sc_types.UnitType.WEIGHT),
            ingredient2: sc_quantity.Quantity(195, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT),
        },
    )

    # Check if the recipe correctly aggregates macros
    assert recipe.is_feasible
    assert recipe.nutritional_facts[sc_types.Macro.PROTEIN].quantity == pytest.approx(33.6)
    assert recipe.nutritional_facts[sc_types.Macro.CARB].quantity == pytest.approx(23.0)
    assert recipe.nutritional_facts[sc_types.Macro.FAT].quantity == pytest.approx(4.5)


if __name__ == "__main__":
    sys.exit(pytest.main())
