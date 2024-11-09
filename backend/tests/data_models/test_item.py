import datetime
import pytest
import sys

from src.data_models import item as sc_item
from src.data_models import quantity as sc_quantity
from src.utils import types as sc_types


@pytest.mark.parametrize(
    "name, quantity, price, merchant, per_serving_macros, serving_size, shelf_life, storage",
    [
        (
            "banana",
            sc_quantity.Quantity(
                quantity=3,
                unit=sc_types.Unit.NONE,
                type=sc_types.UnitType.NONE,
            ),
            1.50,
            "Whole Foods",
            {
                sc_types.Macro.CARB: sc_quantity.Quantity(
                    quantity=31,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.PROTEIN: sc_quantity.Quantity(
                    quantity=1.48,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.FAT: sc_quantity.Quantity(
                    quantity=0.449,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.SUGAR: sc_quantity.Quantity(
                    quantity=16.6,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.CALORIES: sc_quantity.Quantity(
                    quantity=102,
                    unit=sc_types.Unit.KCAL,
                    type=sc_types.UnitType.ENERGY,
                ),
                sc_types.Macro.FIBER: sc_quantity.Quantity(
                    quantity=3.54,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
            },
            sc_quantity.Quantity(
                quantity=1,
                unit=sc_types.Unit.NONE,
                type=sc_types.UnitType.NONE,
            ),
            datetime.timedelta(days=5),
            sc_types.StorageType.PANTRY,
        ),
        (
            "Four Cheese Ravioli",
            sc_quantity.Quantity(
                quantity=283,
                unit=sc_types.Unit.GRAMS,
                type=sc_types.UnitType.WEIGHT,
            ),
            2.99,
            "Trader Joes",
            {
                sc_types.Macro.CARB: sc_quantity.Quantity(
                    quantity=31,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.PROTEIN: sc_quantity.Quantity(
                    quantity=9,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.FAT: sc_quantity.Quantity(
                    quantity=10,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.SUGAR: sc_quantity.Quantity(
                    quantity=5,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.CALORIES: sc_quantity.Quantity(
                    quantity=250,
                    unit=sc_types.Unit.KCAL,
                    type=sc_types.UnitType.ENERGY,
                ),
                sc_types.Macro.FIBER: sc_quantity.Quantity(
                    quantity=1,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
            },
            sc_quantity.Quantity(
                quantity=94,
                unit=sc_types.Unit.GRAMS,
                type=sc_types.UnitType.WEIGHT,
            ),
            datetime.timedelta(days=5),
            sc_types.StorageType.FRIDGE,
        ),
        (
            "Chicken Breast",
            sc_quantity.Quantity(
                quantity=1.23,
                unit=sc_types.Unit.POUNDS,
                type=sc_types.UnitType.WEIGHT,
            ),
            8.99,
            "QFC",
            {
                sc_types.Macro.CARB: sc_quantity.Quantity(
                    quantity=3,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.PROTEIN: sc_quantity.Quantity(
                    quantity=27,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.FAT: sc_quantity.Quantity(
                    quantity=3.5,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.SUGAR: sc_quantity.Quantity(
                    quantity=1,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.CALORIES: sc_quantity.Quantity(
                    quantity=160,
                    unit=sc_types.Unit.KCAL,
                    type=sc_types.UnitType.ENERGY,
                ),
                sc_types.Macro.FIBER: sc_quantity.Quantity(
                    quantity=0,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
            },
            sc_quantity.Quantity(
                quantity=112,
                unit=sc_types.Unit.GRAMS,
                type=sc_types.UnitType.WEIGHT,
            ),
            datetime.timedelta(
                days=180
            ),  # Changed from None to a long shelf life for frozen items
            sc_types.StorageType.FREEZER,
        ),
    ],
)
def test_item_init(
    name,
    quantity,
    price,
    merchant,
    per_serving_macros,
    serving_size,
    shelf_life,
    storage,
):
    test_item = sc_item.Item(
        name=name,
        quantity=quantity,
        price=price,
        merchant=merchant,
        per_serving_macros=per_serving_macros,
        serving_size=serving_size,
        shelf_life=shelf_life,
        storage=storage,
    )

    assert test_item.name == name
    assert test_item.get_shelf_life_remaining() == shelf_life.days

    if name == "banana":
        assert test_item.storage == sc_types.StorageType.PANTRY
        assert (
            test_item._expiration_date
            == datetime.datetime.now().date() + datetime.timedelta(days=5)
        )
    elif name == "Four Cheese Ravioli":
        assert test_item.storage == sc_types.StorageType.FRIDGE
        assert (
            test_item._expiration_date
            == datetime.datetime.now().date() + datetime.timedelta(days=5)
        )
    elif name == "Chicken Breast":
        assert test_item.storage == sc_types.StorageType.FREEZER
        assert (
            test_item._expiration_date
            == datetime.datetime.now().date() + datetime.timedelta(days=180)
        )


def test_item_equality():
    item1 = sc_item.Item(
        name="Test Item",
        quantity=sc_quantity.Quantity(
            quantity=1,
            unit=sc_types.Unit.NONE,
            type=sc_types.UnitType.NONE,
        ),
        price=1.0,
        merchant="Test Merchant",
        per_serving_macros={},
        serving_size=sc_quantity.Quantity(
            quantity=1,
            unit=sc_types.Unit.NONE,
            type=sc_types.UnitType.NONE,
        ),
        shelf_life=datetime.timedelta(days=1),
        storage=sc_types.StorageType.PANTRY,
    )
    item2 = sc_item.Item(
        name="Test Item",
        quantity=sc_quantity.Quantity(
            quantity=2,
            unit=sc_types.Unit.NONE,
            type=sc_types.UnitType.NONE,
        ),
        price=2.0,
        merchant="Another Merchant",
        per_serving_macros={},
        serving_size=sc_quantity.Quantity(
            quantity=2,
            unit=sc_types.Unit.NONE,
            type=sc_types.UnitType.NONE,
        ),
        shelf_life=datetime.timedelta(days=1),
        storage=sc_types.StorageType.FRIDGE,
    )
    item3 = sc_item.Item(
        name="Different Item",
        quantity=sc_quantity.Quantity(
            quantity=1,
            unit=sc_types.Unit.NONE,
            type=sc_types.UnitType.NONE,
        ),
        price=1.0,
        merchant="Test Merchant",
        per_serving_macros={},
        serving_size=sc_quantity.Quantity(
            quantity=1,
            unit=sc_types.Unit.NONE,
            type=sc_types.UnitType.NONE,
        ),
        shelf_life=datetime.timedelta(days=1),
        storage=sc_types.StorageType.PANTRY,
    )

    assert item1 == item2  # Same name and expiration date
    assert item1 != item3  # Different name
    assert hash(item1) == hash(item2)
    assert hash(item1) != hash(item3)


if __name__ == "__main__":
    sys.exit(pytest.main())
