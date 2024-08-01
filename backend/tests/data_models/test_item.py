import datetime
import pytest
import uuid
import sys

from backend.src.data_models import item as sc_item
from backend.src.data_models import quantity as sc_quantity
from backend.src.utils import types as sc_types


TEST_UUID_1 = uuid.uuid4()
TEST_UUID_2 = uuid.uuid4()
TEST_UUID_3 = uuid.uuid4()


@pytest.mark.parametrize(
    "name, item_id, quantity, price, merchant, per_unit_macros, expiration_date, storage",
    [
        (
            "banana",
            TEST_UUID_1,
            sc_quantity.Quantity(
                3,
                sc_types.Unit.NONE,
                sc_types.UnitType.NONE,
            ),
            1.50,
            "Whole Foods",
            {
                sc_types.Macro.CARB: sc_quantity.Quantity(
                    31, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.PROTEIN: sc_quantity.Quantity(
                    1.48, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.FAT: sc_quantity.Quantity(
                    0.449, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.SUGAR: sc_quantity.Quantity(
                    16.6, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.CALORIES: sc_quantity.Quantity(
                    102, sc_types.Unit.KCAL, sc_types.UnitType.ENERGY
                ),
                sc_types.Macro.FIBER: sc_quantity.Quantity(
                    3.54, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT
                ),
            },
            datetime.datetime.now().date() + datetime.timedelta(days=5),
            sc_types.StorageType.PANTRY,
        )
    ],
)
def test_item_init(
    name, item_id, quantity, price, merchant, per_unit_macros, expiration_date, storage
):
    test_item = sc_item.Item(
        name,
        item_id,
        quantity,
        price,
        merchant,
        per_unit_macros,
        expiration_date,
        storage,
    )

    assert print(test_item) == name
    assert test_item.get_shelf_life_remaining() == datetime.timedelta(days=5)


if __name__ == "__main__":
    sys.exit(pytest.main())
