import pytest
import sys

from src.data_models import quantity as sc_quantity
from src.utils import types as sc_types


@pytest.mark.parametrize(
    "quantity, unit, type",
    [
        (5.43, sc_types.Unit.KILOS, sc_types.UnitType.WEIGHT),
        (23.4, sc_types.Unit.KCAL, sc_types.UnitType.ENERGY),
        (7, sc_types.Unit.LITER, sc_types.UnitType.VOLUME),
    ],
)
def test_quantity_init(quantity, unit, type):
    test_quantity = sc_quantity.Quantity(
        quantity=quantity,
        unit=unit,
        type=type,
    )

    assert test_quantity.quantity == quantity
    assert test_quantity.unit == unit
    assert test_quantity.type == type


@pytest.mark.parametrize(
    "quantity_a, quantity_b, expected_quantity",
    [
        (
            sc_quantity.Quantity(
                quantity=5.43, unit=sc_types.Unit.KILOS, type=sc_types.UnitType.WEIGHT
            ),
            sc_quantity.Quantity(
                quantity=1000, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
            ),
            6.43,
        ),
        (
            sc_quantity.Quantity(
                quantity=1, unit=sc_types.Unit.KILOS, type=sc_types.UnitType.WEIGHT
            ),
            sc_quantity.Quantity(
                quantity=500, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
            ),
            1.5,
        ),
    ],
)
def test_quantity_sum(quantity_a, quantity_b, expected_quantity):
    result = quantity_a + quantity_b
    assert result.quantity == pytest.approx(expected_quantity)
    assert result.unit == quantity_a.unit
    assert result.type == quantity_a.type


def test_quantity_sum_different_types():
    quantity_a = sc_quantity.Quantity(
        quantity=23.4, unit=sc_types.Unit.KCAL, type=sc_types.UnitType.ENERGY
    )
    quantity_b = sc_quantity.Quantity(
        quantity=7, unit=sc_types.Unit.LITER, type=sc_types.UnitType.VOLUME
    )

    with pytest.raises(TypeError, match="Quantities must have the same Unit Type"):
        quantity_a + quantity_b


@pytest.mark.parametrize(
    "input_quantity, output_unit, expected_value",
    [
        (
            sc_quantity.Quantity(
                quantity=1, unit=sc_types.Unit.KILOS, type=sc_types.UnitType.WEIGHT
            ),
            sc_types.Unit.GRAMS,
            1000.0,
        ),
        (
            sc_quantity.Quantity(
                quantity=1000, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
            ),
            sc_types.Unit.KILOS,
            1.0,
        ),
        (
            sc_quantity.Quantity(
                quantity=1, unit=sc_types.Unit.POUNDS, type=sc_types.UnitType.WEIGHT
            ),
            sc_types.Unit.OUNCES,
            16.0,
        ),
    ],
)
def test_convert_unit(input_quantity, output_unit, expected_value):
    result = sc_quantity.convert_unit(input_quantity, output_unit)
    assert result == pytest.approx(expected_value)


def test_macros_default_dict():
    macros = sc_quantity.macrosDefaultDict()
    assert len(macros) == 6  # Check all macros are present

    # Check each macro has correct initial values and types
    for macro_quantity in macros.values():
        assert isinstance(macro_quantity, sc_quantity.Quantity)
        assert macro_quantity.quantity == 0


if __name__ == "__main__":
    sys.exit(pytest.main())
