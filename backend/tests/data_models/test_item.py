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
    "name, item_id, quantity, price, merchant, per_serving_macros, serving_size, expiration_date, shelf_life, storage",
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
            sc_quantity.Quantity(
                1,
                sc_types.Unit.NONE,
                sc_types.UnitType.NONE,
            ),
            None,
            datetime.timedelta(days=5),
            sc_types.StorageType.PANTRY,
        ),
        (
            "Four Cheese Ravioli",
            TEST_UUID_2,
            sc_quantity.Quantity(
                283,
                sc_types.Unit.GRAMS,
                sc_types.UnitType.WEIGHT,
            ),
            2.99,
            "Trader Joes",
            {
                sc_types.Macro.CARB: sc_quantity.Quantity(
                    31, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.PROTEIN: sc_quantity.Quantity(
                    9, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.FAT: sc_quantity.Quantity(
                    10, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.SUGAR: sc_quantity.Quantity(
                    5, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.CALORIES: sc_quantity.Quantity(
                    250, sc_types.Unit.KCAL, sc_types.UnitType.ENERGY
                ),
                sc_types.Macro.FIBER: sc_quantity.Quantity(
                    1, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT
                ),
            },
            sc_quantity.Quantity(
                94,
                sc_types.Unit.GRAMS,
                sc_types.UnitType.WEIGHT,
            ),
            datetime.datetime.now().date() + datetime.timedelta(days=5),
            None,
            sc_types.StorageType.FRIDGE,
        ),
        pytest.param(
            "Chicken Breast",
            TEST_UUID_3,
            sc_quantity.Quantity(
                1.23,
                sc_types.Unit.POUNDS,
                sc_types.UnitType.WEIGHT,
            ),
            8.99,
            "QFC",
            {
                sc_types.Macro.CARB: sc_quantity.Quantity(
                    3, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.PROTEIN: sc_quantity.Quantity(
                    27, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.FAT: sc_quantity.Quantity(
                    3.5, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.SUGAR: sc_quantity.Quantity(
                    1, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.CALORIES: sc_quantity.Quantity(
                    160, sc_types.Unit.KCAL, sc_types.UnitType.ENERGY
                ),
                sc_types.Macro.FIBER: sc_quantity.Quantity(
                    0, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT
                ),
            },
            sc_quantity.Quantity(
                112,
                sc_types.Unit.GRAMS,
                sc_types.UnitType.WEIGHT,
            ),
            None,
            None,
            sc_types.StorageType.FREEZER,
            marks=pytest.mark.xfail,
        ),
    ],
)
def test_item_init(
    name,
    item_id,
    quantity,
    price,
    merchant,
    per_serving_macros,
    serving_size,
    expiration_date,
    shelf_life,
    storage,
):
    test_item = sc_item.Item(
        name,
        item_id,
        quantity,
        price,
        merchant,
        per_serving_macros,
        serving_size,
        expiration_date,
        shelf_life,
        storage,
    )

    assert str(test_item) == name
    assert test_item.get_shelf_life_remaining() == datetime.timedelta(days=5).days

    if item_id == TEST_UUID_1:
        assert test_item.storage == sc_types.StorageType.PANTRY
        assert (
            test_item.expiration_date
            == datetime.datetime.now().date() + datetime.timedelta(days=5)
        )
    elif item_id == TEST_UUID_2:
        assert test_item.storage == sc_types.StorageType.FRIDGE


if __name__ == "__main__":
    sys.exit(pytest.main())
