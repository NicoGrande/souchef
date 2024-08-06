import pytest
import sys

from backend.src.data_models import quantity as sc_quantity
from backend.src.utils import types as sc_types


@pytest.mark.parametrize(
    "quantity, unit, type",
    [
        (5.43, sc_types.Unit.KILOS, sc_types.UnitType.WEIGHT),
        (23.4, sc_types.Unit.KCAL, sc_types.UnitType.ENERGY),
        (7, sc_types.Unit.LITER, sc_types.UnitType.VOLUME),
    ],
)
def test_quantity_init(
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


@pytest.mark.parametrize(
    "quantity_a, quantity_b",
    [
        (5.43, sc_types.Unit.KILOS, sc_types.UnitType.WEIGHT),
        (23.4, sc_types.Unit.KCAL, sc_types.UnitType.ENERGY),
        (7, sc_types.Unit.LITER, sc_types.UnitType.VOLUME),
    ],
)
def test_quantity_sum(quantity_a, quantity_b):
    pass


if __name__ == "__main__":
    sys.exit(pytest.main())
