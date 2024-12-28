import datetime
import pytest
import sys
import uuid
import pydantic

from src.data_models import quantity as sc_quantity
from src.utils import types as sc_types
from src.data_models.recipe import Recipe, RecipeIngredient
from src.data_models.item import Item
from src.data_models.nutritional_facts import NutritionalFacts


def test_recipe_macro_aggregation():
    # Create ingredients with macros
    ingredient1 = Item(
        name="Chicken Breast",
        quantity=sc_quantity.Quantity(
            quantity=1.60, unit=sc_types.Unit.POUNDS, type=sc_types.UnitType.WEIGHT
        ),
        shelf_life=datetime.timedelta(days=7),
        storage=sc_types.StorageType.FRIDGE,
    )

    # Update chicken breast nutritional facts (per 195g serving)
    ingredient1.nutritional_facts = NutritionalFacts(
        serving_size=sc_quantity.Quantity(
            quantity=113.4,  # 4 oz in grams
            unit=sc_types.Unit.GRAMS,
            type=sc_types.UnitType.WEIGHT,
        ),
        calories=sc_quantity.Quantity(
            quantity=165, unit=sc_types.Unit.KCAL, type=sc_types.UnitType.ENERGY
        ),
        protein=sc_quantity.Quantity(
            quantity=31, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        ),
        fat=sc_quantity.Quantity(
            quantity=3.6, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        ),
        carbs=sc_quantity.Quantity(
            quantity=0, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        ),
        sugar=sc_quantity.Quantity(
            quantity=0, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        ),
        fiber=sc_quantity.Quantity(
            quantity=0, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        ),
    )

    ingredient2 = Item(
        name="Brown Rice",
        quantity=sc_quantity.Quantity(
            quantity=3, unit=sc_types.Unit.POUNDS, type=sc_types.UnitType.WEIGHT
        ),
        shelf_life=datetime.timedelta(days=365),
        storage=sc_types.StorageType.PANTRY,
    )
    # Brown rice nutritional facts (per 195g serving)
    ingredient2.nutritional_facts = NutritionalFacts(
        serving_size=sc_quantity.Quantity(
            quantity=195, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        ),
        calories=sc_quantity.Quantity(
            quantity=216, unit=sc_types.Unit.KCAL, type=sc_types.UnitType.ENERGY
        ),
        protein=sc_quantity.Quantity(
            quantity=5, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        ),
        fat=sc_quantity.Quantity(
            quantity=1.8, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        ),
        carbs=sc_quantity.Quantity(
            quantity=45, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        ),
        sugar=sc_quantity.Quantity(
            quantity=0.7, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        ),
        fiber=sc_quantity.Quantity(
            quantity=3.5, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        ),
    )

    # Create a recipe with these ingredients
    recipe = Recipe(
        name="Chicken and Rice",
        description="A simple recipe to cook chicken and rice.",
        instructions={
            1: "Cook the chicken in a pan.",
            2: "Cook the rice in a pot.",
            3: "Mix the chicken and rice together.",
            4: "Serve.",
        },
        ingredients=[
            RecipeIngredient(
                name="Chicken Breast", quantity=4, unit=sc_types.Unit.OUNCES.value
            ),
            RecipeIngredient(
                name="Brown Rice", quantity=195, unit=sc_types.Unit.GRAMS.value
            ),
        ],
    )

    # Check if the recipe is feasible and calculate nutritional facts
    assert recipe.check_feasibility(existing_items=[ingredient1, ingredient2])
    recipe.update_nutritional_facts(existing_items=[ingredient1, ingredient2])

    # Now check the nutritional facts
    assert recipe.nutritional_facts.protein.quantity == pytest.approx(36.0, 0.1)
    assert recipe.nutritional_facts.carbs.quantity == pytest.approx(45.0, 0.1)
    assert recipe.nutritional_facts.fat.quantity == pytest.approx(5.4, 0.1)

    # Additional nutritional fact checks
    assert recipe.nutritional_facts.calories.quantity == pytest.approx(381.0, 0.1)
    assert recipe.nutritional_facts.fiber.quantity == pytest.approx(3.5, 0.1)


def test_recipe_validation():
    with pytest.raises(pydantic.ValidationError):
        Recipe(
            name=1234,  # Invalid recipe name
            description="This recipe should fail validation",
            instructions={1: "Step 1"},
            ingredients=[],  # Empty list should trigger validation error
        )

    with pytest.raises(pydantic.ValidationError):
        Recipe(
            name="Chicken and Rice",
            description="This recipe should fail validation",
            instructions={1: "Step 1"},
            ingredients=[],
        )

    with pytest.raises(pydantic.ValidationError):
        Recipe(
            name="Chicken and Rice",
            description="This recipe should fail validation",
            instructions={},
            ingredients=[],
        )


def test_recipe_not_feasible():
    """Test that a recipe is correctly identified as not feasible when there aren't enough ingredients."""
    # Create an ingredient with insufficient quantity
    ingredient1 = Item(
        name="Chicken Breast",
        quantity=sc_quantity.Quantity(
            quantity=0.1,  # Only 0.1 pounds of chicken (not enough for 4 oz)
            unit=sc_types.Unit.POUNDS,
            type=sc_types.UnitType.WEIGHT,
        ),
        shelf_life=datetime.timedelta(days=7),
        storage=sc_types.StorageType.FRIDGE,
    )

    ingredient2 = Item(
        name="Brown Rice",
        quantity=sc_quantity.Quantity(
            quantity=50,  # Only 50g of rice (not enough for 195g)
            unit=sc_types.Unit.GRAMS,
            type=sc_types.UnitType.WEIGHT,
        ),
        shelf_life=datetime.timedelta(days=365),
        storage=sc_types.StorageType.PANTRY,
    )

    # Create a recipe that requires more ingredients than we have
    recipe = Recipe(
        name="Chicken and Rice",
        description="A simple recipe that we can't make.",
        instructions={
            1: "Cook the chicken in a pan.",
            2: "Cook the rice in a pot.",
            3: "Mix the chicken and rice together.",
            4: "Serve.",
        },
        ingredients=[
            RecipeIngredient(
                name="Chicken Breast",
                quantity=4,
                unit=sc_types.Unit.OUNCES.value,  # Need 4 oz (0.25 pounds)
            ),
            RecipeIngredient(
                name="Brown Rice",
                quantity=195,
                unit=sc_types.Unit.GRAMS.value,  # Need 195g
            ),
        ],
    )

    # Check that the recipe is not feasible
    assert not recipe.check_feasibility(existing_items=[ingredient1, ingredient2])

    # Also test with missing ingredients
    assert not recipe.check_feasibility(existing_items=[ingredient1])  # Missing rice
    assert not recipe.check_feasibility(existing_items=[])  # No ingredients


if __name__ == "__main__":
    sys.exit(pytest.main())
