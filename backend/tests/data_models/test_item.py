import datetime
import pytest
import sys

from src.data_models import item as sc_item
from src.data_models import quantity as sc_quantity
from src.utils import types as sc_types


@pytest.mark.parametrize(
    "name, quantity, shelf_life, storage",
    [
        (
            "banana",
            sc_quantity.Quantity(
                quantity=3,
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
    shelf_life,
    storage,
):
    test_item = sc_item.Item(
        name=name,
        quantity=quantity,
        shelf_life=shelf_life,
        storage=storage,
    )

    assert test_item.name == name
    assert test_item.get_shelf_life_remaining() == shelf_life

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
        shelf_life=datetime.timedelta(days=1),
        storage=sc_types.StorageType.PANTRY,
    )

    assert item1 == item2  # Same name and expiration date
    assert item1 != item3  # Different name
    assert hash(item1) == hash(item2)
    assert hash(item1) != hash(item3)


def test_parse_shelf_life():
    """Test the shelf life parsing function with various formats."""
    test_cases = [
        # ISO 8601 duration format
        ("P1Y", datetime.timedelta(days=365)),
        ("P6M", datetime.timedelta(days=180)),
        ("P2W", datetime.timedelta(days=14)),
        ("P5D", datetime.timedelta(days=5)),
        # Natural language format
        ("1 year", datetime.timedelta(days=365)),
        ("2 years", datetime.timedelta(days=730)),
        ("6 months", datetime.timedelta(days=180)),
        ("2 weeks", datetime.timedelta(days=14)),
        ("5 days", datetime.timedelta(days=5)),
        # Abbreviated formats
        ("1yr", datetime.timedelta(days=365)),
        ("6mo", datetime.timedelta(days=180)),
        ("2wk", datetime.timedelta(days=14)),
        ("5d", datetime.timedelta(days=5)),
        # Simple number (days)
        ("5", datetime.timedelta(days=5)),
        # Decimal values
        ("1.5 years", datetime.timedelta(days=547)),
        ("2.5 months", datetime.timedelta(days=75)),
        # Already a timedelta
        (datetime.timedelta(days=5), datetime.timedelta(days=5)),
    ]

    for input_value, expected_output in test_cases:
        test_item = sc_item.Item(
            name="Test Item",
            quantity=sc_quantity.Quantity(
                quantity=1,
                unit=sc_types.Unit.NONE,
                type=sc_types.UnitType.NONE,
            ),
            shelf_life=input_value,
            storage=sc_types.StorageType.PANTRY,
        )
        assert test_item.get_shelf_life_remaining() == expected_output


def test_parse_shelf_life_errors():
    """Test error cases for shelf life parsing."""
    invalid_inputs = [
        "invalid",
        "P1X",  # Invalid ISO duration
        "1 decade",  # Unsupported unit
        "year",  # Missing number
        None,  # Invalid type
        123,  # Invalid type
    ]

    for invalid_input in invalid_inputs:
        with pytest.raises(ValueError):
            print(invalid_input)
            sc_item.Item(
                name="Test Item",
                quantity=sc_quantity.Quantity(
                    quantity=1,
                    unit=sc_types.Unit.NONE,
                    type=sc_types.UnitType.NONE,
                ),
                shelf_life=invalid_input,
                storage=sc_types.StorageType.PANTRY,
            )


if __name__ == "__main__":
    sys.exit(pytest.main())
