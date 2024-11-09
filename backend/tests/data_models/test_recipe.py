import datetime
import pytest
import sys
import uuid
import pydantic

from src.data_models import quantity as sc_quantity
from src.utils import types as sc_types
from src.data_models.recipe import Recipe
from src.data_models.item import Item


def test_recipe_macro_aggregation():
    # Create ingredients with macros
    ingredient1 = Item(
        name="Chicken Breast",
        item_id=uuid.uuid4(),
        quantity=sc_quantity.Quantity(
            quantity=1.60, unit=sc_types.Unit.POUNDS, type=sc_types.UnitType.WEIGHT
        ),
        price=11.80,
        merchant="Trader Joes",
        per_serving_macros={
            sc_types.Macro.PROTEIN: sc_quantity.Quantity(
                quantity=31, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
            ),
            sc_types.Macro.CARB: sc_quantity.Quantity(
                quantity=0, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
            ),
            sc_types.Macro.FAT: sc_quantity.Quantity(
                quantity=3.6, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
            ),
            sc_types.Macro.CALORIES: sc_quantity.Quantity(
                quantity=140, unit=sc_types.Unit.KCAL, type=sc_types.UnitType.ENERGY
            ),
            sc_types.Macro.SUGAR: sc_quantity.Quantity(
                quantity=0, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
            ),
            sc_types.Macro.FIBER: sc_quantity.Quantity(
                quantity=0, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
            ),
        },
        serving_size=sc_quantity.Quantity(
            quantity=4, unit=sc_types.Unit.OUNCES, type=sc_types.UnitType.WEIGHT
        ),
        expiration_date=None,
        shelf_life=datetime.timedelta(days=7),
        storage=sc_types.StorageType.FRIDGE,
    )
    ingredient2 = Item(
        name="Brown Rice",
        item_id=uuid.uuid4(),
        price=3.99,
        quantity=sc_quantity.Quantity(
            quantity=3, unit=sc_types.Unit.POUNDS, type=sc_types.UnitType.WEIGHT
        ),
        merchant="Trader Joes",
        per_serving_macros={
            sc_types.Macro.PROTEIN: sc_quantity.Quantity(
                quantity=2.6, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
            ),
            sc_types.Macro.CARB: sc_quantity.Quantity(
                quantity=23, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
            ),
            sc_types.Macro.FAT: sc_quantity.Quantity(
                quantity=0.9, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
            ),
            sc_types.Macro.CALORIES: sc_quantity.Quantity(
                quantity=120, unit=sc_types.Unit.KCAL, type=sc_types.UnitType.ENERGY
            ),
            sc_types.Macro.SUGAR: sc_quantity.Quantity(
                quantity=0.9, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
            ),
            sc_types.Macro.FIBER: sc_quantity.Quantity(
                quantity=2.1, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
            ),
        },
        serving_size=sc_quantity.Quantity(
            quantity=195, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        ),
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
            ingredient1: sc_quantity.Quantity(
                quantity=4, unit=sc_types.Unit.OUNCES, type=sc_types.UnitType.WEIGHT
            ),
            ingredient2: sc_quantity.Quantity(
                quantity=195, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
            ),
        },
    )

    # Check if the recipe correctly aggregates macros
    assert recipe.is_feasible
    assert recipe.nutritional_facts[sc_types.Macro.PROTEIN].quantity == pytest.approx(
        33.6
    )
    assert recipe.nutritional_facts[sc_types.Macro.CARB].quantity == pytest.approx(23.0)
    assert recipe.nutritional_facts[sc_types.Macro.FAT].quantity == pytest.approx(4.5)


def test_recipe_validation():
    with pytest.raises(pydantic.ValidationError):
        Recipe(
            recipe_name=1234,  # Invalid recipe name
            recipe_description="This recipe should fail validation",
            recipe_instructions={1: "Step 1"},
            recipe_ingredients={},
        )


if __name__ == "__main__":
    sys.exit(pytest.main())
